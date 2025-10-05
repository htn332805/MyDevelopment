# Framework0 Enterprise Integration Patterns

*Updated on 2025-01-05*

Comprehensive integration patterns for Framework0 enterprise automation ecosystem, covering all major components including recipe orchestration, scriptlet framework, enhanced context server, recipe isolation, performance monitoring, and AI-powered analysis.

## Table of Contents

1. [Recipe Orchestration Integration](#recipe-orchestration-integration)
2. [Scriptlet Framework Integration](#scriptlet-framework-integration)
3. [Enhanced Context Server Integration](#enhanced-context-server-integration)
4. [Recipe Isolation Integration](#recipe-isolation-integration)
5. [Performance Monitoring Integration](#performance-monitoring-integration)
6. [AI Analysis Integration](#ai-analysis-integration)
7. [Cross-Platform Integration](#cross-platform-integration)
8. [Enterprise Deployment Patterns](#enterprise-deployment-patterns)

## Recipe Orchestration Integration

### Embedded Recipe Execution

```python
from orchestrator.runner import EnhancedRecipeRunner
from orchestrator.context import Context

class ApplicationWithFramework0:
    """Application integrating Framework0 recipe orchestration."""
    
    def __init__(self):
        self.context = Context()
        self.runner = EnhancedRecipeRunner(self.context)
        
    def process_data_workflow(self, input_data: dict):
        """Execute data processing using Framework0 recipes."""
        
        # Set input data in context
        self.context.set("workflow.input", input_data, who="application")
        
        # Execute recipe with error handling
        try:
            result = self.runner.run_recipe("workflows/data_processing.yaml")
            
            if result.overall_success:
                # Get processed results
                processed_data = self.context.get("workflow.output")
                return {"success": True, "data": processed_data}
            else:
                return {"success": False, "errors": result.global_errors}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def batch_process_files(self, file_list: list):
        """Batch process multiple files using parallel recipes."""
        
        results = []
        
        for file_path in file_list:
            # Set file-specific context
            self.context.set("batch.current_file", file_path, who="batch_processor")
            
            # Execute file processing recipe
            result = self.runner.run_recipe("workflows/file_processor.yaml")
            results.append({
                "file": file_path,
                "success": result.overall_success,
                "execution_time": result.execution_time_seconds
            })
            
        return results

# Integration example
app = ApplicationWithFramework0()
result = app.process_data_workflow({"source": "/data/input.csv"})
```

### Recipe Template System

```python
from orchestrator.recipe_template import RecipeTemplateEngine

class DynamicRecipeGenerator:
    """Generate recipes dynamically based on application needs."""
    
    def __init__(self):
        self.template_engine = RecipeTemplateEngine()
        
    def create_etl_recipe(self, source_config: dict, target_config: dict) -> str:
        """Generate ETL recipe from configuration."""
        
        template = """
metadata:
  name: "dynamic_etl_{{ timestamp }}"
  version: "1.0"
  description: "Auto-generated ETL pipeline"

steps:
  - name: "extract_data"
    idx: 1
    type: "python"
    module: "scriptlets.extractors"
    function: "{{ extractor_type }}Extractor"
    args:
      source_url: "{{ source_url }}"
      connection_params: {{ source_params }}
      
  - name: "transform_data"
    idx: 2
    type: "python"
    module: "scriptlets.transformers"
    function: "DataTransformerScriptlet"
    depends_on: ["extract_data"]
    args:
      transformation_rules: {{ transform_rules }}
      
  - name: "load_data"
    idx: 3
    type: "python"
    module: "scriptlets.loaders"
    function: "{{ loader_type }}Loader"
    depends_on: ["transform_data"]
    args:
      target_url: "{{ target_url }}"
      load_options: {{ load_options }}
"""
        
        # Render template with configuration
        recipe_yaml = self.template_engine.render(template, {
            "timestamp": int(time.time()),
            "extractor_type": source_config["type"],
            "source_url": source_config["url"],
            "source_params": source_config["params"],
            "transform_rules": source_config.get("transformations", []),
            "loader_type": target_config["type"],
            "target_url": target_config["url"],
            "load_options": target_config.get("options", {})
        })
        
        return recipe_yaml

# Usage
generator = DynamicRecipeGenerator()
recipe = generator.create_etl_recipe(
    source_config={"type": "Database", "url": "postgres://...", "params": {}},
    target_config={"type": "S3", "url": "s3://bucket/", "options": {}}
)
```

## Scriptlet Framework Integration

### Custom Scriptlet Development

```python
from scriptlets.framework import BaseScriptlet, register_scriptlet
from orchestrator.context import Context
from typing import Dict, Any, List
import requests

@register_scriptlet
class APIIntegrationScriptlet(BaseScriptlet):
    """Custom scriptlet for external API integration."""
    
    def __init__(self):
        super().__init__()
        self.name = "api_integration"
        self.version = "1.0"
        self.description = "Integrate with external REST APIs"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API integration with comprehensive error handling."""
        
        try:
            # Extract parameters
            endpoint = params["endpoint"]
            method = params.get("method", "GET")
            headers = params.get("headers", {})
            payload = params.get("payload", {})
            timeout = params.get("timeout", 30)
            
            # Add authentication if provided
            if "auth_token" in params:
                headers["Authorization"] = f"Bearer {params['auth_token']}"
            
            # Make API request
            response = requests.request(
                method=method,
                url=endpoint,
                headers=headers,
                json=payload if method in ["POST", "PUT", "PATCH"] else None,
                timeout=timeout
            )
            
            # Process response
            if response.status_code == 200:
                result_data = response.json() if response.content else {}
                
                # Store results in context
                context.set(f"{self.name}.response", result_data, who=self.name)
                context.set(f"{self.name}.status_code", response.status_code, who=self.name)
                
                return {
                    "status": "success",
                    "data": result_data,
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                error_msg = f"API request failed: {response.status_code} - {response.text}"
                context.set(f"{self.name}.error", error_msg, who=self.name)
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(f"API integration failed: {e}")
            raise

@register_scriptlet
class DatabaseIntegrationScriptlet(BaseScriptlet):
    """Database operations scriptlet with connection pooling."""
    
    def __init__(self):
        super().__init__()
        self.name = "database_integration"
        self.connection_pool = None
        
    def setup(self, context: Context, params: Dict[str, Any]) -> None:
        """Initialize database connection pool."""
        
        connection_string = params["connection_string"]
        pool_size = params.get("pool_size", 5)
        
        # Initialize connection pool based on database type
        if "postgresql" in connection_string:
            import psycopg2.pool
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1, maxconn=pool_size, dsn=connection_string
            )
        elif "mysql" in connection_string:
            import mysql.connector.pooling
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="framework0_pool", pool_size=pool_size, **params["db_config"]
            )
        
        context.set(f"{self.name}.pool_ready", True, who=self.name)
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database operations with transaction support."""
        
        connection = None
        cursor = None
        
        try:
            # Get connection from pool
            connection = self.connection_pool.getconn()
            cursor = connection.cursor()
            
            # Execute query
            query = params["query"]
            query_params = params.get("params", [])
            
            cursor.execute(query, query_params)
            
            # Handle different query types
            if query.strip().upper().startswith("SELECT"):
                # Fetch results for SELECT queries
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                
                # Convert to list of dictionaries
                result_data = [
                    dict(zip(column_names, row)) for row in results
                ]
                
                context.set(f"{self.name}.query_results", result_data, who=self.name)
                
                return {
                    "status": "success",
                    "operation": "select",
                    "row_count": len(result_data),
                    "data": result_data
                }
            else:
                # Handle INSERT/UPDATE/DELETE queries
                connection.commit()
                affected_rows = cursor.rowcount
                
                return {
                    "status": "success", 
                    "operation": "modify",
                    "affected_rows": affected_rows
                }
                
        except Exception as e:
            if connection:
                connection.rollback()
            raise
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.connection_pool.putconn(connection)
                
    def teardown(self, context: Context) -> None:
        """Clean up database connections."""
        if self.connection_pool:
            self.connection_pool.closeall()
```

### Scriptlet Plugin System

```python
from scriptlets.plugin_manager import PluginManager
from pathlib import Path

class CustomScriptletPlugin:
    """Plugin for extending Framework0 with custom scriptlets."""
    
    def __init__(self, plugin_dir: str):
        self.plugin_dir = Path(plugin_dir)
        self.manager = PluginManager()
        
    def load_custom_scriptlets(self):
        """Load custom scriptlets from plugin directory."""
        
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("scriptlet_"):
                # Import custom scriptlet module
                module_name = plugin_file.stem
                spec = importutil.util.spec_from_file_location(module_name, plugin_file)
                module = importutil.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Register scriptlets from module
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (isinstance(item, type) and 
                        issubclass(item, BaseScriptlet) and 
                        item != BaseScriptlet):
                        
                        self.manager.register_scriptlet(item())
                        self.logger.info(f"Loaded custom scriptlet: {item_name}")
    
    def create_scriptlet_template(self, scriptlet_name: str) -> str:
        """Generate template for new custom scriptlet."""
        
        template = f'''
from scriptlets.framework import BaseScriptlet, register_scriptlet
from orchestrator.context import Context
from typing import Dict, Any
from src.core.logger import get_logger
import os

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

@register_scriptlet
class {scriptlet_name}Scriptlet(BaseScriptlet):
    """
    Custom {scriptlet_name.lower()} scriptlet for Framework0.
    
    Add your implementation description here.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.name = "{scriptlet_name.lower()}"
        self.version = "1.0"
        self.description = "Custom {scriptlet_name.lower()} implementation"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute {scriptlet_name.lower()} operations.
        
        Args:
            context: Framework0 context for data sharing
            params: Parameters from recipe
            
        Returns:
            Dict containing execution results
        """
        try:
            logger.info(f"Starting {{self.name}} execution")
            
            # TODO: Implement your scriptlet logic here
            
            # Store results in context
            context.set(f"{{self.name}}.result", {{}}, who=self.name)
            
            logger.info(f"{{self.name}} execution completed successfully")
            
            return {{
                "status": "success",
                "message": f"{{self.name}} executed successfully"
            }}
            
        except Exception as e:
            logger.error(f"{{self.name}} execution failed: {{e}}")
            context.set(f"{{self.name}}.error", str(e), who=self.name)
            raise
'''
        
        return template.strip()

# Usage
plugin_system = CustomScriptletPlugin("plugins/scriptlets")
plugin_system.load_custom_scriptlets()

# Generate template for new scriptlet
template = plugin_system.create_scriptlet_template("DataProcessor")
with open("plugins/scriptlets/scriptlet_data_processor.py", "w") as f:
    f.write(template)
```

## Enhanced Context Server Integration
```

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

