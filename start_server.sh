#!/bin/bash
#
# Framework0 Context Server Startup Script
#
# This script provides easy startup and management for the Framework0 Enhanced
# Context Server with support for different deployment modes and environments.
#

# Script configuration and metadata
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"  # Get script directory
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"                # Get project root
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"               # Script name for messages

# Default configuration values
DEFAULT_HOST="0.0.0.0"            # Default server host
DEFAULT_PORT="8080"               # Default server port
DEFAULT_CONFIG="configs/server.json"  # Default config file path
DEFAULT_LOG_LEVEL="INFO"          # Default logging level

# Environment configuration (can be overridden by environment variables)
CONTEXT_SERVER_HOST="${CONTEXT_SERVER_HOST:-$DEFAULT_HOST}"
CONTEXT_SERVER_PORT="${CONTEXT_SERVER_PORT:-$DEFAULT_PORT}"
CONTEXT_CONFIG_FILE="${CONTEXT_CONFIG_FILE:-$DEFAULT_CONFIG}"
CONTEXT_LOG_LEVEL="${CONTEXT_LOG_LEVEL:-$DEFAULT_LOG_LEVEL}"
CONTEXT_PYTHON_ENV="${CONTEXT_PYTHON_ENV:-}"                # Optional Python virtual environment

# Color codes for output formatting
RED='\033[0;31m'      # Error messages
GREEN='\033[0;32m'    # Success messages  
YELLOW='\033[0;33m'   # Warning messages
BLUE='\033[0;34m'     # Information messages
CYAN='\033[0;36m'     # Highlight messages
NC='\033[0m'          # No Color - reset

# Logging functions for consistent output
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_highlight() {
    echo -e "${CYAN}[HIGHLIGHT]${NC} $1" >&2
}

# Function to display help information
show_help() {
    cat << EOF
Framework0 Context Server Startup Script

USAGE:
    $SCRIPT_NAME <command> [options]

COMMANDS:
    start                 Start the context server
    stop                  Stop the context server  
    restart              Restart the context server
    status               Show server status
    logs                 Show server logs (if logging to file)
    config               Manage configuration
    install              Install dependencies
    help                 Show this help message

OPTIONS:
    -h, --host <host>     Server host address (default: $DEFAULT_HOST)
    -p, --port <port>     Server port number (default: $DEFAULT_PORT)
    -c, --config <file>   Configuration file path (default: $DEFAULT_CONFIG)
    -e, --env <path>      Python virtual environment path
    -d, --daemon          Run server in daemon mode (background)
    -v, --verbose         Enable verbose output
    --debug               Enable debug mode
    --no-color            Disable colored output

ENVIRONMENT VARIABLES:
    CONTEXT_SERVER_HOST   Override server host
    CONTEXT_SERVER_PORT   Override server port  
    CONTEXT_CONFIG_FILE   Override config file path
    CONTEXT_LOG_LEVEL     Override log level (DEBUG, INFO, WARNING, ERROR)
    CONTEXT_PYTHON_ENV    Override Python virtual environment path

EXAMPLES:
    # Start server with defaults
    $SCRIPT_NAME start
    
    # Start server on specific host and port
    $SCRIPT_NAME start --host localhost --port 9090
    
    # Start server with custom config
    $SCRIPT_NAME start --config my_config.json
    
    # Start server in background
    $SCRIPT_NAME start --daemon
    
    # Check server status
    $SCRIPT_NAME status
    
    # Restart server
    $SCRIPT_NAME restart

EXIT CODES:
    0    Success
    1    General error
    2    Invalid arguments
    3    Server connection error
    4    Configuration error
    5    Dependency error

EOF
}

# Function to check if required dependencies are available
check_dependencies() {
    local missing_deps=()
    
    # Check for Python
    if ! command -v python3 >/dev/null 2>&1; then
        missing_deps+=("python3")
    fi
    
    # Check for required Python packages (if virtual env is active)
    if [[ -n "$CONTEXT_PYTHON_ENV" ]] || [[ -n "$VIRTUAL_ENV" ]]; then
        local python_cmd="python3"
        if [[ -n "$CONTEXT_PYTHON_ENV" ]]; then
            python_cmd="$CONTEXT_PYTHON_ENV/bin/python"
        fi
        
        # Check for Flask (required for server)
        if ! $python_cmd -c "import flask" >/dev/null 2>&1; then
            log_warning "Flask not found - may need to install dependencies"
        fi
    fi
    
    # Report missing dependencies
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install missing dependencies and try again"
        return 5  # Dependency error code
    fi
    
    return 0
}

# Function to activate Python virtual environment if specified
activate_python_env() {
    if [[ -n "$CONTEXT_PYTHON_ENV" ]]; then
        if [[ -f "$CONTEXT_PYTHON_ENV/bin/activate" ]]; then
            log_info "Activating Python environment: $CONTEXT_PYTHON_ENV"
            source "$CONTEXT_PYTHON_ENV/bin/activate"
        else
            log_error "Python environment not found: $CONTEXT_PYTHON_ENV"
            return 5  # Dependency error
        fi
    fi
    
    return 0
}

# Function to get server PID from process list
get_server_pid() {
    # Look for Python process running enhanced_context_server.py
    pgrep -f "enhanced_context_server.py" 2>/dev/null | head -n1
}

# Function to check if server is running
is_server_running() {
    local pid
    pid=$(get_server_pid)
    
    if [[ -n "$pid" ]]; then
        # Double-check that process is still alive
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # Server is running
        fi
    fi
    
    return 1  # Server is not running
}

# Function to wait for server to start
wait_for_server_start() {
    local timeout=30  # 30 second timeout
    local count=0
    
    log_info "Waiting for server to start..."
    
    while [[ $count -lt $timeout ]]; do
        if is_server_running; then
            log_success "Server started successfully"
            return 0
        fi
        
        sleep 1
        ((count++))
    done
    
    log_error "Server failed to start within $timeout seconds"
    return 1
}

# Function to wait for server to stop  
wait_for_server_stop() {
    local timeout=10  # 10 second timeout
    local count=0
    
    log_info "Waiting for server to stop..."
    
    while [[ $count -lt $timeout ]]; do
        if ! is_server_running; then
            log_success "Server stopped successfully"
            return 0
        fi
        
        sleep 1
        ((count++))
    done
    
    log_warning "Server did not stop gracefully, may need to force kill"
    return 1
}

# Function to start the context server
start_server() {
    local daemon_mode=false
    local debug_mode=false
    local verbose_mode=false
    
    # Parse start command options
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--daemon)
                daemon_mode=true
                shift
                ;;
            --debug)
                debug_mode=true
                shift
                ;;
            -v|--verbose)
                verbose_mode=true
                shift
                ;;
            *)
                log_error "Unknown start option: $1"
                return 2
                ;;
        esac
    done
    
    # Check if server is already running
    if is_server_running; then
        local pid
        pid=$(get_server_pid)
        log_warning "Server is already running (PID: $pid)"
        return 0
    fi
    
    # Check dependencies and activate environment
    check_dependencies || return $?
    activate_python_env || return $?
    
    # Build server command
    local server_cmd=()
    server_cmd+=("python3")
    server_cmd+=("$PROJECT_ROOT/server/enhanced_context_server.py")
    server_cmd+=("--host" "$CONTEXT_SERVER_HOST")
    server_cmd+=("--port" "$CONTEXT_SERVER_PORT")
    
    if [[ "$debug_mode" == "true" ]]; then
        server_cmd+=("--debug")
    fi
    
    log_info "Starting context server..."
    log_highlight "Host: $CONTEXT_SERVER_HOST"
    log_highlight "Port: $CONTEXT_SERVER_PORT"
    log_highlight "Config: $CONTEXT_CONFIG_FILE"
    
    # Change to project directory
    cd "$PROJECT_ROOT" || {
        log_error "Failed to change to project directory: $PROJECT_ROOT"
        return 1
    }
    
    if [[ "$daemon_mode" == "true" ]]; then
        # Start server in background
        log_info "Starting server in daemon mode..."
        
        # Create logs directory if it doesn't exist
        mkdir -p "$PROJECT_ROOT/logs"
        
        # Start server with output redirection
        nohup "${server_cmd[@]}" \
            > "$PROJECT_ROOT/logs/server.log" \
            2> "$PROJECT_ROOT/logs/server.error.log" &
        
        local server_pid=$!
        log_info "Server started in background with PID: $server_pid"
        
        # Wait briefly and check if server is running
        sleep 2
        if wait_for_server_start; then
            log_success "Server is running at http://$CONTEXT_SERVER_HOST:$CONTEXT_SERVER_PORT"
            return 0
        else
            log_error "Server failed to start - check logs for details"
            return 1
        fi
    else
        # Start server in foreground
        log_info "Starting server in foreground mode (Ctrl+C to stop)..."
        exec "${server_cmd[@]}"
    fi
}

# Function to stop the context server
stop_server() {
    local force_kill=false
    
    # Parse stop command options
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--force)
                force_kill=true
                shift
                ;;
            *)
                log_error "Unknown stop option: $1"
                return 2
                ;;
        esac
    done
    
    # Check if server is running
    if ! is_server_running; then
        log_info "Server is not running"
        return 0
    fi
    
    local pid
    pid=$(get_server_pid)
    log_info "Stopping server (PID: $pid)..."
    
    if [[ "$force_kill" == "true" ]]; then
        # Force kill immediately
        log_warning "Force killing server process"
        kill -9 "$pid" 2>/dev/null
        log_success "Server process terminated"
        return 0
    else
        # Try graceful shutdown first
        log_info "Sending TERM signal for graceful shutdown..."
        kill -TERM "$pid" 2>/dev/null
        
        if wait_for_server_stop; then
            return 0
        else
            # Graceful shutdown failed, force kill
            log_warning "Graceful shutdown failed, force killing..."
            kill -9 "$pid" 2>/dev/null
            log_success "Server process terminated"
            return 0
        fi
    fi
}

# Function to show server status
show_status() {
    if is_server_running; then
        local pid
        pid=$(get_server_pid)
        
        log_success "Server is running"
        echo "  PID: $pid"
        echo "  Host: $CONTEXT_SERVER_HOST"
        echo "  Port: $CONTEXT_SERVER_PORT"
        echo "  URL: http://$CONTEXT_SERVER_HOST:$CONTEXT_SERVER_PORT"
        
        # Test server connectivity
        if command -v curl >/dev/null 2>&1; then
            if curl -s --connect-timeout 3 "http://$CONTEXT_SERVER_HOST:$CONTEXT_SERVER_PORT/" >/dev/null; then
                echo "  Status: ✅ Reachable"
            else
                echo "  Status: ⚠️  Process running but not responding"
            fi
        else
            echo "  Status: ❓ Cannot test (curl not available)"
        fi
    else
        log_info "Server is not running"
        echo "  Host: $CONTEXT_SERVER_HOST"
        echo "  Port: $CONTEXT_SERVER_PORT"
        echo "  Status: ❌ Stopped"
    fi
}

# Function to restart the server
restart_server() {
    log_info "Restarting context server..."
    
    # Stop server if running
    if is_server_running; then
        stop_server "$@" || return $?
        sleep 2  # Brief pause between stop and start
    fi
    
    # Start server with original arguments
    start_server "$@"
}

# Function to show server logs
show_logs() {
    local log_file="$PROJECT_ROOT/logs/server.log"
    local error_log_file="$PROJECT_ROOT/logs/server.error.log"
    local follow_mode=false
    local lines=50
    
    # Parse logs command options
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--follow)
                follow_mode=true
                shift
                ;;
            -n|--lines)
                lines="$2"
                shift 2
                ;;
            *)
                log_error "Unknown logs option: $1"
                return 2
                ;;
        esac
    done
    
    if [[ ! -f "$log_file" ]]; then
        log_warning "Log file not found: $log_file"
        log_info "Server may not be running in daemon mode or logs disabled"
        return 1
    fi
    
    log_info "Server logs from: $log_file"
    echo "----------------------------------------"
    
    if [[ "$follow_mode" == "true" ]]; then
        # Follow logs in real-time
        tail -f -n "$lines" "$log_file"
    else
        # Show last N lines
        tail -n "$lines" "$log_file"
        
        # Show errors if error log exists and has content
        if [[ -f "$error_log_file" ]] && [[ -s "$error_log_file" ]]; then
            echo ""
            echo "=========================================="
            echo "Recent errors from: $error_log_file"
            echo "=========================================="
            tail -n 20 "$error_log_file"
        fi
    fi
}

# Function to manage configuration
manage_config() {
    local action="$1"
    shift
    
    case "$action" in
        "create")
            log_info "Creating default configuration file..."
            python3 "$PROJECT_ROOT/configs/server_config.py" config create "$CONTEXT_CONFIG_FILE"
            ;;
        "validate")
            log_info "Validating configuration file..."
            python3 "$PROJECT_ROOT/configs/server_config.py" config validate "$CONTEXT_CONFIG_FILE"
            ;;
        "show")
            if [[ -f "$CONTEXT_CONFIG_FILE" ]]; then
                log_info "Configuration file: $CONTEXT_CONFIG_FILE"
                echo "----------------------------------------"
                cat "$CONTEXT_CONFIG_FILE"
            else
                log_warning "Configuration file not found: $CONTEXT_CONFIG_FILE"
            fi
            ;;
        *)
            log_error "Unknown config action: $action"
            log_info "Available config actions: create, validate, show"
            return 2
            ;;
    esac
}

# Function to install dependencies
install_dependencies() {
    log_info "Installing Framework0 Context Server dependencies..."
    
    # Activate Python environment if specified
    activate_python_env || return $?
    
    # Change to project directory
    cd "$PROJECT_ROOT" || {
        log_error "Failed to change to project directory: $PROJECT_ROOT"
        return 1
    }
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        log_info "Installing Python packages from requirements.txt..."
        pip install -r requirements.txt
        
        if [[ $? -eq 0 ]]; then
            log_success "Dependencies installed successfully"
        else
            log_error "Failed to install dependencies"
            return 1
        fi
    else
        log_warning "requirements.txt not found, installing core dependencies..."
        pip install flask flask-socketio python-socketio aiohttp requests
    fi
    
    return 0
}

# Main function to handle command-line arguments
main() {
    local command=""
    
    # Parse global options and command
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--host)
                CONTEXT_SERVER_HOST="$2"
                shift 2
                ;;
            -p|--port)
                CONTEXT_SERVER_PORT="$2"
                shift 2
                ;;
            -c|--config)
                CONTEXT_CONFIG_FILE="$2"
                shift 2
                ;;
            -e|--env)
                CONTEXT_PYTHON_ENV="$2"
                shift 2
                ;;
            --no-color)
                # Disable colors by clearing color variables
                RED='' GREEN='' YELLOW='' BLUE='' CYAN='' NC=''
                shift
                ;;
            help|--help)
                show_help
                exit 0
                ;;
            start|stop|restart|status|logs|config|install)
                command="$1"
                shift
                break  # Remaining arguments are for the command
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 2
                ;;
        esac
    done
    
    # Validate command
    if [[ -z "$command" ]]; then
        log_error "No command specified"
        show_help
        exit 2
    fi
    
    # Execute command
    case "$command" in
        "start")
            start_server "$@"
            ;;
        "stop")
            stop_server "$@"
            ;;
        "restart")
            restart_server "$@"
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs "$@"
            ;;
        "config")
            if [[ $# -eq 0 ]]; then
                log_error "Config command requires an action"
                log_info "Available actions: create, validate, show"
                exit 2
            fi
            manage_config "$@"
            ;;
        "install")
            install_dependencies
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 2
            ;;
    esac
}

# Execute main function with all script arguments
main "$@"