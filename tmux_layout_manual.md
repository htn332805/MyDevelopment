# TMux Layout Manager - User Manual

## Overview

The `tmux_layout.sh` script is a comprehensive tool for creating and managing tmux sessions with customizable layouts, multiple windows, and multiple panes. It provides automated logging, pane management, and session configuration with a rich set of options for development and debugging workflows.

## Features

### Core Capabilities
- **Multi-window Sessions**: Create sessions with multiple named windows
- **Multi-pane Windows**: Split windows into multiple panes with customizable layouts
- **Automated Logging**: Capture pane output to log files with optional history
- **Session Management**: Automatic session naming with collision avoidance
- **Layout Options**: Support for 5 different tmux layouts
- **Pane Synchronization**: Optional synchronized input across panes
- **Border Titles**: Named pane borders for easy identification
- **Flexible Configuration**: Extensive command-line options for customization

### Advanced Features
- **Sanitized File Names**: Automatic filename sanitization for logs
- **History Capture**: Include existing pane history in logs
- **Session Persistence**: Configure pane behavior on command exit
- **Mouse Support**: Enabled by default for easier navigation
- **Index Configuration**: Configurable base index for windows and panes
- **Status Customization**: Custom status bar configuration

## Installation and Requirements

### Prerequisites
- **tmux**: Version 3.0 or higher (tested with 3.4)
- **bash**: Version 4.0 or higher
- **Standard Unix utilities**: `tr`, `printf`, `cat`, `mkdir`

### Installation
```bash
# Make the script executable
chmod +x scriptlets/steps/tmux_layout.sh

# Optionally, add to PATH for global access
export PATH="$PATH:$(pwd)/scriptlets/steps"
```

## Command Line Options

### Basic Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--windows <n>` | `-w` | Number of windows to create | `1` |
| `--window-names <csv>` | `-wn`, `-W` | Comma-separated window names | `win0, win1, ...` |
| `--panes <n>` | `-p` | Number of panes per window | `1` |
| `--pane-names <csv>` | `-pn`, `-P` | Comma-separated pane names | `pane0, pane1, ...` |
| `--session-name <name>` | `-sn` | Custom session name | `session_<timestamp>` |

### Layout Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--layout <layout>` | `-L` | Pane layout style | `tiled` |

**Available Layouts:**
- `tiled` - Arrange panes in a tiled pattern
- `even-horizontal` - Divide panes horizontally with equal sizes
- `even-vertical` - Divide panes vertically with equal sizes
- `main-horizontal` - One large horizontal pane with others below
- `main-vertical` - One large vertical pane with others to the right

### Logging Options

| Option | Description | Default |
|--------|-------------|---------|
| `--log-dir <dir>` | Directory for log files | `Logs` |
| `--append-logs` | Append to existing logs instead of truncating | `false` |
| `--no-history` | Don't capture existing pane history | `false` |

### Display Options

| Option | Description | Default |
|--------|-------------|---------|
| `--no-border-titles` | Disable pane border titles | `false` |
| `--base-index <0\|1>` | Base index for windows/panes | `1` |

### Behavior Options

| Option | Description | Default |
|--------|-------------|---------|
| `--sync` | Enable pane synchronization per window | `false` |
| `--remain-on-exit` | Keep panes visible after process exits | `false` |

### Help

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show usage help |

## Usage Examples

### Basic Usage

#### Single Window, Single Pane
```bash
./tmux_layout.sh
```
Creates a basic tmux session with one window and one pane.

#### Multiple Panes
```bash
./tmux_layout.sh --panes 4 --layout tiled
```
Creates a session with 4 panes arranged in a tiled layout.

### Window Management

#### Multiple Windows
```bash
./tmux_layout.sh --windows 3 --window-names "development,testing,logs"
```
Creates 3 windows with custom names.

#### Combined Windows and Panes
```bash
./tmux_layout.sh --windows 2 --panes 2 \
  --window-names "frontend,backend" \
  --pane-names "server,client"
```

### Layout Examples

#### Development Environment
```bash
./tmux_layout.sh \
  --windows 2 \
  --window-names "code,monitoring" \
  --panes 3 \
  --layout main-vertical \
  --session-name "dev-session"
```

#### Split Screen Debugging
```bash
./tmux_layout.sh \
  --panes 2 \
  --layout even-horizontal \
  --pane-names "debugger,output" \
  --sync \
  --session-name "debug"
```

### Logging Configuration

#### Custom Log Directory
```bash
./tmux_layout.sh \
  --log-dir "/var/log/tmux-sessions" \
  --panes 3 \
  --append-logs
```

#### Development with History
```bash
./tmux_layout.sh \
  --panes 4 \
  --layout tiled \
  --log-dir "development-logs" \
  --session-name "dev-$(date +%Y%m%d)"
```

### Advanced Scenarios

#### Multi-Environment Setup
```bash
./tmux_layout.sh \
  --windows 4 \
  --window-names "development,staging,production,monitoring" \
  --panes 2 \
  --layout even-vertical \
  --log-dir "env-logs" \
  --base-index 0 \
  --remain-on-exit
```

#### Team Collaboration Session
```bash
./tmux_layout.sh \
  --windows 3 \
  --window-names "main,testing,logs" \
  --panes 3 \
  --layout main-horizontal \
  --sync \
  --session-name "team-session" \
  --no-border-titles
```

## File Structure and Logging

### Log File Naming Convention
Log files are automatically named using the pattern:
```
{sanitized_session}_{sanitized_window}_{pane_index}_{sanitized_pane_name}.log
```

Example: `dev_session_frontend_0_server.log`

### Directory Structure
```
project/
├── Logs/                           # Default log directory
│   ├── session_12345_win0_0_pane0.log
│   ├── session_12345_win0_1_pane1.log
│   └── ...
└── scriptlets/
    └── steps/
        └── tmux_layout.sh
```

### Log Content
- **Standard Mode**: Captures new pane output only
- **History Mode**: Includes existing pane history (default)
- **Append Mode**: Appends to existing logs instead of overwriting

## Session Management

### Session Naming
- **Default**: `session_<unix_timestamp>`
- **Custom**: Use `--session-name` option
- **Collision Handling**: Automatic suffix addition (`_$$`) if session exists

### Session Options Configured
- **Mouse support**: Enabled for easier navigation
- **Status bar**: Custom format with session name
- **Window renaming**: Disabled to preserve custom names
- **Auto-close**: Session closes when last pane exits
- **Border styling**: Grey borders, red active border

### Attaching to Sessions
The script automatically:
1. Creates the session in detached mode
2. Configures all windows and panes
3. Attaches to the session (or switches if already in tmux)

## Troubleshooting

### Common Issues

#### "Missing required command: tmux"
**Solution**: Install tmux
```bash
# Ubuntu/Debian
sudo apt-get install tmux

# MacOS
brew install tmux

# CentOS/RHEL
sudo yum install tmux
```

#### "Session already exists"
The script automatically handles session name collisions by appending the process ID. If you want to force a specific session name:
```bash
# Kill existing session first
tmux kill-session -t my-session
./tmux_layout.sh --session-name my-session
```

#### Logs not being created
**Check permissions**:
```bash
# Ensure log directory is writable
chmod 755 Logs/
```

**Verify log directory**:
```bash
ls -la Logs/
```

#### Panes not splitting correctly
**Verify positive integers**:
```bash
# This will fail
./tmux_layout.sh --panes 0

# This will work
./tmux_layout.sh --panes 2
```

### Debug Mode
For troubleshooting, you can enable bash debug mode:
```bash
bash -x ./tmux_layout.sh --panes 2
```

### Validation Errors
The script validates:
- Window count must be positive integer
- Pane count must be positive integer  
- Layout must be one of the 5 supported types
- Base index must be 0 or 1

## Integration Examples

### With Development Workflows

#### Git Development
```bash
./tmux_layout.sh \
  --windows 3 \
  --window-names "code,git,test" \
  --panes 2 \
  --layout even-vertical \
  --session-name "git-workflow"
```

#### Docker Development
```bash
./tmux_layout.sh \
  --windows 2 \
  --window-names "containers,logs" \
  --panes 4 \
  --layout tiled \
  --log-dir "docker-logs" \
  --session-name "docker-dev"
```

### With CI/CD

#### Build Monitoring
```bash
./tmux_layout.sh \
  --windows 4 \
  --window-names "build,test,deploy,monitor" \
  --panes 1 \
  --log-dir "ci-logs" \
  --append-logs \
  --session-name "ci-$(date +%Y%m%d-%H%M)"
```

### Script Integration
```bash
#!/bin/bash
# Start development environment
./tmux_layout.sh \
  --windows 3 \
  --window-names "editor,server,database" \
  --panes 2 \
  --session-name "dev-env"

# Send commands to specific panes
tmux send-keys -t dev-env:editor:0 "vim ." C-m
tmux send-keys -t dev-env:server:0 "npm start" C-m
tmux send-keys -t dev-env:database:0 "docker-compose up" C-m
```

## Best Practices

### Session Organization
1. **Use descriptive session names** for easy identification
2. **Organize by purpose** (development, monitoring, debugging)
3. **Use consistent naming conventions** across projects

### Window and Pane Management
1. **Limit panes per window** to avoid overcrowding (2-4 recommended)
2. **Use appropriate layouts** based on content type
3. **Name windows and panes** descriptively

### Logging Strategy
1. **Organize logs by purpose** using custom log directories
2. **Use append mode** for long-running sessions
3. **Include timestamps** in session names for tracking

### Performance Considerations
1. **Monitor resource usage** with many panes
2. **Clean up old sessions** regularly
3. **Limit history capture** for high-output panes

## Advanced Configuration

### Environment Integration
The script can be integrated into your shell profile:
```bash
# ~/.bashrc or ~/.zshrc
alias dev-tmux='path/to/tmux_layout.sh --windows 3 --panes 2 --layout main-vertical'
```

### Custom Wrapper Scripts
```bash
#!/bin/bash
# dev-environment.sh
PROJECT_NAME=${1:-"project"}
LOG_DIR="logs/$PROJECT_NAME"

./tmux_layout.sh \
  --session-name "$PROJECT_NAME" \
  --windows 3 \
  --window-names "code,server,database" \
  --panes 2 \
  --layout main-vertical \
  --log-dir "$LOG_DIR" \
  --append-logs
```

This manual provides comprehensive coverage of the tmux_layout.sh script's capabilities, usage patterns, and integration possibilities. The script is designed to be flexible and powerful for various development and system administration workflows.