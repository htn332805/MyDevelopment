#!/bin/bash
# Framework0 Context Server - Shell Integration Demo
# 
# This script demonstrates how shell scripts can interact with the Framework0
# Context Server to share data with Python applications and Dash dashboards.
# Shows practical examples of setting system monitoring data, configuration,
# and coordinating between different types of applications.

set -euo pipefail  # Enable strict error handling

# Configuration - can be overridden by environment variables
CONTEXT_SERVER_HOST="${CONTEXT_SERVER_HOST:-localhost}"
CONTEXT_SERVER_PORT="${CONTEXT_SERVER_PORT:-8080}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT_SCRIPT="${SCRIPT_DIR}/../tools/context.sh"

# Colors for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'  
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

log_success() {
    echo -e "${PURPLE}[SUCCESS]${NC} $1"
}

# Check if context server is available
check_server() {
    log_step "Checking context server connection..."
    
    if [[ ! -f "$CONTEXT_SCRIPT" ]]; then
        log_error "Context script not found at: $CONTEXT_SCRIPT"
        return 1
    fi
    
    # Make script executable if needed
    chmod +x "$CONTEXT_SCRIPT"
    
    # Test server connection
    if "$CONTEXT_SCRIPT" status >/dev/null 2>&1; then
        log_success "Connected to context server at ${CONTEXT_SERVER_HOST}:${CONTEXT_SERVER_PORT}"
        return 0
    else
        log_error "Cannot connect to context server!"
        log_info "Make sure the server is running: ./start_server.sh start"
        return 1
    fi
}

# Example 1: System monitoring data
example_system_monitoring() {
    echo
    echo -e "${CYAN}=== EXAMPLE 1: System Monitoring Data ===${NC}"
    
    log_step "Collecting system information..."
    
    # Get system information
    hostname=$(hostname)
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    uptime_info=$(uptime | awk -F'load average:' '{print $2}' | sed 's/^ *//')
    
    # Get CPU usage (simple approach)
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    
    # Get memory usage
    memory_info=$(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}')
    
    # Get disk usage for root filesystem
    disk_usage=$(df -h / | awk 'NR==2{printf "%s", $5}' | sed 's/%//')
    
    log_info "System stats collected:"
    log_info "  Hostname: $hostname"
    log_info "  CPU Usage: ${cpu_usage}%"
    log_info "  Memory Usage: ${memory_info}%"
    log_info "  Disk Usage: ${disk_usage}%"
    
    # Set system monitoring data in context server
    log_step "Setting system monitoring data in context server..."
    
    "$CONTEXT_SCRIPT" set "monitoring.system.hostname" "$hostname"
    "$CONTEXT_SCRIPT" set "monitoring.system.timestamp" "$timestamp"
    "$CONTEXT_SCRIPT" set "monitoring.system.cpu_usage" "$cpu_usage"
    "$CONTEXT_SCRIPT" set "monitoring.system.memory_usage" "$memory_info"
    "$CONTEXT_SCRIPT" set "monitoring.system.disk_usage" "$disk_usage"
    "$CONTEXT_SCRIPT" set "monitoring.system.load_average" "$uptime_info"
    "$CONTEXT_SCRIPT" set "monitoring.system.status" "online"
    
    log_success "System monitoring data stored in context server"
}

# Example 2: Process monitoring
example_process_monitoring() {
    echo
    echo -e "${CYAN}=== EXAMPLE 2: Process Monitoring ===${NC}"
    
    log_step "Monitoring key system processes..."
    
    # List of processes to monitor
    processes=("ssh" "systemd" "bash")
    
    for process in "${processes[@]}"; do
        # Count running processes
        count=$(pgrep -c "$process" 2>/dev/null || echo "0")
        
        # Get memory usage for the process
        if [[ "$count" -gt 0 ]]; then
            memory=$(ps -C "$process" -o pid,pcpu,pmem,comm --no-headers | \
                    awk '{mem+=$3} END {printf "%.1f", mem}')
            status="running"
        else
            memory="0.0"
            status="not_running"
        fi
        
        log_info "Process $process: $count instances, ${memory}% memory"
        
        # Store in context server
        "$CONTEXT_SCRIPT" set "monitoring.processes.${process}.count" "$count"
        "$CONTEXT_SCRIPT" set "monitoring.processes.${process}.memory_usage" "$memory"
        "$CONTEXT_SCRIPT" set "monitoring.processes.${process}.status" "$status"
        "$CONTEXT_SCRIPT" set "monitoring.processes.${process}.last_check" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    done
    
    log_success "Process monitoring data stored"
}

# Example 3: Configuration management
example_configuration() {
    echo
    echo -e "${CYAN}=== EXAMPLE 3: Configuration Management ===${NC}"
    
    log_step "Setting application configuration via shell..."
    
    # Environment-specific configuration
    environment="${ENVIRONMENT:-development}"
    
    # Application configuration
    "$CONTEXT_SCRIPT" set "config.shell_app.environment" "$environment"
    "$CONTEXT_SCRIPT" set "config.shell_app.version" "1.2.3"
    "$CONTEXT_SCRIPT" set "config.shell_app.debug" "true"
    "$CONTEXT_SCRIPT" set "config.shell_app.log_level" "INFO"
    "$CONTEXT_SCRIPT" set "config.shell_app.max_workers" "4"
    
    # Feature flags
    "$CONTEXT_SCRIPT" set "config.shell_app.features.monitoring" "enabled"
    "$CONTEXT_SCRIPT" set "config.shell_app.features.metrics" "enabled"
    "$CONTEXT_SCRIPT" set "config.shell_app.features.alerts" "disabled"
    
    # Database configuration (example)
    "$CONTEXT_SCRIPT" set "config.database.host" "localhost"
    "$CONTEXT_SCRIPT" set "config.database.port" "5432"
    "$CONTEXT_SCRIPT" set "config.database.name" "framework0"
    "$CONTEXT_SCRIPT" set "config.database.pool_size" "10"
    
    log_success "Application configuration stored"
    
    # Demonstrate reading configuration
    log_step "Reading configuration from context server..."
    
    app_version=$("$CONTEXT_SCRIPT" get "config.shell_app.version" --format plain)
    db_host=$("$CONTEXT_SCRIPT" get "config.database.host" --format plain)
    monitoring_enabled=$("$CONTEXT_SCRIPT" get "config.shell_app.features.monitoring" --format plain)
    
    log_info "Retrieved configuration:"
    log_info "  App Version: $app_version"
    log_info "  Database Host: $db_host"
    log_info "  Monitoring: $monitoring_enabled"
}

# Example 4: Data pipeline coordination
example_data_pipeline() {
    echo
    echo -e "${CYAN}=== EXAMPLE 4: Data Pipeline Coordination ===${NC}"
    
    log_step "Simulating data pipeline with shell coordination..."
    
    pipeline_id="shell_pipeline_$(date +%s)"
    
    # Initialize pipeline status
    "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.status" "initializing"
    "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.start_time" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.stage" "data_collection"
    "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.progress" "0"
    
    log_info "Pipeline $pipeline_id initialized"
    
    # Simulate pipeline stages
    stages=("data_collection" "data_processing" "data_validation" "data_storage")
    
    for i in "${!stages[@]}"; do
        stage="${stages[$i]}"
        progress=$(( (i + 1) * 25 ))
        
        log_step "Processing stage: $stage"
        
        # Update pipeline status
        "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.status" "running"
        "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.stage" "$stage"
        "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.progress" "$progress"
        "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.last_update" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        
        # Simulate work
        sleep 1
        
        log_info "Stage $stage completed (${progress}%)"
    done
    
    # Mark pipeline as completed
    "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.status" "completed"
    "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.end_time" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    "$CONTEXT_SCRIPT" set "pipeline.${pipeline_id}.progress" "100"
    
    log_success "Pipeline $pipeline_id completed successfully"
}

# Example 5: Alerting and notifications
example_alerting() {
    echo
    echo -e "${CYAN}=== EXAMPLE 5: Alerting System ===${NC}"
    
    log_step "Generating system alerts..."
    
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Simulate different types of alerts
    alerts=(
        "system:disk_space:WARNING:Disk usage above 85%"
        "application:response_time:INFO:Average response time increased"
        "security:login_attempt:WARNING:Multiple failed login attempts detected"
        "performance:memory:ERROR:Memory usage critical - above 95%"
    )
    
    for alert in "${alerts[@]}"; do
        IFS=':' read -ra ALERT_PARTS <<< "$alert"
        category="${ALERT_PARTS[0]}"
        type="${ALERT_PARTS[1]}"
        severity="${ALERT_PARTS[2]}"
        message="${ALERT_PARTS[3]}"
        
        alert_id="alert_$(date +%s)_$$"
        
        # Store alert in context server
        "$CONTEXT_SCRIPT" set "alerts.${alert_id}.category" "$category"
        "$CONTEXT_SCRIPT" set "alerts.${alert_id}.type" "$type"
        "$CONTEXT_SCRIPT" set "alerts.${alert_id}.severity" "$severity"
        "$CONTEXT_SCRIPT" set "alerts.${alert_id}.message" "$message"
        "$CONTEXT_SCRIPT" set "alerts.${alert_id}.timestamp" "$timestamp"
        "$CONTEXT_SCRIPT" set "alerts.${alert_id}.acknowledged" "false"
        "$CONTEXT_SCRIPT" set "alerts.${alert_id}.source" "shell_monitor"
        
        case "$severity" in
            "ERROR")   log_error "ALERT: $message" ;;
            "WARNING") log_warn "ALERT: $message" ;;
            "INFO")    log_info "ALERT: $message" ;;
        esac
    done
    
    log_success "Alerts generated and stored in context server"
}

# Show current context data
show_context_summary() {
    echo
    echo -e "${CYAN}=== CONTEXT SUMMARY ===${NC}"
    
    log_step "Retrieving all context data..."
    
    # Get all data and filter for our examples
    if "$CONTEXT_SCRIPT" list --format json >/dev/null 2>&1; then
        # Use JSON format if available
        total_keys=$("$CONTEXT_SCRIPT" list --format json | jq '. | length' 2>/dev/null || echo "unknown")
    else
        # Fallback to plain format
        total_keys=$("$CONTEXT_SCRIPT" list --format plain | wc -l)
    fi
    
    log_info "Total context keys: $total_keys"
    
    # Show some example data
    log_step "Sample context data:"
    
    # Try to get some example values
    example_keys=(
        "monitoring.system.hostname"
        "config.shell_app.version"  
        "monitoring.system.status"
    )
    
    for key in "${example_keys[@]}"; do
        if value=$("$CONTEXT_SCRIPT" get "$key" --format plain 2>/dev/null); then
            log_info "  $key: $value"
        fi
    done
}

# Main function
main() {
    echo -e "${PURPLE}🐚 Framework0 Context Server - Shell Integration Demo${NC}"
    echo "=================================================================="
    
    # Check command line arguments
    case "${1:-all}" in
        "monitoring")
            check_server && example_system_monitoring
            ;;
        "processes")
            check_server && example_process_monitoring
            ;;
        "config")
            check_server && example_configuration
            ;;
        "pipeline")
            check_server && example_data_pipeline
            ;;
        "alerts")
            check_server && example_alerting
            ;;
        "summary")
            check_server && show_context_summary
            ;;
        "all"|*)
            if check_server; then
                example_system_monitoring
                example_process_monitoring
                example_configuration
                example_data_pipeline
                example_alerting
                show_context_summary
                
                echo
                echo -e "${PURPLE}🎉 All shell integration examples completed!${NC}"
                echo "=================================================================="
                echo -e "${GREEN}📊 View the data in real-time:${NC}"
                echo -e "   🌐 Dashboard: http://${CONTEXT_SERVER_HOST}:${CONTEXT_SERVER_PORT}"
                echo -e "   🔍 List data: $CONTEXT_SCRIPT list"
                echo -e "   📈 Monitor: $CONTEXT_SCRIPT monitor"
            fi
            ;;
    esac
}

# Show usage if requested
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "Usage: $0 [example]"
    echo
    echo "Examples:"
    echo "  monitoring  - System monitoring data collection"
    echo "  processes   - Process monitoring and status"
    echo "  config      - Configuration management"
    echo "  pipeline    - Data pipeline coordination"
    echo "  alerts      - Alerting and notification system"
    echo "  summary     - Show context data summary"
    echo "  all         - Run all examples (default)"
    echo
    echo "Environment Variables:"
    echo "  CONTEXT_SERVER_HOST - Server hostname (default: localhost)"
    echo "  CONTEXT_SERVER_PORT - Server port (default: 8080)"
    echo "  ENVIRONMENT         - Environment name (default: development)"
    exit 0
fi

# Run main function
main "$@"