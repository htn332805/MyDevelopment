import json
import subprocess
import sys


def run_tmux_cmd(cmd):
    """Run a tmux command and capture errors."""
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}")
    return result


def split_to_grid(session, window, total_panes):
    """Split the tmux window into a fixed 4x4 grid (16 panes)."""
    target = f"{session}:{window}"

    # Create a 4x4 grid by splitting panes strategically
    pane_index = 0
    for row in range(3):  # 3 horizontal splits to make 4 rows
        run_tmux_cmd(["tmux", "split-window", "-v", "-t", target, "-l", "5"])
        run_tmux_cmd(["tmux", "select-layout", "-t", target, "tiled"])

    for i in range(4):  # Now for each of 4 rows, split horizontally 3 times
        for j in range(3):
            run_tmux_cmd(["tmux", "select-pane", "-t", f"{target}.{i*4 + j}"])
            run_tmux_cmd(
                ["tmux", "split-window", "-h", "-t", f"{target}.{i*4 + j}", "-l", "20"]
            )
            run_tmux_cmd(["tmux", "select-layout", "-t", target, "tiled"])


def set_pane_titles(session, window_index, panes):
    """Set titles for all panes."""
    for i, pane in enumerate(panes):
        title = pane.get("title") or pane.get("name") or f"Pane{i}"
        run_tmux_cmd(["tmux", "select-pane", "-t", f"{session}:{window_index}.{i}"])
        run_tmux_cmd(["tmux", "select-pane", "-T", title])


def send_commands_to_panes(session, window_index, panes):
    """Send user-defined commands to each pane."""
    for i, pane in enumerate(panes):
        cmd = pane.get("command", "bash")
        run_tmux_cmd(
            ["tmux", "send-keys", "-t", f"{session}:{window_index}.{i}", cmd, "C-m"]
        )


if len(sys.argv) != 2:
    print("Usage: python create_tmux_layout.py <layout.json>")
    sys.exit(1)

# Load JSON
config_file = sys.argv[1]
with open(config_file) as f:
    config = json.load(f)

session_name = config["name"]
window = config["windows"][0]
window_name = window["name"]
panes = window["panes"]
window_layout = window.get("layout", "tiled")

# --- Create session and window
run_tmux_cmd(["tmux", "new-session", "-d", "-s", session_name, "-n", window_name])

# --- Apply tmux options
options = config.get("options", {})
for opt, val in options.items():
    val_str = "on" if val is True else "off" if val is False else str(val)
    run_tmux_cmd(["tmux", "set-option", "-g", str(opt), val_str])

# --- Build fixed 4x4 grid of panes
split_to_grid(session_name, 0, 16)

# --- Set pane titles
set_pane_titles(session_name, 0, panes)

# --- Send commands
send_commands_to_panes(session_name, 0, panes)

# --- Set layout one last time
run_tmux_cmd(["tmux", "select-layout", "-t", f"{session_name}:0", window_layout])

# --- Attach session
run_tmux_cmd(["tmux", "attach-session", "-t", session_name])
