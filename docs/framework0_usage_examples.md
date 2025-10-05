# Framework0 Complete Usage Examples and Scenarios

This comprehensive guide provides practical examples for all Framework0 features and capabilities, including real-world scenarios, integration patterns, and advanced use cases.

**Last Updated:** 2025-01-05  
**Framework Version:** 2.0.0-enhanced

## Table of Contents

1. [Recipe Creation and Execution](#recipe-creation-and-execution)
2. [Scriptlet Development](#scriptlet-development)  
3. [Context Management](#context-management)
4. [Recipe Isolation and Deployment](#recipe-isolation-and-deployment)
5. [Performance Monitoring](#performance-monitoring)
6. [AI-Powered Analysis](#ai-powered-analysis)
7. [Visualization](#visualization)
8. [Enhanced Context Server](#enhanced-context-server)
9. [Integration Patterns](#integration-patterns)
10. [Production Scenarios](#production-scenarios)

## Recipe Creation and Execution

### Basic Recipe Structure

```yaml
# basic_data_processing.yaml
metadata:
  name: "basic_data_processing"
  version: "1.0"
  description: "Process CSV data with validation and analysis"
  author: "Framework0 Team"
  tags: ["data", "processing", "analytics"]

steps:
  - name: "load_data"
    idx: 1
    type: "python"
    module: "scriptlets.data_loaders"
    function: "CSVLoaderScriptlet"
    args:
      file_path: "/data/input.csv"
      encoding: "utf-8"
    timeout: 30
    
  - name: "validate_data"
    idx: 2
    type: "python"
    module: "scriptlets.validators"
    function: "DataValidatorScriptlet"
    depends_on: ["load_data"]
    args:
      validation_rules: ["non_null", "type_check"]
    
  - name: "analyze_data"
    idx: 3
    type: "python"
    module: "scriptlets.analyzers"
    function: "StatisticalAnalyzerScriptlet"
    depends_on: ["validate_data"]
    args:
      metrics: ["mean", "median", "std"]
      
  - name: "generate_report"
    idx: 4
    type: "python"
    module: "scriptlets.reporters"
    function: "ReportGeneratorScriptlet"
    depends_on: ["analyze_data"]
    args:
      output_format: "html"
      template: "analytics_report"
```

### Advanced Recipe with Parallel Execution

```yaml
# parallel_data_pipeline.yaml
metadata:
  name: "parallel_data_pipeline"
  version: "2.0"
  description: "Parallel data processing with error handling"
  
steps:
  - name: "setup_environment"
    idx: 1
    type: "python"
    module: "scriptlets.setup"
    function: "EnvironmentSetupScriptlet"
    
  - name: "load_dataset_a"
    idx: 2
    type: "python"
    module: "scriptlets.loaders"
    function: "DatasetLoaderScriptlet"
    depends_on: ["setup_environment"]
    args:
      dataset_id: "dataset_a"
      source: "/data/sources/a/"
      
  - name: "load_dataset_b"
    idx: 3
    type: "python"
    module: "scriptlets.loaders"  
    function: "DatasetLoaderScriptlet"
    depends_on: ["setup_environment"]
    args:
      dataset_id: "dataset_b"
      source: "/data/sources/b/"
      
  - name: "process_dataset_a"
    idx: 4
    type: "python"
    module: "scriptlets.processors"
    function: "DataProcessorScriptlet"
    depends_on: ["load_dataset_a"]
    parallel: true
    args:
      processing_type: "transform"
      
  - name: "process_dataset_b"
    idx: 5
    type: "python"
    module: "scriptlets.processors"
    function: "DataProcessorScriptlet"
    depends_on: ["load_dataset_b"]
    parallel: true
    args:
      processing_type: "transform"
      
  - name: "merge_results"
    idx: 6
    type: "python"
    module: "scriptlets.mergers"
    function: "DataMergerScriptlet"
    depends_on: ["process_dataset_a", "process_dataset_b"]
    args:
      merge_strategy: "inner_join"
      key_columns: ["id", "timestamp"]
```

### Executing Recipes

```python
from orchestrator.runner import EnhancedRecipeRunner
from orchestrator.context import Context

# Create enhanced runner with context
context = Context()
runner = EnhancedRecipeRunner(context)

# Execute recipe with monitoring
try:
    print("🚀 Starting recipe execution...")
    result = runner.run_recipe("basic_data_processing.yaml")
    
    # Check execution results
    if result.overall_success:
        print(f"✅ Recipe completed successfully!")
        print(f"📊 Execution time: {result.execution_time_seconds:.2f}s")
        print(f"📈 Steps completed: {len(result.step_results)}")
        
        # Access results from context
        processed_data = context.get("analyze_data.result")
        report_path = context.get("generate_report.output_path")
        
        print(f"📄 Report generated: {report_path}")
        print(f"📊 Analysis results: {processed_data}")
        
    else:
        print(f"❌ Recipe execution failed")
        print(f"💥 Failed steps: {result.failed_step_count}")
        for error in result.global_errors:
            print(f"   • {error}")
            
except Exception as e:
    print(f"💥 Recipe execution error: {e}")
```

### CLI Execution

```bash
# Basic execution
python orchestrator/runner.py --recipe basic_data_processing.yaml --debug

# Advanced execution with options
python orchestrator/runner.py \
    --recipe parallel_data_pipeline.yaml \
    --only setup_environment,load_dataset_a \
    --continue-on-error \
    --max-retries 3 \
    --step-timeout 60 \
    --json-output

# Execute with specific steps
python orchestrator/runner.py \
    --recipe basic_data_processing.yaml \
    --skip validate_data \
    --debug
```

## Scriptlet Development

### Basic Scriptlet Template

```python
from scriptlets.framework import BaseScriptlet, register_scriptlet
from orchestrator.context import Context
from typing import Dict, Any, Optional
from src.core.logger import get_logger
import os

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

@register_scriptlet
class DataProcessorScriptlet(BaseScriptlet):
    """
    Data processing scriptlet with context integration and error handling.
    
    This scriptlet demonstrates best practices for Framework0 scriptlet
    development including type safety, logging, and context management.
    """
    
    def __init__(self) -> None:
        """Initialize data processor scriptlet."""
        super().__init__()
        self.name = "data_processor"
        self.version = "1.0"
        self.description = "Process data with validation and transformation"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute data processing with comprehensive error handling.
        
        Args:
            context: Framework0 context for data sharing
            params: Processing parameters from recipe
            
        Returns:
            Dict containing processing results and metadata
        """
        try:
            logger.info(f"Starting data processing: {self.name}")
            
            # Extract parameters with defaults
            input_data = params.get("input_data", [])
            processing_type = params.get("processing_type", "transform")
            validation_enabled = params.get("validate", True)
            
            # Validate inputs
            if validation_enabled:
                self._validate_inputs(input_data, processing_type)
            
            # Process data based on type
            if processing_type == "transform":
                result = self._transform_data(input_data)
            elif processing_type == "aggregate":
                result = self._aggregate_data(input_data)
            elif processing_type == "filter":
                result = self._filter_data(input_data, params.get("filter_criteria", {}))
            else:
                raise ValueError(f"Unknown processing type: {processing_type}")
            
            # Store results in context
            context.set(f"{self.name}.result", result, who=self.name)
            context.set(f"{self.name}.metadata", {
                "processing_type": processing_type,
                "input_count": len(input_data),
                "output_count": len(result) if isinstance(result, list) else 1,
                "execution_time": self.get_execution_time()
            }, who=self.name)
            
            logger.info(f"✅ Data processing completed: {len(result) if isinstance(result, list) else 1} records")
            
            return {
                "status": "success",
                "processed_records": len(result) if isinstance(result, list) else 1,
                "processing_type": processing_type,
                "execution_time": self.get_execution_time()
            }
            
        except Exception as e:
            logger.error(f"❌ Data processing failed: {e}")
            context.set(f"{self.name}.error", str(e), who=self.name)
            raise
            
    def _validate_inputs(self, data: Any, processing_type: str) -> None:
        """Validate input data and parameters."""
        if not isinstance(data, list):
            raise ValueError("Input data must be a list")
            
        if not data:
            raise ValueError("Input data cannot be empty")
            
        if processing_type not in ["transform", "aggregate", "filter"]:
            raise ValueError(f"Invalid processing type: {processing_type}")
            
    def _transform_data(self, data: list) -> list:
        """Transform data with processing logic."""
        return [self._transform_record(record) for record in data]
        
    def _transform_record(self, record: Any) -> Any:
        """Transform individual record."""
        if isinstance(record, dict):
            # Transform dictionary records
            return {
                **record,
                "processed": True,
                "processing_timestamp": self.get_current_timestamp()
            }
        else:
            # Transform simple values
            return {"value": record, "processed": True}
            
    def _aggregate_data(self, data: list) -> dict:
        """Aggregate data into summary statistics."""
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        
        return {
            "total_records": len(data),
            "numeric_records": len(numeric_data),
            "sum": sum(numeric_data) if numeric_data else 0,
            "mean": sum(numeric_data) / len(numeric_data) if numeric_data else 0,
            "min": min(numeric_data) if numeric_data else None,
            "max": max(numeric_data) if numeric_data else None
        }
        
    def _filter_data(self, data: list, criteria: dict) -> list:
        """Filter data based on criteria."""
        if not criteria:
            return data
            
        filtered = []
        for item in data:
            if self._meets_criteria(item, criteria):
                filtered.append(item)
                
        return filtered
        
    def _meets_criteria(self, item: Any, criteria: dict) -> bool:
        """Check if item meets filtering criteria."""
        for key, value in criteria.items():
            if isinstance(item, dict):
                if item.get(key) != value:
                    return False
            else:
                # For non-dict items, apply simple equality
                if item != value:
                    return False
        return True
```

### Advanced Scriptlet with Resource Management

```python
@register_scriptlet
class DatabaseProcessorScriptlet(BaseScriptlet):
    """
    Database processing scriptlet with connection pooling and transactions.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.name = "database_processor"
        self.version = "2.0"
        self.connection_pool = None
        
    def setup(self, context: Context, params: Dict[str, Any]) -> None:
        """Setup database connections and resources."""
        try:
            connection_string = params.get("connection_string")
            pool_size = params.get("pool_size", 5)
            
            # Initialize connection pool
            self.connection_pool = self._create_connection_pool(
                connection_string, pool_size
            )
            
            context.set(f"{self.name}.connection_ready", True, who=self.name)
            logger.info(f"Database connection pool initialized: {pool_size} connections")
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            raise
            
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database operations with transaction management."""
        connection = None
        try:
            # Get database connection
            connection = self.connection_pool.get_connection()
            
            # Start transaction
            connection.begin()
            
            # Execute SQL operations
            query = params.get("query")
            query_params = params.get("query_params", {})
            
            result = connection.execute(query, query_params)
            
            # Process results
            processed_results = self._process_db_results(result)
            
            # Commit transaction
            connection.commit()
            
            # Store results
            context.set(f"{self.name}.query_result", processed_results, who=self.name)
            
            return {
                "status": "success",
                "records_processed": len(processed_results),
                "query_executed": query
            }
            
        except Exception as e:
            # Rollback on error
            if connection:
                connection.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
            
        finally:
            # Return connection to pool
            if connection:
                self.connection_pool.return_connection(connection)
                
    def teardown(self, context: Context) -> None:
        """Clean up database resources."""
        if self.connection_pool:
            self.connection_pool.close_all()
            logger.info("Database connection pool closed")
            
    def _create_connection_pool(self, connection_string: str, pool_size: int):
        """Create database connection pool."""
        # Implementation depends on database type
        pass
        
    def _process_db_results(self, result) -> list:
        """Process database query results."""
        # Convert results to list of dictionaries
        pass
```

### Scriptlet Testing

```python
import unittest
from unittest.mock import Mock, patch
from orchestrator.context import Context

class TestDataProcessorScriptlet(unittest.TestCase):
    """Test cases for DataProcessorScriptlet."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.scriptlet = DataProcessorScriptlet()
        self.context = Context()
        
    def test_transform_processing(self) -> None:
        """Test data transformation processing."""
        # Prepare test data
        params = {
            "input_data": [1, 2, 3, 4, 5],
            "processing_type": "transform",
            "validate": True
        }
        
        # Execute scriptlet
        result = self.scriptlet.run(self.context, params)
        
        # Verify results
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["processed_records"], 5)
        
        # Check context data
        processed_data = self.context.get("data_processor.result")
        self.assertIsNotNone(processed_data)
        self.assertEqual(len(processed_data), 5)
        
    def test_aggregate_processing(self) -> None:
        """Test data aggregation processing."""
        params = {
            "input_data": [10, 20, 30, 40, 50],
            "processing_type": "aggregate"
        }
        
        result = self.scriptlet.run(self.context, params)
        
        # Verify aggregation results
        aggregated = self.context.get("data_processor.result")
        self.assertEqual(aggregated["total_records"], 5)
        self.assertEqual(aggregated["sum"], 150)
        self.assertEqual(aggregated["mean"], 30)
        
    def test_invalid_input_validation(self) -> None:
        """Test input validation error handling."""
        params = {
            "input_data": "invalid",  # Should be list
            "processing_type": "transform"
        }
        
        with self.assertRaises(ValueError):
            self.scriptlet.run(self.context, params)

if __name__ == "__main__":
    unittest.main()
```

## Context Management

### Basic Context Operations

```python
from orchestrator.context import Context

# Initialize context
context = Context()

# Basic data storage and retrieval
context.set("user.name", "John Doe", who="user_service")
context.set("user.email", "john@example.com", who="user_service")
context.set("session.id", "sess_12345", who="session_manager")

# Retrieve data
user_name = context.get("user.name")
session_id = context.get("session.id", default="no_session")

print(f"User: {user_name}, Session: {session_id}")

# Check data existence
if context.contains("user.preferences"):
    preferences = context.get("user.preferences")
else:
    # Set default preferences
    context.set("user.preferences", {"theme": "dark", "lang": "en"}, who="ui")
```

### Advanced Context Features

```python
# Context with hierarchical data
context.set("app.database.host", "localhost", who="config")
context.set("app.database.port", 5432, who="config")
context.set("app.database.name", "myapp_prod", who="config")

# Bulk operations
database_config = {
    "app.database.user": "dbuser",
    "app.database.password": "secure_pass",
    "app.database.ssl": True
}

for key, value in database_config.items():
    context.set(key, value, who="config_loader")

# Pattern-based retrieval
db_settings = {}
for key in context.keys():
    if key.startswith("app.database."):
        db_settings[key.split(".")[-1]] = context.get(key)

print(f"Database config: {db_settings}")

# Context history and tracking
history = context.get_history()
print(f"Context operations: {len(history)}")

for entry in history[-5:]:  # Last 5 operations
    print(f"  {entry['timestamp']}: {entry['operation']} by {entry['who']}")
```

### Context with Scriptlet Integration

```python
@register_scriptlet
class ConfigurationManagerScriptlet(BaseScriptlet):
    """Manage application configuration through context."""
    
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """Load and validate configuration."""
        config_file = params.get("config_file", "config.json")
        
        # Load configuration
        config_data = self._load_config_file(config_file)
        
        # Store in context with namespace
        for section, values in config_data.items():
            for key, value in values.items():
                context_key = f"config.{section}.{key}"
                context.set(context_key, value, who=self.name)
        
        # Validate required settings
        required_keys = params.get("required_keys", [])
        missing_keys = []
        
        for key in required_keys:
            if not context.contains(f"config.{key}"):
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Missing required configuration: {missing_keys}")
        
        # Store validation status
        context.set("config.validated", True, who=self.name)
        context.set("config.validation_time", self.get_current_timestamp(), who=self.name)
        
        return {
            "status": "success",
            "sections_loaded": len(config_data),
            "total_settings": sum(len(v) for v in config_data.values()),
            "missing_keys": missing_keys
        }
    
    def _load_config_file(self, file_path: str) -> dict:
        """Load configuration from file."""
        import json
        with open(file_path, 'r') as f:
            return json.load(f)
```

## Recipe Isolation and Deployment

### Basic Recipe Isolation

```python
from tools.recipe_isolation_cli import Framework0RecipeCliV2

# Initialize CLI
cli = Framework0RecipeCliV2()

# Analyze recipe dependencies
print("🔍 Analyzing recipe dependencies...")
analysis = cli.analyze_recipe_dependencies("orchestrator/recipes/data_processing.yaml")

if analysis.success:
    print(f"✅ Analysis completed in {analysis.analysis_time:.2f}s")
    print(f"📦 Dependencies found: {len(analysis.dependencies)}")
    print(f"🏗️ Framework directories: {len(analysis.framework_dirs)}")
    print(f"📁 Required files: {len(analysis.required_files)}")
    
    # List dependencies
    print("\n📋 Dependencies:")
    for dep in analysis.dependencies:
        print(f"  • {dep}")
        
    # List framework infrastructure
    print("\n🔧 Framework Infrastructure:")
    for dir_name in analysis.framework_dirs:
        print(f"  • {dir_name}")
        
else:
    print("❌ Analysis failed:")
    for error in analysis.errors:
        print(f"  • {error}")
```

### Creating Deployment Packages

```bash
# CLI Usage Examples

# 1. Simple package creation
python tools/recipe_isolation_cli.py create orchestrator/recipes/example.yaml

# 2. Custom output directory
python tools/recipe_isolation_cli.py create orchestrator/recipes/example.yaml --output /deploy/packages

# 3. Complete workflow (analyze + create + validate)
python tools/recipe_isolation_cli.py workflow orchestrator/recipes/example.yaml

# 4. Minimal dependency package
python tools/recipe_isolation_cli.py minimal orchestrator/recipes/example.yaml --target /deploy/minimal

# 5. List available recipes
python tools/recipe_isolation_cli.py list --directory orchestrator/recipes

# 6. Validate existing package
python tools/recipe_isolation_cli.py validate isolated_recipe/example_numbers

# 7. Clean up packages
python tools/recipe_isolation_cli.py clean --confirm
```

### Programmatic Package Creation

```python
import glob
from pathlib import Path

# Batch process recipes for deployment
cli = Framework0RecipeCliV2()
recipes_dir = Path("orchestrator/recipes")
deploy_dir = Path("/deploy/packages")

print("🚀 Starting batch recipe isolation...")

processed_recipes = []
failed_recipes = []

for recipe_file in recipes_dir.glob("*.yaml"):
    try:
        print(f"\n📋 Processing: {recipe_file.name}")
        
        # Create isolated package
        package_dir = cli.create_isolated_package(
            str(recipe_file), 
            str(deploy_dir)
        )
        
        # Validate package
        validation = cli.validate_isolated_package(package_dir)
        
        if validation["success"]:
            processed_recipes.append({
                "recipe": recipe_file.name,
                "package": package_dir,
                "status": "ready"
            })
            print(f"✅ {recipe_file.name} -> Package ready")
        else:
            failed_recipes.append({
                "recipe": recipe_file.name,
                "errors": validation["errors"]
            })
            print(f"❌ {recipe_file.name} -> Validation failed")
            
    except Exception as e:
        failed_recipes.append({
            "recipe": recipe_file.name,
            "errors": [str(e)]
        })
        print(f"💥 {recipe_file.name} -> Error: {e}")

# Summary report
print(f"\n📊 Batch Processing Complete")
print(f"✅ Successful: {len(processed_recipes)}")
print(f"❌ Failed: {len(failed_recipes)}")

if processed_recipes:
    print(f"\n📦 Ready for deployment:")
    for recipe in processed_recipes:
        print(f"  • {recipe['recipe']} -> {recipe['package']}")

if failed_recipes:
    print(f"\n💥 Failed recipes:")
    for recipe in failed_recipes:
        print(f"  • {recipe['recipe']}: {recipe['errors'][0]}")
```

### Deployment Validation

```python
def validate_deployment_environment(package_dir: str) -> dict:
    """Comprehensive deployment validation."""
    
    validation_results = {
        "package_structure": False,
        "recipe_syntax": False,
        "dependencies": False,
        "execution_test": False,
        "errors": [],
        "warnings": []
    }
    
    try:
        # 1. Package structure validation
        required_files = ["run_recipe.py", "package_manifest.json"]
        package_path = Path(package_dir)
        
        for required_file in required_files:
            if not (package_path / required_file).exists():
                validation_results["errors"].append(f"Missing required file: {required_file}")
            else:
                validation_results["package_structure"] = True
        
        # 2. Recipe syntax validation
        recipe_files = list(package_path.glob("*.yaml")) + list(package_path.glob("*.yml"))
        
        if not recipe_files:
            validation_results["errors"].append("No recipe files found")
        else:
            import yaml
            try:
                for recipe_file in recipe_files:
                    with open(recipe_file, 'r') as f:
                        yaml.safe_load(f)
                validation_results["recipe_syntax"] = True
            except yaml.YAMLError as e:
                validation_results["errors"].append(f"Recipe syntax error: {e}")
        
        # 3. Dependency validation
        if (package_path / "orchestrator").exists():
            validation_results["dependencies"] = True
        else:
            validation_results["errors"].append("Missing Framework0 infrastructure")
        
        # 4. Basic execution test
        startup_script = package_path / "run_recipe.py"
        if startup_script.exists():
            try:
                # Test script compilation
                with open(startup_script, 'r') as f:
                    compile(f.read(), str(startup_script), 'exec')
                validation_results["execution_test"] = True
            except SyntaxError as e:
                validation_results["errors"].append(f"Startup script syntax error: {e}")
        
        # Overall validation status
        all_passed = all([
            validation_results["package_structure"],
            validation_results["recipe_syntax"], 
            validation_results["dependencies"],
            validation_results["execution_test"]
        ])
        
        validation_results["overall_success"] = all_passed
        
        return validation_results
        
    except Exception as e:
        validation_results["errors"].append(f"Validation error: {e}")
        return validation_results

# Usage
package_dir = "isolated_recipe/data_processing"
results = validate_deployment_environment(package_dir)

if results["overall_success"]:
    print("✅ Package ready for deployment")
else:
    print("❌ Deployment validation failed:")
    for error in results["errors"]:
        print(f"  • {error}")
```

## Performance Monitoring

### Basic Performance Tracking

```python
from src.analysis.framework import PerformanceMonitor
from orchestrator.context import Context
import time

# Initialize performance monitor
context = Context()
monitor = PerformanceMonitor(context)

# Track operation performance
@monitor.track_performance
def data_processing_operation(data: list) -> list:
    """Example operation with performance tracking."""
    time.sleep(0.1)  # Simulate processing time
    return [x * 2 for x in data]

# Execute tracked operation
test_data = list(range(1000))
result = data_processing_operation(test_data)

# Get performance metrics
metrics = monitor.get_metrics("data_processing_operation")
print(f"Operation metrics: {metrics}")

# Performance statistics
stats = monitor.get_performance_statistics()
print(f"Average execution time: {stats['avg_execution_time']:.3f}s")
print(f"Total operations: {stats['total_operations']}")
```

### Advanced Performance Analysis

```python
from src.visualization.performance_dashboard import PerformanceDashboard
from src.analysis.enhanced_framework import EnhancedAnalyzer

class PerformanceAnalyzer:
    """Comprehensive performance analysis for Framework0 operations."""
    
    def __init__(self, context: Context):
        self.context = context
        self.monitor = PerformanceMonitor(context)
        self.dashboard = PerformanceDashboard(context)
        self.analyzer = EnhancedAnalyzer(context)
        
    def analyze_recipe_performance(self, recipe_path: str) -> dict:
        """Analyze recipe execution performance."""
        
        # Execute recipe with monitoring
        from orchestrator.runner import EnhancedRecipeRunner
        
        runner = EnhancedRecipeRunner(self.context)
        
        start_time = time.time()
        result = runner.run_recipe(recipe_path)
        total_time = time.time() - start_time
        
        # Collect performance data
        performance_data = {
            "total_execution_time": total_time,
            "successful_steps": len([s for s in result.step_results if s.success]),
            "failed_steps": len([s for s in result.step_results if not s.success]),
            "step_timings": [],
            "memory_usage": self._get_memory_usage(),
            "cpu_utilization": self._get_cpu_usage()
        }
        
        # Analyze individual step performance
        for step_result in result.step_results:
            step_timing = {
                "step_name": step_result.step_name,
                "execution_time": step_result.execution_time,
                "status": "success" if step_result.success else "failed",
                "memory_delta": step_result.memory_usage if hasattr(step_result, 'memory_usage') else 0
            }
            performance_data["step_timings"].append(step_timing)
        
        # Generate performance insights
        insights = self._generate_performance_insights(performance_data)
        performance_data["insights"] = insights
        
        # Store analysis results
        self.context.set("performance.analysis", performance_data, who="performance_analyzer")
        
        return performance_data
    
    def create_performance_report(self, analysis_data: dict) -> str:
        """Generate comprehensive performance report."""
        
        report_lines = [
            "# Recipe Performance Analysis Report",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Executive Summary",
            f"- Total execution time: {analysis_data['total_execution_time']:.2f}s",
            f"- Successful steps: {analysis_data['successful_steps']}",
            f"- Failed steps: {analysis_data['failed_steps']}",
            f"- Memory usage: {analysis_data['memory_usage']} MB",
            f"- CPU utilization: {analysis_data['cpu_utilization']}%",
            "",
            "## Step Performance Analysis"
        ]
        
        for step in analysis_data["step_timings"]:
            status_emoji = "✅" if step["status"] == "success" else "❌"
            report_lines.append(
                f"- {status_emoji} **{step['step_name']}**: {step['execution_time']:.3f}s"
            )
        
        # Add insights
        if analysis_data.get("insights"):
            report_lines.extend([
                "",
                "## Performance Insights"
            ])
            
            for insight in analysis_data["insights"]:
                report_lines.append(f"- {insight}")
        
        # Performance recommendations
        report_lines.extend([
            "",
            "## Recommendations",
            "- Monitor memory usage for long-running recipes",
            "- Consider parallel execution for independent steps",
            "- Implement caching for repeated operations",
            "- Review timeout settings for slow steps"
        ])
        
        return "\n".join(report_lines)
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU utilization percentage."""
        import psutil
        return psutil.cpu_percent(interval=1)
    
    def _generate_performance_insights(self, data: dict) -> list:
        """Generate performance insights and recommendations."""
        insights = []
        
        # Analyze execution time
        if data["total_execution_time"] > 30:
            insights.append("⚠️ Long execution time detected - consider optimization")
        
        # Analyze step performance
        step_times = [s["execution_time"] for s in data["step_timings"]]
        if step_times:
            avg_step_time = sum(step_times) / len(step_times)
            slow_steps = [s for s in data["step_timings"] if s["execution_time"] > avg_step_time * 2]
            
            if slow_steps:
                insights.append(f"🐌 Slow steps detected: {[s['step_name'] for s in slow_steps]}")
        
        # Memory analysis
        if data["memory_usage"] > 100:  # MB
            insights.append("💾 High memory usage - consider data streaming")
        
        # CPU analysis  
        if data["cpu_utilization"] > 80:
            insights.append("🔥 High CPU utilization - system under load")
        
        return insights

# Usage example
analyzer = PerformanceAnalyzer(context)
analysis = analyzer.analyze_recipe_performance("orchestrator/recipes/data_pipeline.yaml")
report = analyzer.create_performance_report(analysis)

print(report)
```

### Real-Time Performance Dashboard

```python
from src.visualization.realtime_dashboard import RealtimeDashboard
import asyncio

class RealtimePerformanceMonitor:
    """Real-time performance monitoring with WebSocket updates."""
    
    def __init__(self, context: Context):
        self.context = context
        self.dashboard = RealtimeDashboard(context, port=8080)
        self.is_monitoring = False
        
    async def start_monitoring(self):
        """Start real-time performance monitoring."""
        self.is_monitoring = True
        
        print("🔄 Starting real-time performance monitoring...")
        print("📊 Dashboard available at: http://localhost:8080/dashboard")
        
        while self.is_monitoring:
            try:
                # Collect current metrics
                metrics = self._collect_system_metrics()
                
                # Update dashboard
                await self.dashboard.update_metrics(metrics)
                
                # Store in context for historical analysis
                self.context.set("monitoring.current_metrics", metrics, who="realtime_monitor")
                
                # Wait before next update
                await asyncio.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(5)
    
    def _collect_system_metrics(self) -> dict:
        """Collect current system performance metrics."""
        import psutil
        
        return {
            "timestamp": time.time(),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "active_processes": len(psutil.pids()),
            "framework_context_size": len(self.context.keys()) if self.context else 0
        }
    
    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self.is_monitoring = False
        print("⏹️ Performance monitoring stopped")

# Usage
async def main():
    monitor = RealtimePerformanceMonitor(context)
    
    # Start monitoring in background
    monitoring_task = asyncio.create_task(monitor.start_monitoring())
    
    # Simulate some work
    await asyncio.sleep(30)
    
    # Stop monitoring
    monitor.stop_monitoring()
    await monitoring_task

# Run async monitoring
asyncio.run(main())
```

## AI-Powered Analysis

### Basic Analysis Configuration

```python
from src.analysis.enhanced_framework import EnhancedAnalyzer, AnalysisConfig
from orchestrator.context import Context

# Configure AI-powered analysis
config = AnalysisConfig(
    statistical_precision=4,
    pattern_threshold=0.7,
    enable_ai_insights=True,
    debug_mode=True,
    analysis_types=["statistical", "trend", "anomaly", "performance"]
)

# Initialize analyzer with context
context = Context()
analyzer = EnhancedAnalyzer(config, context)

# Sample data for analysis
execution_data = [
    {"timestamp": "2025-01-05T10:00:00", "duration": 1.2, "status": "success", "step": "load_data"},
    {"timestamp": "2025-01-05T10:01:00", "duration": 0.8, "status": "success", "step": "validate_data"},
    {"timestamp": "2025-01-05T10:02:00", "duration": 2.1, "status": "success", "step": "process_data"},
    {"timestamp": "2025-01-05T10:03:00", "duration": 0.5, "status": "success", "step": "save_results"},
    {"timestamp": "2025-01-05T10:05:00", "duration": 1.8, "status": "success", "step": "load_data"},
    {"timestamp": "2025-01-05T10:06:00", "duration": 0.9, "status": "success", "step": "validate_data"},
    {"timestamp": "2025-01-05T10:07:00", "duration": 3.2, "status": "failed", "step": "process_data"},
]

# Perform comprehensive analysis
print("🤖 Starting AI-powered analysis...")
results = analyzer.analyze_execution_data(execution_data)

if results.success:
    print(f"✅ Analysis completed successfully!")
    print(f"📊 Quality Score: {results.quality_score:.2f}")
    print(f"📈 Patterns Found: {len(results.patterns)}")
    print(f"⚠️ Anomalies Detected: {len(results.anomalies)}")
    
    # Display insights
    print("\n🧠 AI Insights:")
    for insight in results.insights:
        print(f"  • {insight}")
        
    # Display patterns
    if results.patterns:
        print(f"\n📊 Detected Patterns:")
        for pattern in results.patterns:
            print(f"  • {pattern['type']}: {pattern['description']} (confidence: {pattern['confidence']:.2f})")
    
    # Display anomalies
    if results.anomalies:
        print(f"\n⚠️ Anomalies:")
        for anomaly in results.anomalies:
            print(f"  • {anomaly['type']}: {anomaly['description']} (severity: {anomaly['severity']})")

else:
    print("❌ Analysis failed:")
    for error in results.errors:
        print(f"  • {error}")
```

### Advanced Analysis Pipeline

```python
class ComprehensiveAnalysisPipeline:
    """Advanced analysis pipeline with multiple AI models."""
    
    def __init__(self, context: Context):
        self.context = context
        self.analyzers = {
            "statistical": EnhancedAnalyzer(AnalysisConfig(analysis_types=["statistical"]), context),
            "trend": EnhancedAnalyzer(AnalysisConfig(analysis_types=["trend"]), context),
            "anomaly": EnhancedAnalyzer(AnalysisConfig(analysis_types=["anomaly"]), context),
            "performance": EnhancedAnalyzer(AnalysisConfig(analysis_types=["performance"]), context)
        }
        
    def analyze_recipe_execution_history(self, recipe_name: str) -> dict:
        """Comprehensive analysis of recipe execution history."""
        
        # Retrieve historical data from context
        history_key = f"recipes.{recipe_name}.execution_history"
        execution_history = self.context.get(history_key, [])
        
        if not execution_history:
            return {"error": "No execution history found for recipe"}
        
        print(f"📊 Analyzing {len(execution_history)} historical executions for '{recipe_name}'")
        
        analysis_results = {}
        
        # 1. Statistical Analysis
        print("📈 Running statistical analysis...")
        stats_result = self.analyzers["statistical"].analyze_execution_data(execution_history)
        analysis_results["statistical"] = {
            "mean_duration": stats_result.statistics.get("mean", 0),
            "std_deviation": stats_result.statistics.get("std", 0),
            "success_rate": stats_result.statistics.get("success_rate", 0),
            "total_executions": len(execution_history)
        }
        
        # 2. Trend Analysis
        print("📉 Running trend analysis...")
        trend_result = self.analyzers["trend"].analyze_execution_data(execution_history)
        analysis_results["trends"] = {
            "duration_trend": trend_result.trends.get("duration_trend", "stable"),
            "success_trend": trend_result.trends.get("success_trend", "stable"),
            "frequency_trend": trend_result.trends.get("frequency_trend", "stable")
        }
        
        # 3. Anomaly Detection
        print("🔍 Running anomaly detection...")
        anomaly_result = self.analyzers["anomaly"].analyze_execution_data(execution_history)
        analysis_results["anomalies"] = [
            {
                "timestamp": anomaly.get("timestamp"),
                "type": anomaly.get("type"),
                "severity": anomaly.get("severity"),
                "description": anomaly.get("description")
            }
            for anomaly in anomaly_result.anomalies
        ]
        
        # 4. Performance Analysis
        print("⚡ Running performance analysis...")
        perf_result = self.analyzers["performance"].analyze_execution_data(execution_history)
        analysis_results["performance"] = {
            "avg_step_duration": perf_result.performance_metrics.get("avg_step_duration", 0),
            "bottleneck_steps": perf_result.performance_metrics.get("bottleneck_steps", []),
            "optimization_suggestions": perf_result.performance_metrics.get("suggestions", [])
        }
        
        # 5. Generate comprehensive insights
        insights = self._generate_comprehensive_insights(analysis_results)
        analysis_results["insights"] = insights
        
        # 6. Generate recommendations
        recommendations = self._generate_recommendations(analysis_results)
        analysis_results["recommendations"] = recommendations
        
        # Store results in context
        self.context.set(f"analysis.{recipe_name}.comprehensive", analysis_results, who="analysis_pipeline")
        
        return analysis_results
    
    def _generate_comprehensive_insights(self, results: dict) -> list:
        """Generate high-level insights from analysis results."""
        insights = []
        
        # Success rate insights
        success_rate = results["statistical"]["success_rate"]
        if success_rate < 0.8:
            insights.append(f"⚠️ Low success rate detected ({success_rate:.1%}) - investigate failure patterns")
        elif success_rate > 0.95:
            insights.append(f"✅ Excellent success rate ({success_rate:.1%}) - recipe is stable")
        
        # Duration insights
        mean_duration = results["statistical"]["mean_duration"]
        std_duration = results["statistical"]["std_deviation"]
        
        if std_duration > mean_duration * 0.5:
            insights.append("📊 High duration variability - execution time is inconsistent")
        
        # Trend insights
        duration_trend = results["trends"]["duration_trend"]
        if duration_trend == "increasing":
            insights.append("📈 Execution time is increasing over time - potential performance degradation")
        elif duration_trend == "decreasing":
            insights.append("📉 Execution time is improving over time - optimizations are working")
        
        # Anomaly insights
        anomaly_count = len(results["anomalies"])
        if anomaly_count > 0:
            high_severity = len([a for a in results["anomalies"] if a["severity"] == "high"])
            insights.append(f"🚨 {anomaly_count} anomalies detected ({high_severity} high severity)")
        
        return insights
    
    def _generate_recommendations(self, results: dict) -> list:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Performance recommendations
        bottlenecks = results["performance"]["bottleneck_steps"]
        if bottlenecks:
            recommendations.append(f"🔧 Optimize bottleneck steps: {', '.join(bottlenecks)}")
        
        # Reliability recommendations
        if results["statistical"]["success_rate"] < 0.9:
            recommendations.append("🛡️ Implement retry mechanisms and better error handling")
        
        # Monitoring recommendations
        if len(results["anomalies"]) > 2:
            recommendations.append("📊 Increase monitoring frequency to catch issues early")
        
        # Optimization recommendations
        if results["statistical"]["mean_duration"] > 60:  # seconds
            recommendations.append("⚡ Consider parallel execution for long-running recipes")
        
        return recommendations

# Usage example
pipeline = ComprehensiveAnalysisPipeline(context)

# Simulate execution history data
execution_history = [
    {"timestamp": f"2025-01-{i:02d}T10:00:00", "duration": 1.2 + (i * 0.1), "status": "success", "steps": ["load", "process", "save"]}
    for i in range(1, 31)  # 30 days of history
]

# Add some failures and anomalies
execution_history[10]["status"] = "failed"
execution_history[10]["duration"] = 45.0  # Anomaly
execution_history[20]["duration"] = 0.1   # Another anomaly

# Store history in context
context.set("recipes.data_processing.execution_history", execution_history, who="system")

# Run comprehensive analysis
results = pipeline.analyze_recipe_execution_history("data_processing")

# Generate analysis report
def generate_analysis_report(results: dict) -> str:
    """Generate human-readable analysis report."""
    
    report = [
        "# Recipe Analysis Report",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Executive Summary"
    ]
    
    # Key metrics
    stats = results["statistical"]
    report.extend([
        f"- **Success Rate**: {stats['success_rate']:.1%}",
        f"- **Average Duration**: {stats['mean_duration']:.2f}s",
        f"- **Total Executions**: {stats['total_executions']}",
        f"- **Anomalies Detected**: {len(results['anomalies'])}",
        ""
    ])
    
    # Insights
    if results["insights"]:
        report.extend(["## Key Insights"])
        report.extend([f"- {insight}" for insight in results["insights"]])
        report.append("")
    
    # Recommendations
    if results["recommendations"]:
        report.extend(["## Recommendations"])
        report.extend([f"- {rec}" for rec in results["recommendations"]])
        report.append("")
    
    # Trends
    trends = results["trends"]
    report.extend([
        "## Trend Analysis",
        f"- **Duration Trend**: {trends['duration_trend']}",
        f"- **Success Trend**: {trends['success_trend']}",
        f"- **Frequency Trend**: {trends['frequency_trend']}",
        ""
    ])
    
    # Performance details
    perf = results["performance"]
    if perf["bottleneck_steps"]:
        report.extend([
            "## Performance Bottlenecks",
            f"- Identified bottleneck steps: {', '.join(perf['bottleneck_steps'])}",
            f"- Average step duration: {perf['avg_step_duration']:.2f}s"
        ])
    
    return "\n".join(report)

# Generate and print report
report = generate_analysis_report(results)
print("\n" + report)
```

## Visualization

### Performance Visualization Dashboard

```python
from src.visualization.performance_dashboard import PerformanceDashboard
from src.visualization.realtime_dashboard import RealtimeDashboard

# Create performance visualization
dashboard = PerformanceDashboard(context, port=8080)

# Start dashboard server
dashboard.start_server()
print("📊 Performance Dashboard: http://localhost:8080/dashboard")

# Add real-time metrics
realtime_dashboard = RealtimeDashboard(context, port=8081)
realtime_dashboard.add_metric_widget("CPU Usage", "gauge")
realtime_dashboard.add_metric_widget("Memory Usage", "line_chart")
realtime_dashboard.add_metric_widget("Recipe Execution Time", "bar_chart")

# Generate visualization data
visualization_data = {
    "execution_times": [1.2, 0.8, 2.1, 0.5, 1.8],
    "cpu_usage": [45, 52, 38, 41, 48],
    "memory_usage": [120, 135, 98, 110, 125],
    "success_rates": [0.95, 0.87, 0.92, 0.98, 0.91]
}

# Create charts
charts = dashboard.create_performance_charts(visualization_data)
dashboard.display_charts(charts)
```

## Enhanced Context Server

### WebSocket Real-Time Synchronization

```python
from server.context_server import EnhancedContextServer
import asyncio

# Initialize enhanced context server
server = EnhancedContextServer(host="0.0.0.0", port=8765)

# Start server with WebSocket support
async def start_context_server():
    print("🌐 Starting Enhanced Context Server...")
    
    # Configure distributed sync
    server.enable_distributed_sync(
        cluster_nodes=["node1:8765", "node2:8765"],
        sync_interval=1.0
    )
    
    # Start WebSocket server
    await server.start_websocket_server()
    
    # Set up memory bus
    server.setup_memory_bus()
    
    print("✅ Context Server ready for distributed operations")

# Run server
asyncio.run(start_context_server())
```

### Distributed Context Management

```python
from orchestrator.context import DistributedContext

# Create distributed context client
distributed_context = DistributedContext(
    server_url="ws://localhost:8765",
    node_id="worker_1"
)

# Connect to distributed context
await distributed_context.connect()

# Cross-node data sharing
distributed_context.set_global("shared.config", {"env": "production"})
distributed_context.set_local("worker.status", "active")

# Synchronize across cluster
await distributed_context.sync_cluster()
```

## Integration Patterns

### Multi-Framework Integration

```python
# Integration with external systems
class ExternalSystemIntegration:
    """Framework0 integration with external systems."""
    
    def __init__(self, context: Context):
        self.context = context
        self.integrations = {}
    
    def register_integration(self, name: str, connector):
        """Register external system connector."""
        self.integrations[name] = connector
        self.context.set(f"integrations.{name}.status", "registered")
    
    def execute_cross_system_workflow(self, workflow_config: dict):
        """Execute workflow across multiple systems."""
        for step in workflow_config["steps"]:
            system = step["system"]
            operation = step["operation"]
            
            if system in self.integrations:
                connector = self.integrations[system]
                result = connector.execute(operation, step["params"])
                
                self.context.set(f"workflow.{step['name']}.result", result)
            else:
                raise ValueError(f"Unknown integration: {system}")

# Usage
integration = ExternalSystemIntegration(context)
integration.register_integration("database", database_connector)
integration.register_integration("api", api_connector)

workflow = {
    "steps": [
        {"name": "fetch_data", "system": "database", "operation": "select", "params": {"table": "users"}},
        {"name": "process_api", "system": "api", "operation": "post", "params": {"endpoint": "/process"}}
    ]
}

integration.execute_cross_system_workflow(workflow)
```

## Production Scenarios

### Enterprise Deployment Example

```bash
#!/bin/bash
# Production deployment script

# 1. Create isolated recipe packages
python tools/recipe_isolation_cli.py workflow orchestrator/recipes/etl_pipeline.yaml --output /deploy/production

# 2. Validate deployment packages
python tools/recipe_isolation_cli.py validate /deploy/production/etl_pipeline

# 3. Start enhanced context server cluster
python server/context_server.py --cluster --nodes node1,node2,node3

# 4. Deploy to production environment
./deploy_framework0.sh --environment production --package /deploy/production/etl_pipeline

# 5. Start monitoring
python tools/monitoring_dashboard.py --production --port 9090
```

### High-Availability Configuration

```yaml
# production_config.yaml
framework0:
  context_server:
    cluster_mode: true
    nodes:
      - host: "node1.prod.local"
        port: 8765
      - host: "node2.prod.local" 
        port: 8765
      - host: "node3.prod.local"
        port: 8765
    
  recipe_execution:
    max_retries: 3
    timeout: 300
    parallel_limit: 10
    
  monitoring:
    performance_tracking: true
    real_time_dashboard: true
    alert_thresholds:
      execution_time: 60
      memory_usage: 80
      error_rate: 0.1
```

This comprehensive Framework0 usage documentation covers all major features with practical examples and real-world scenarios. Users can reference these examples to understand how to implement complete automation solutions using Framework0's enterprise-grade capabilities.

The documentation demonstrates the full power of Framework0, from simple recipe creation to advanced AI-powered analysis and production deployment scenarios. Each section builds upon the previous ones, showing how Framework0 components work together to create sophisticated automation workflows.