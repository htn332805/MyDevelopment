#!/bin/bash
#
# Context Server Shell Client - Cross-Platform Context Management
#
# This shell script provides a simple command-line interface for interacting
# with the Framework0 Enhanced Context Server. Supports get/set operations,
# monitoring, and debugging features for shell scripts and automation.
#

# Default configuration - can be overridden by environment variables
CONTEXT_SERVER_HOST="${CONTEXT_SERVER_HOST:-localhost}"  # Server host address
CONTEXT_SERVER_PORT="${CONTEXT_SERVER_PORT:-8080}"       # Server port number
CONTEXT_SERVER_URL="http://${CONTEXT_SERVER_HOST}:${CONTEXT_SERVER_PORT}"  # Full server URL

# Script metadata and version information
SCRIPT_NAME="context.sh"                                 # Script name for help and errors
SCRIPT_VERSION="1.0.0"                                   # Version for compatibility tracking
SCRIPT_AUTHOR="Framework0 Context Server Client"         # Attribution for the tool

# Color codes for enhanced output formatting (works on most terminals)
RED='\033[0;31m'      # Error messages and failures
GREEN='\033[0;32m'    # Success messages and confirmations
YELLOW='\033[0;33m'   # Warning messages and info
BLUE='\033[0;34m'     # Information and debug output
CYAN='\033[0;36m'     # Highlighting and emphasis
NC='\033[0m'          # No Color - reset to default

# Global variables for script state and configuration
VERBOSE=false         # Enable verbose output for debugging
QUIET=false          # Suppress non-essential output
TIMEOUT=10           # Default timeout for HTTP requests
FORMAT="auto"        # Output format: auto, json, plain, pretty
DRY_RUN=false        # Preview operations without executing

# Utility functions for common operations and formatting

print_help() {
    # Display comprehensive help information with usage examples
    cat << 'EOF'
Framework0 Context Server Shell Client

USAGE:
    context.sh <command> [options] [arguments]

COMMANDS:
    get <key>                    Get value for specified key from context
    set <key> <value>           Set key to value in context
    list                        List all context keys and values
    history                     Show context change history
    status                      Show server status and connection info
    monitor                     Monitor context changes in real-time
    clear                       Clear all context data (interactive)
    dump [options]              Dump context data to file
    dumps                       List available dump files
    help                        Show this help message

DUMP OPTIONS:
    --dump-format <format>      Dump file format: json, pretty, csv, txt (default: json)
    --filename <name>           Custom filename for dump (optional)
    --include-history           Include change history in dump
    --who <attribution>         Set attribution for dump operation

OPTIONS:
    -h, --host <host>           Context server host (default: localhost)
    -p, --port <port>           Context server port (default: 8080)
    -f, --format <format>       Output format: auto, json, plain, pretty
    -t, --timeout <seconds>     HTTP request timeout (default: 10)
    -v, --verbose               Enable verbose output for debugging
    -q, --quiet                 Suppress non-essential output
    -n, --dry-run              Preview operations without executing
    --who <attribution>         Set attribution for changes (default: shell_client)

ENVIRONMENT VARIABLES:
    CONTEXT_SERVER_HOST         Server host address
    CONTEXT_SERVER_PORT         Server port number
    CONTEXT_CLIENT_TIMEOUT      Default timeout for requests
    CONTEXT_CLIENT_FORMAT       Default output format

EXAMPLES:
    # Basic operations
    context.sh get app.status
    context.sh set app.debug true
    context.sh set user.config '{"theme": "dark", "lang": "en"}'
    
    # List and monitor
    context.sh list
    context.sh monitor
    
    # Different output formats
    context.sh get app.config --format json
    context.sh list --format pretty
    
    # Remote server
    context.sh get status --host production-server --port 9090
    
    # Batch operations with error handling
    context.sh set batch.start "$(date)" && \
    context.sh set batch.status "running" && \
    echo "Batch started successfully"

EXIT CODES:
    0    Success
    1    General error
    2    Invalid arguments
    3    Server connection error
    4    Server error response
    5    Authentication/permission error

EOF
}

log() {
    # Print log message with timestamp and level formatting
    local level="$1"      # Log level: INFO, WARN, ERROR, DEBUG
    local message="$2"    # Message content to log
    
    if [[ "$QUIET" == "true" && "$level" != "ERROR" ]]; then
        return  # Skip non-error messages in quiet mode
    fi
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')  # Current timestamp for log entry
    local color=""        # Color code for the log level
    
    case "$level" in
        "ERROR") color="$RED" ;;      # Red for errors
        "WARN")  color="$YELLOW" ;;   # Yellow for warnings
        "INFO")  color="$GREEN" ;;    # Green for info
        "DEBUG") color="$BLUE" ;;     # Blue for debug
        *)       color="$NC" ;;       # No color for unknown levels
    esac
    
    if [[ "$level" == "DEBUG" && "$VERBOSE" != "true" ]]; then
        return  # Skip debug messages unless verbose mode enabled
    fi
    
    echo -e "${color}[$timestamp] [$level]${NC} $message" >&2  # Output to stderr with color
}

check_dependencies() {
    # Verify that required external tools are available
    local missing_deps=()  # Array to track missing dependencies
    
    # Check for curl (required for HTTP requests)
    if ! command -v curl >/dev/null 2>&1; then
        missing_deps+=("curl")  # Add curl to missing dependencies
    fi
    
    # Check for jq (optional but recommended for JSON processing)
    if ! command -v jq >/dev/null 2>&1; then
        log "WARN" "jq not found - JSON formatting will be limited"
    fi
    
    # Report missing critical dependencies
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log "ERROR" "Missing required dependencies: ${missing_deps[*]}"
        log "ERROR" "Please install missing tools and try again"
        exit 1
    fi
    
    log "DEBUG" "All required dependencies are available"
}

validate_server_connection() {
    # Test connection to context server and verify it's responding
    log "DEBUG" "Testing connection to $CONTEXT_SERVER_URL"
    
    # Attempt to connect to server with short timeout
    if ! curl -s --max-time 3 --connect-timeout 2 "$CONTEXT_SERVER_URL/" >/dev/null 2>&1; then
        log "ERROR" "Cannot connect to context server at $CONTEXT_SERVER_URL"
        log "ERROR" "Please check server is running and address is correct"
        return 3  # Return connection error code
    fi
    
    log "DEBUG" "Server connection successful"
    return 0
}

parse_json_value() {
    # Parse and validate JSON input, handling both objects and primitives
    local input="$1"      # Input value to parse as JSON
    
    # If jq is available, use it for robust JSON parsing
    if command -v jq >/dev/null 2>&1; then
        if echo "$input" | jq . >/dev/null 2>&1; then
            echo "$input"  # Valid JSON, return as-is
            return 0
        fi
    fi
    
    # Fallback: try to detect if input looks like JSON
    if [[ "$input" =~ ^[{[].*[}\]]$ ]] || [[ "$input" =~ ^\".*\"$ ]]; then
        echo "$input"  # Looks like JSON, return as-is
        return 0
    fi
    
    # Not JSON, wrap as string value
    echo "\"$input\""
    return 0
}

format_output() {
    # Format output according to specified format option
    local content="$1"    # Content to format
    local format="$2"     # Desired format: json, pretty, plain, auto
    
    case "$format" in
        "json")
            # Raw JSON output for machine processing
            echo "$content"
            ;;
        "pretty")
            # Pretty-printed JSON with colors if jq available
            if command -v jq >/dev/null 2>&1; then
                echo "$content" | jq -C .  # Colorized pretty JSON
            else
                echo "$content"  # Fallback to raw JSON
            fi
            ;;
        "plain")
            # Extract just the value without JSON formatting
            if command -v jq >/dev/null 2>&1; then
                echo "$content" | jq -r '.value // empty'  # Extract value field
            else
                echo "$content"  # Fallback to raw content
            fi
            ;;
        "auto"|*)
            # Auto-detect best format based on content and terminal
            if [[ -t 1 ]] && command -v jq >/dev/null 2>&1; then
                echo "$content" | jq -C .  # Pretty format for terminal
            else
                echo "$content"  # Raw format for pipes/scripts
            fi
            ;;
    esac
}

make_request() {
    # Make HTTP request to context server with error handling
    local method="$1"     # HTTP method: GET, POST, PUT, DELETE
    local endpoint="$2"   # API endpoint path
    local data="$3"       # Request body data (optional)
    local who="${WHO:-shell_client}"  # Attribution for the request
    
    local url="${CONTEXT_SERVER_URL}${endpoint}"  # Full URL for the request
    local curl_args=()    # Array to build curl arguments
    
    # Build curl command arguments
    curl_args+=("-s")                      # Silent mode (no progress bar)
    curl_args+=("--max-time" "$TIMEOUT")   # Set request timeout
    curl_args+=("-X" "$method")            # Set HTTP method
    curl_args+=("-H" "Content-Type: application/json")  # Set content type
    
    # Add request body for POST/PUT requests
    if [[ -n "$data" ]]; then
        # Wrap data with attribution if not already present
        if [[ "$data" == *'"who"'* ]]; then
            curl_args+=("-d" "$data")  # Data already has attribution
        else
            # Add who field to data
            local attributed_data=$(echo "$data" | jq --arg who "$who" '. + {who: $who}' 2>/dev/null || echo "$data")
            curl_args+=("-d" "$attributed_data")
        fi
    fi
    
    curl_args+=("$url")  # Add URL as final argument
    
    log "DEBUG" "Making $method request to $endpoint"
    
    # Execute request and capture response
    local response
    if response=$(curl "${curl_args[@]}" 2>/dev/null); then
        # Check if response indicates an error status
        if echo "$response" | grep -q '"status":"error"' 2>/dev/null; then
            local error_msg=$(echo "$response" | jq -r '.error // "Unknown server error"' 2>/dev/null || echo "Server error")
            log "ERROR" "Server error: $error_msg"
            return 4  # Server error code
        fi
        
        echo "$response"  # Return successful response
        return 0
    else
        log "ERROR" "Request failed - check server connection"
        return 3  # Connection error code
    fi
}

cmd_get() {
    # Get value for specified key from context server
    local key="$1"        # Context key to retrieve
    
    if [[ -z "$key" ]]; then
        log "ERROR" "Missing required argument: key"
        echo "Usage: $SCRIPT_NAME get <key>" >&2
        return 2  # Invalid arguments error
    fi
    
    log "DEBUG" "Getting value for key: $key"
    
    # Make GET request to retrieve key value
    local response
    if response=$(make_request "GET" "/ctx?key=$(printf '%s' "$key" | sed 's/ /%20/g')"); then
        format_output "$response" "$FORMAT"  # Format and display response
        return 0
    else
        return $?  # Return error code from make_request
    fi
}

cmd_set() {
    # Set key to specified value in context server
    local key="$1"        # Context key to set
    local value="$2"      # Value to assign to key
    
    if [[ -z "$key" || -z "$value" ]]; then
        log "ERROR" "Missing required arguments: key and/or value"
        echo "Usage: $SCRIPT_NAME set <key> <value>" >&2
        return 2  # Invalid arguments error
    fi
    
    log "DEBUG" "Setting key '$key' to value '$value'"
    
    # Parse value as JSON if possible
    local parsed_value
    parsed_value=$(parse_json_value "$value")
    
    # Build request data
    local request_data
    request_data=$(jq -n --arg key "$key" --argjson value "$parsed_value" '{key: $key, value: $value}' 2>/dev/null)
    
    if [[ -z "$request_data" ]]; then
        # Fallback if jq fails
        request_data="{\"key\":\"$key\",\"value\":$parsed_value}"
    fi
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log "INFO" "[DRY RUN] Would set $key = $parsed_value"
        echo "$request_data" | format_output /dev/stdin "$FORMAT"
        return 0
    fi
    
    # Make POST request to set key value
    local response
    if response=$(make_request "POST" "/ctx" "$request_data"); then
        log "INFO" "Successfully set $key"
        format_output "$response" "$FORMAT"  # Format and display response
        return 0
    else
        return $?  # Return error code from make_request
    fi
}

cmd_list() {
    # List all context keys and values from server
    log "DEBUG" "Retrieving all context data"
    
    # Make GET request to retrieve all context data
    local response
    if response=$(make_request "GET" "/ctx/all"); then
        case "$FORMAT" in
            "plain")
                # Extract and display just key-value pairs
                if command -v jq >/dev/null 2>&1; then
                    echo "$response" | jq -r '.context | to_entries[] | "\(.key) = \(.value)"'
                else
                    format_output "$response" "$FORMAT"
                fi
                ;;
            *)
                format_output "$response" "$FORMAT"  # Use standard formatting
                ;;
        esac
        return 0
    else
        return $?  # Return error code from make_request
    fi
}

cmd_history() {
    # Show context change history from server
    log "DEBUG" "Retrieving context change history"
    
    # Make GET request to retrieve change history
    local response
    if response=$(make_request "GET" "/ctx/history"); then
        format_output "$response" "$FORMAT"  # Format and display response
        return 0
    else
        return $?  # Return error code from make_request
    fi
}

cmd_status() {
    # Show server status and connection information
    log "DEBUG" "Checking server status"
    
    echo -e "${CYAN}Context Server Status${NC}"
    echo -e "${CYAN}====================${NC}"
    echo "Server URL: $CONTEXT_SERVER_URL"
    echo "Timeout: ${TIMEOUT}s"
    echo "Format: $FORMAT"
    echo ""
    
    # Test server connection
    if validate_server_connection; then
        echo -e "${GREEN}✓ Server is reachable${NC}"
        
        # Get server statistics
        local response
        if response=$(make_request "GET" "/ctx/all"); then
            if command -v jq >/dev/null 2>&1; then
                local key_count=$(echo "$response" | jq '.context | length' 2>/dev/null || echo "unknown")
                local history_count=$(echo "$response" | jq '.history_count // "unknown"' 2>/dev/null || echo "unknown")
                local client_count=$(echo "$response" | jq '.connected_clients // "unknown"' 2>/dev/null || echo "unknown")
                
                echo "Context Keys: $key_count"
                echo "History Entries: $history_count"
                echo "Connected Clients: $client_count"
            else
                echo "Server Details: (jq required for detailed stats)"
            fi
        else
            echo -e "${YELLOW}⚠ Server reachable but API unavailable${NC}"
        fi
    else
        echo -e "${RED}✗ Server is not reachable${NC}"
        return 3  # Connection error
    fi
}

cmd_monitor() {
    # Monitor context changes in real-time (polling mode)
    log "INFO" "Starting context monitoring (Ctrl+C to stop)"
    echo -e "${CYAN}Monitoring context changes...${NC}"
    
    local last_timestamp=""  # Track last seen timestamp
    
    # Continuous monitoring loop
    while true; do
        local response
        if response=$(make_request "GET" "/ctx/history"); then
            if command -v jq >/dev/null 2>&1; then
                # Get latest changes since last check
                local latest_changes
                if [[ -n "$last_timestamp" ]]; then
                    latest_changes=$(echo "$response" | jq --arg ts "$last_timestamp" '.history[] | select(.timestamp > $ts)')
                else
                    latest_changes=$(echo "$response" | jq '.history[-5:] // .history[]')  # Show last 5 or all
                fi
                
                # Display new changes
                if [[ -n "$latest_changes" && "$latest_changes" != "null" ]]; then
                    echo "$latest_changes" | jq -r '"[\(.timestamp)] \(.who): \(.key) = \(.after)"' 2>/dev/null
                fi
                
                # Update last timestamp
                last_timestamp=$(echo "$response" | jq -r '.history[-1].timestamp // empty' 2>/dev/null)
            else
                echo "$(date): Context updated (jq required for details)"
            fi
        else
            log "WARN" "Failed to fetch updates - retrying in 5 seconds"
        fi
        
        sleep 5  # Poll every 5 seconds
    done
}

cmd_clear() {
    # Clear all context data (interactive confirmation)
    echo -e "${YELLOW}This will clear ALL context data on the server.${NC}"
    echo -n "Are you sure you want to continue? (yes/no): "
    read -r confirmation
    
    if [[ "$confirmation" != "yes" ]]; then
        log "INFO" "Clear operation cancelled"
        return 0
    fi
    
    log "WARN" "Clear operation not yet implemented in server API"
    log "INFO" "This would require additional server endpoint for bulk operations"
    return 1
}

main() {
    # Main entry point - parse arguments and execute commands
    local command=""      # Command to execute
    local args=()         # Arguments for the command
    
    # Parse command-line arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--host)
                CONTEXT_SERVER_HOST="$2"  # Override server host
                CONTEXT_SERVER_URL="http://${CONTEXT_SERVER_HOST}:${CONTEXT_SERVER_PORT}"
                shift 2
                ;;
            -p|--port)
                CONTEXT_SERVER_PORT="$2"  # Override server port
                CONTEXT_SERVER_URL="http://${CONTEXT_SERVER_HOST}:${CONTEXT_SERVER_PORT}"
                shift 2
                ;;
            -f|--format)
                FORMAT="$2"  # Set output format
                shift 2
                ;;
            -t|--timeout)
                TIMEOUT="$2"  # Set request timeout
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true  # Enable verbose output
                shift
                ;;
            -q|--quiet)
                QUIET=true    # Enable quiet mode
                shift
                ;;
            -n|--dry-run)
                DRY_RUN=true  # Enable dry-run mode
                shift
                ;;
            --who)
                WHO="$2"      # Set attribution for changes
                shift 2
                ;;
            help|--help)
                print_help    # Show help and exit
                exit 0
                ;;
            get|set|list|history|status|monitor|clear)
                command="$1"  # Set command to execute
                shift
                args=("$@")   # Remaining arguments for command
                break
                ;;
            *)
                log "ERROR" "Unknown option or command: $1"
                echo "Use '$SCRIPT_NAME help' for usage information" >&2
                exit 2  # Invalid arguments error
                ;;
        esac
    done
    
    # Validate command was provided
    if [[ -z "$command" ]]; then
        log "ERROR" "No command specified"
        echo "Use '$SCRIPT_NAME help' for usage information" >&2
        exit 2  # Invalid arguments error
    fi
    
    # Check dependencies and server connection
    check_dependencies
    
    # Skip connection check for help and status commands
    if [[ "$command" != "status" ]]; then
        validate_server_connection || exit $?
    fi
    
    # Execute requested command
    case "$command" in
        "get")
            cmd_get "${args[@]}"
            ;;
        "set")
            cmd_set "${args[@]}"
            ;;
        "list")
            cmd_list "${args[@]}"
            ;;
        "history")
            cmd_history "${args[@]}"
            ;;
        "status")
            cmd_status "${args[@]}"
            ;;
        "monitor")
            cmd_monitor "${args[@]}"
            ;;
        "clear")
            cmd_clear "${args[@]}"
            ;;
        "dump")
            cmd_dump "${args[@]}"
            ;;
        "dumps")
            cmd_dumps "${args[@]}"
            ;;
        *)
            log "ERROR" "Unknown command: $command"
            exit 2  # Invalid arguments error
            ;;
    esac
}

# Execute main function if script is run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi