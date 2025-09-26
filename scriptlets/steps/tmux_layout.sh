#!/usr/bin/env bash
set -Eeuo pipefail

# ------------------ Defaults ------------------
windows=1
panes=1
declare -a window_names=()
declare -a pane_names=()
session_name="session_$(date +%s)"
layout="tiled"              # tiled|even-horizontal|even-vertical|main-vertical|main-horizontal
log_dir="Logs"
append_logs=0               # 0: truncate, 1: append
capture_history=1           # 1 -> pipe-pane -O to include history
base_index=1                # 1 or 0
pane_border_status=1        # show pane titles on borders
sync_panes=0                # synchronize panes per window
remain_on_exit=0            # close panes immediately when process exits

# ------------------ Helpers -------------------
die() { echo "Error: $*" >&2; exit 1; }

need_cmd() { command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1"; }

is_pos_int() { [[ "$1" =~ ^[1-9][0-9]*$ ]]; }

sanitize() { # safe for filenames
  local s=$1
  s=${s// /_}
  s=$(printf '%s' "$s" | tr -c 'A-Za-z0-9._-' '_')
  printf '%s' "$s"
}

usage() {
  cat <<EOF
Usage: $0 [options]
Options:
  -w, --windows <n>              Number of windows (default: $windows)
  -wn, -W, --window-names <csv>  Comma-separated window names
  -p, --panes <n>                Number of panes per window (default: $panes)
  -pn, -P, --pane-names <csv>    Comma-separated pane names
  -sn, --session-name <name>     Custom tmux session name
  -L, --layout <layout>          Layout: tiled|even-horizontal|even-vertical|main-vertical|main-horizontal
  --log-dir <dir>                Directory for logs (default: $log_dir)
  --append-logs                  Append instead of truncate logs
  --no-history                   Do not capture existing pane history into logs
  --no-border-titles             Disable pane border titles
  --base-index <0|1>             Base index for windows/panes (default: $base_index)
  --sync                         Enable synchronize-panes per window
  --remain-on-exit               Keep panes visible after exit (default: off)
  -h, --help                     Show this help
EOF
  exit 1
}

# ------------------ Parse args ----------------
need_cmd tmux

# Expand long options to short-like tokens
args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --windows)           args+=(-w "$2"); shift 2 ;;
    --window-names)      args+=(-W "$2"); shift 2 ;;
    --panes)             args+=(-p "$2"); shift 2 ;;
    --pane-names)        args+=(-P "$2"); shift 2 ;;
    --session-name)      args+=(-s "$2"); shift 2 ;;
    --layout)            args+=(-l "$2"); shift 2 ;;
    --log-dir)           args+=(--LD "$2"); shift 2 ;;
    --append-logs)       args+=(--AL); shift ;;
    --no-history)        args+=(--NH); shift ;;
    --no-border-titles)  args+=(--NBT); shift ;;
    --base-index)        args+=(--BI "$2"); shift 2 ;;
    --sync)              args+=(--SYNC); shift ;;
    --remain-on-exit)    args+=(--ROE); shift ;;
    -h|--help)           usage ;;
    *)                   args+=("$1"); shift ;;
  esac
done
set -- "${args[@]}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -w) windows="${2:-}"; shift 2 ;;
    -W|-wn) IFS=',' read -r -a window_names <<< "${2:-}"; shift 2 ;;
    -p) panes="${2:-}"; shift 2 ;;
    -P|-pn) IFS=',' read -r -a pane_names   <<< "${2:-}"; shift 2 ;;
    -s|-sn) session_name="${2:-}"; shift 2 ;;
    -l) layout="${2:-}"; shift 2 ;;
    --LD) log_dir="${2:-}"; shift 2 ;;
    --AL) append_logs=1; shift ;;
    --NH) capture_history=0; shift ;;
    --NBT) pane_border_status=0; shift ;;
    --BI) base_index="${2:-}"; shift 2 ;;
    --SYNC) sync_panes=1; shift ;;
    --ROE) remain_on_exit=1; shift ;;
    -h|--help) usage ;;
    *) die "Unknown option: $1" ;;
  esac
done

is_pos_int "$windows" || die "-w/--windows must be a positive integer"
is_pos_int "$panes"   || die "-p/--panes must be a positive integer"
[[ "$layout" =~ ^(tiled|even-horizontal|even-vertical|main-vertical|main-horizontal)$ ]] || \
  die "--layout must be one of tiled|even-horizontal|even-vertical|main-vertical|main-horizontal"
[[ "$base_index" =~ ^[01]$ ]] || die "--base-index must be 0 or 1"

mkdir -p "$log_dir"

# Avoid session name collisions
if tmux has-session -t "$session_name" 2>/dev/null; then
  session_name="${session_name}_$$"
fi

# ------------------ Start session ----------------
first_win_name="${window_names[0]:-win0}"
tmux new-session -d -s "$session_name" -n "$first_win_name"

# Per-session options (no -g)
tmux set-option  -t "$session_name" mouse on
tmux set-option  -t "$session_name" status-left "#[bold]#S"
tmux set-option  -t "$session_name" allow-rename off
tmux set-option  -t "$session_name" remain-on-exit "$( ((remain_on_exit)) && echo on || echo off )"
tmux set-option  -t "$session_name" base-index "$base_index"
tmux set-option  -t "$session_name" exit-empty on   # 👈 Auto-close session when last pane exits

# ------------------ Build windows/panes ----------------
for ((w=0; w<windows; w++)); do
  win_name="${window_names[w]:-win$w}"
  if (( w != 0 )); then
    tmux new-window -t "$session_name" -n "$win_name"
  else
    tmux rename-window -t "$session_name:$w" "$win_name"
  fi

  if (( pane_border_status )); then
    tmux set-window-option -t "$session_name:$w" pane-border-status top
    tmux set-window-option -t "$session_name:$w" pane-border-format '#{?pane_active,#[bold],}#T'
  fi

  for ((p=1; p<panes; p++)); do
    tmux split-window -t "$session_name:$w" -h
    tmux select-layout -t "$session_name:$w" "$layout"
  done

  tmux set-window-option -t "$session_name:$w" synchronize-panes "$( ((sync_panes)) && echo on || echo off )"

  tmux set-option -t "$session_name" pane-border-style 'fg=grey'
  tmux set-option -t "$session_name" pane-active-border-style 'fg=brightred'

  while IFS=' ' read -r pane_id pane_idx; do
    pane_label="${pane_names[pane_idx]:-pane$pane_idx}"
    safe_session=$(sanitize "$session_name")
    safe_win=$(sanitize "$win_name")
    safe_label=$(sanitize "$pane_label")
    full_title="${safe_session}_${safe_win}_${pane_idx}_${safe_label}"

    tmux select-pane -t "$pane_id" -T "$pane_label"
    tmux send-keys -t "$pane_id" "printf '\\033]2;%s\\033\\\\' '$full_title'" C-m

    log_file="$log_dir/${full_title}.log"
    redir=">"
    (( append_logs )) && redir=">>"
    flags=()
    (( capture_history )) && flags+=(-O)
    flags+=(-o)
    tmux pipe-pane "${flags[@]}" -t "$pane_id" "cat $redir \"$log_file\""
  done < <(tmux list-panes -t "$session_name:$w" -F "#{pane_id} #{pane_index}")
done

# ------------------ Attach or switch ----------------
tmux select-window -t "$session_name:0"
if [[ -n "${TMUX:-}" ]]; then
  tmux switch-client -t "$session_name"
else
  tmux attach-session -t "$session_name"
fi
