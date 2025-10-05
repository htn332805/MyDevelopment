# Framework0 Enhanced Context Server - Integration Patterns

*Generated on 2025-10-05 08:48:13 UTC*

Examples and patterns for integrating with the Framework0 Enhanced Context Server.

## Python Client Integration

### Synchronous Client

```python
from src.context_client import ContextClient

# Initialize client
client = ContextClient(host='127.0.0.1', port=8080)

# Basic operations
client.set('config.database_url', 'postgresql://localhost/mydb', who='setup')
database_url = client.get('config.database_url')
all_config = client.get_all()

# File dumping
dump_result = client.dump_context(
    format='json',
    filename='backup_config',
    include_history=True,
    who='backup_service'
)
```

### Asynchronous Client

```python
import asyncio
from src.context_client import AsyncContextClient

async def async_example():
    client = AsyncContextClient(host='127.0.0.1', port=8080)
    
    # Async operations
    await client.set('status.service_state', 'running', who='monitor')
    state = await client.get('status.service_state')
    
    # Async file dumping
    dumps = await client.list_dumps()
    latest_dump = await client.download_dump(dumps['dump_files'][0]['filename'])

# Run async client
asyncio.run(async_example())
```

## Shell Script Integration

### Basic Commands

```bash
# Set context values
./tools/context.sh set deployment.version 1.2.3 --who deployment_script
./tools/context.sh set config.environment production --who setup

# Get context values
VERSION=$(./tools/context.sh get deployment.version --format plain)
echo "Deploying version: $VERSION"

# List all context
./tools/context.sh list --format json > current_config.json

# Create context dump
./tools/context.sh dump --dump-format csv --filename daily_backup \
    --include-history --who backup_cron
```

### Advanced Shell Integration

```bash
#!/bin/bash
# Deployment script with context integration

CONTEXT_CMD="./tools/context.sh"
DEPLOYMENT_ID=$(date +%Y%m%d_%H%M%S)

# Update deployment context
$CONTEXT_CMD set deployment.id "$DEPLOYMENT_ID" --who deploy_script
$CONTEXT_CMD set deployment.status "starting" --who deploy_script
$CONTEXT_CMD set deployment.timestamp "$(date -Iseconds)" --who deploy_script

# Perform deployment steps
if deploy_application; then
    $CONTEXT_CMD set deployment.status "success" --who deploy_script
    $CONTEXT_CMD dump --dump-format json --filename "deployment_$DEPLOYMENT_ID" \
        --who deploy_script
else
    $CONTEXT_CMD set deployment.status "failed" --who deploy_script
    $CONTEXT_CMD set deployment.error "$?" --who deploy_script
fi
```

## WebSocket Real-time Integration

### Python WebSocket Client

```python
import socketio
import json

# Create WebSocket client
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to context server')
    # Subscribe to context changes
    sio.emit('subscribe', {'keys': ['deployment.*', 'config.*']})

@sio.event
def context_changed(data):
    print(f"Context changed: {data['key']} = {data['new_value']}")
    print(f"Changed by: {data['who']} at {data['timestamp']}")

@sio.event
def context_dump_complete(data):
    print(f"Dump complete: {data['filename']} ({data['file_size']} bytes)")

# Connect to server
sio.connect('http://127.0.0.1:8080')
sio.wait()
```

## Dashboard Integration

### Custom Dash Application

```python
import dash
from dash import dcc, html, callback, Input, Output
from src.dash_integration import DashContextIntegration

# Initialize Dash app with context integration
app = dash.Dash(__name__)
context_integration = DashContextIntegration(
    context_host='127.0.0.1',
    context_port=8080
)

app.layout = html.Div([
    html.H1('Custom Context Dashboard'),
    dcc.Graph(id='context-metrics'),
    dcc.Interval(id='update-interval', interval=5000, n_intervals=0)
])

@callback(
    Output('context-metrics', 'figure'),
    Input('update-interval', 'n_intervals')
)
def update_metrics(n):
    context_data = context_integration.get_all_context()
    # Create custom visualizations from context data
    return create_metrics_chart(context_data)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
```

