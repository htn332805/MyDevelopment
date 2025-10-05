# Framework0 Context Server Examples

This directory contains practical examples demonstrating how to use the Framework0 Context Server for data sharing between shell scripts, Python applications, and Dash dashboards.

## Quick Start

1. **Start the Context Server**:
   ```bash
   ./start_server.sh start
   ```

2. **Run Shell Integration Demo**:
   ```bash
   ./examples/shell_demo.sh
   ```

3. **Run Python Integration Demo**:
   ```bash
   cd /home/hai/hai_vscode/MyDevelopment
   source ~/pyvenv/bin/activate
   python examples/integration_demo.py
   ```

4. **Run Dash Dashboard Demo**:
   ```bash
   cd /home/hai/hai_vscode/MyDevelopment
   source ~/pyvenv/bin/activate
   python examples/dash_demo.py
   ```

## Example Files

### 1. `shell_demo.sh`
Comprehensive shell script demonstration showing:
- System monitoring data collection
- Process monitoring and status reporting
- Configuration management from shell scripts
- Data pipeline coordination
- Alerting and notification systems

**Usage**:
```bash
# Run all examples
./examples/shell_demo.sh

# Run specific example
./examples/shell_demo.sh monitoring
./examples/shell_demo.sh config
./examples/shell_demo.sh alerts
```

### 2. `integration_demo.py`
Advanced Python integration examples featuring:
- Basic context operations (get/set/list)
- Shell script integration testing
- Async WebSocket real-time updates
- Multi-source monitoring simulation
- Configuration management patterns

**Usage**:
```bash
# Run all examples
python examples/integration_demo.py

# Run specific example
python examples/integration_demo.py --example basic
python examples/integration_demo.py --example async
```

### 3. `dash_demo.py`
Interactive Dash web dashboard showing:
- Real-time system metrics visualization
- Configuration status overview
- Context data tables
- Alert monitoring
- Auto-refresh capabilities

**Usage**:
```bash
# Start dashboard on default port 8050
python examples/dash_demo.py

# Custom configuration
python examples/dash_demo.py --context-host localhost --context-port 8080 --dash-port 8051
```

## Integration Workflow

The examples demonstrate a complete integration workflow:

1. **Shell Scripts** (`shell_demo.sh`) collect system data and set configuration
2. **Python Applications** (`integration_demo.py`) process and analyze the data
3. **Dash Dashboard** (`dash_demo.py`) visualizes everything in real-time

All components share data through the Context Server, enabling:
- Cross-platform communication
- Real-time data sharing
- Centralized configuration management
- Event-driven updates

## Data Flow Example

```
Shell Script          Python App           Dash Dashboard
    |                     |                      |
    | Set system metrics  |                      |
    |-------------------->|                      |
    |                     | Process & analyze    |
    |                     |--------------------->|
    |                     |                      | Display charts
    |                     |                      | & real-time data
    | Set alerts          |                      |
    |-------------------->|                      |
    |                     |--------------------->| Show alerts
```

## Environment Variables

Set these environment variables to customize behavior:

```bash
export CONTEXT_SERVER_HOST="localhost"
export CONTEXT_SERVER_PORT="8080"
export ENVIRONMENT="development"
export DEBUG="1"
```

## Monitoring the System

While running examples, you can monitor the system in real-time:

1. **Web Dashboard**: http://localhost:8080 (built-in server dashboard)
2. **Dash Dashboard**: http://localhost:8050 (custom visualization)
3. **Shell Commands**:
   ```bash
   ./tools/context.sh status
   ./tools/context.sh list
   ./tools/context.sh monitor
   ```

## Next Steps

After running the examples:

1. Modify the scripts to add your own data sources
2. Create custom Dash visualizations for your use case
3. Build your own applications using the context client libraries
4. Set up production deployment with Docker

For more information, see the main project documentation and the `src/` directory for client libraries.