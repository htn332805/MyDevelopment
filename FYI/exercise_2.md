# Exercise 2: Data Processing Basics - Context & Variables

**Duration:** 45-60 minutes  
**Difficulty:** Beginner-Intermediate  
**Prerequisites:** Completed Exercise 1  

## 🎯 Learning Objectives

By the end of this exercise, you will:

- Master Framework0 Context operations (get, set, contains, keys)
- Understand data flow between recipe steps
- Process CSV data using Framework0 patterns
- Implement variable substitution and templating
- Create reusable data processing scriptlets
- Handle different data formats (CSV, JSON, text)
- Use Context for configuration management

## 📚 Concepts Introduction

### Advanced Context Operations

The Framework0 **Context** system is your data backbone. It enables:

- **Data Sharing**: Pass data between recipe steps
- **State Management**: Track workflow progress and results
- **Configuration**: Store settings accessible to all steps
- **History Tracking**: Monitor data changes and operations

### Context Methods Overview

```python
# Basic operations
context.set(key, value, who="scriptlet_name")     # Store data
data = context.get(key, default=None)             # Retrieve data
exists = context.contains(key)                    # Check existence
all_keys = context.keys()                         # List all keys

# Advanced operations
context.get_history()                             # View change history
context.clear()                                   # Clear all data
context.get_by_pattern("user.*")                  # Pattern matching
```

### Data Processing Patterns

Framework0 follows these data processing patterns:
- **Input → Process → Output**: Standard ETL workflow
- **Validation → Transform → Store**: Data quality pipeline
- **Load → Analyze → Report**: Analytics workflow

## 🛠️ Exercise Steps

### Step 1: Create Sample Data Files

First, let's create sample data files for our processing exercises.

**📁 Create:** `FYI/exercises/data/sample_employees.csv`

```csv
id,name,department,salary,hire_date,status
1,Alice Johnson,Engineering,85000,2023-01-15,active
2,Bob Smith,Marketing,62000,2023-02-20,active
3,Carol Davis,Engineering,78000,2022-11-10,active
4,David Wilson,Sales,71000,2023-03-05,active
5,Eve Brown,Marketing,58000,2022-12-01,inactive
6,Frank Miller,Engineering,92000,2021-08-15,active
7,Grace Lee,Sales,66000,2023-04-12,active
8,Henry Taylor,Engineering,81000,2022-09-18,active
```

**📁 Create:** `FYI/exercises/data/config.json`

```json
{
  "processing": {
    "output_format": "json",
    "include_statistics": true,
    "filter_active_only": true,
    "salary_threshold": 70000
  },
  "reporting": {
    "generate_summary": true,
    "export_charts": false,
    "email_results": false
  },
  "database": {
    "connection_string": "sqlite:///employees.db",
    "table_name": "employees",
    "auto_create": true
  }
}
```

### Step 2: Create the Data Processing Recipe

Now let's create a comprehensive recipe that demonstrates Context usage and data processing.

**📁 Create:** `FYI/exercises/data_processing_basics.yaml`

```yaml
metadata:
  name: "data_processing_basics"
  version: "1.0"
  description: "Learn Framework0 Context and data processing fundamentals"
  author: "Framework0 Student"
  tags: ["tutorial", "data-processing", "context", "variables"]
  created_date: "2025-01-05"

steps:
  - name: "load_configuration"
    idx: 1
    type: "python"
    module: "scriptlets.tutorial"
    function: "ConfigLoaderScriptlet"
    args:
      config_file: "FYI/exercises/data/config.json"
      config_namespace: "app_config"
      validate_required: true

  - name: "load_employee_data"
    idx: 2
    type: "python"
    module: "scriptlets.tutorial"
    function: "CSVLoaderScriptlet"
    depends_on: ["load_configuration"]
    args:
      input_file: "FYI/exercises/data/sample_employees.csv"
      data_key: "employees"
      validate_headers: true
      expected_columns: ["id", "name", "department", "salary", "hire_date", "status"]

  - name: "process_employee_data"
    idx: 3
    type: "python"
    module: "scriptlets.tutorial"
    function: "DataProcessorScriptlet"
    depends_on: ["load_employee_data"]
    args:
      input_key: "employees"
      output_key: "processed_employees"
      operations:
        - "filter_active"
        - "calculate_statistics"
        - "add_salary_grades"

  - name: "generate_report"
    idx: 4
    type: "python"
    module: "scriptlets.tutorial"
    function: "ReportGeneratorScriptlet"
    depends_on: ["process_employee_data"]
    args:
      data_key: "processed_employees"
      template_variables:
        report_title: "Employee Data Analysis Report"
        generated_by: "Framework0 Tutorial System"
        company_name: "Tutorial Corp"
      output_formats: ["console", "json"]
      output_file: "FYI/exercises/output/employee_report.json"
```

### Step 3: Create Advanced Data Processing Scriptlets

Now let's create the scriptlets that demonstrate Context mastery and data processing.

**📁 Create:** `scriptlets/tutorial/data_processing_scriptlets.py`

```python
"""
Framework0 Tutorial - Data Processing Scriptlets

Advanced scriptlets demonstrating:
- Context operations and data flow
- CSV data processing and validation
- Configuration management
- Variable substitution and templating
- Error handling and data validation
"""

from scriptlets.framework import BaseScriptlet, register_scriptlet
from orchestrator.context import Context
from typing import Dict, Any, List, Optional
from src.core.logger import get_logger
import os
import json
import csv
import pathlib
from datetime import datetime, date
from decimal import Decimal

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

@register_scriptlet
class ConfigLoaderScriptlet(BaseScriptlet):
    """
    Configuration loader with Context integration.
    
    Demonstrates:
    - Loading JSON configuration files
    - Storing configuration in Context with namespacing
    - Configuration validation and error handling
    - Making config accessible to other scriptlets
    """
    
    def __init__(self) -> None:
        """Initialize the configuration loader."""
        super().__init__()
        self.name = "config_loader"
        self.version = "1.0"
        self.description = "Load and validate JSON configuration files"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load configuration file and store in Context.
        
        Args:
            context: Framework0 context for data sharing
            params: Parameters including config_file path
            
        Returns:
            Dict containing loading results and statistics
        """
        try:
            logger.info(f"Starting {self.name} execution")
            
            # Extract parameters
            config_file = params["config_file"]
            namespace = params.get("config_namespace", "config")
            validate_required = params.get("validate_required", False)
            
            # Validate file exists
            config_path = pathlib.Path(config_file)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_file}")
            
            # Load JSON configuration
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            print(f"📋 Loading configuration from: {config_file}")
            print(f"📁 Namespace: {namespace}")
            
            # Store configuration in Context with namespace
            for section, values in config_data.items():
                section_key = f"{namespace}.{section}"
                context.set(section_key, values, who=self.name)
                
                print(f"   ✅ Loaded section '{section}' with {len(values)} settings")
                
                # Store individual config values for easy access
                for key, value in values.items():
                    full_key = f"{namespace}.{section}.{key}"
                    context.set(full_key, value, who=self.name)
            
            # Store metadata
            context.set(f"{namespace}._metadata", {
                "loaded_from": str(config_path.absolute()),
                "loaded_at": datetime.now().isoformat(),
                "sections": list(config_data.keys()),
                "total_settings": sum(len(v) if isinstance(v, dict) else 1 for v in config_data.values())
            }, who=self.name)
            
            logger.info(f"✅ Configuration loaded successfully: {len(config_data)} sections")
            
            return {
                "status": "success",
                "config_file": config_file,
                "namespace": namespace,
                "sections_loaded": len(config_data),
                "total_settings": sum(len(v) if isinstance(v, dict) else 1 for v in config_data.values()),
                "execution_time": self.get_execution_time()
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} execution failed: {e}")
            context.set(f"{self.name}.error", str(e), who=self.name)
            raise

@register_scriptlet
class CSVLoaderScriptlet(BaseScriptlet):
    """
    CSV data loader with validation and Context integration.
    
    Demonstrates:
    - CSV file processing and validation
    - Data type conversion and cleaning
    - Storing structured data in Context
    - Error handling for malformed data
    """
    
    def __init__(self) -> None:
        """Initialize the CSV loader."""
        super().__init__()
        self.name = "csv_loader"
        self.version = "1.0"
        self.description = "Load and validate CSV data files"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load CSV file and store data in Context.
        
        Args:
            context: Framework0 context for data sharing
            params: Parameters including input_file and validation options
            
        Returns:
            Dict containing loading results and data statistics
        """
        try:
            logger.info(f"Starting {self.name} execution")
            
            # Extract parameters
            input_file = params["input_file"]
            data_key = params.get("data_key", "csv_data")
            validate_headers = params.get("validate_headers", False)
            expected_columns = params.get("expected_columns", [])
            
            # Validate file exists
            csv_path = pathlib.Path(input_file)
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file not found: {input_file}")
            
            print(f"📊 Loading CSV data from: {input_file}")
            
            # Load CSV data
            records = []
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate headers if requested
                if validate_headers and expected_columns:
                    actual_columns = reader.fieldnames or []
                    missing_columns = set(expected_columns) - set(actual_columns)
                    if missing_columns:
                        raise ValueError(f"Missing expected columns: {missing_columns}")
                    print(f"   ✅ Header validation passed: {len(actual_columns)} columns")
                
                # Process records
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Clean and convert data types
                        processed_row = self._process_csv_row(row)
                        processed_row['_row_number'] = row_num
                        records.append(processed_row)
                    except Exception as e:
                        logger.warning(f"Error processing row {row_num}: {e}")
                        continue
            
            # Store data in Context
            context.set(data_key, records, who=self.name)
            
            # Store metadata
            metadata = {
                "source_file": str(csv_path.absolute()),
                "loaded_at": datetime.now().isoformat(),
                "total_records": len(records),
                "columns": list(records[0].keys()) if records else [],
                "file_size_bytes": csv_path.stat().st_size
            }
            context.set(f"{data_key}_metadata", metadata, who=self.name)
            
            print(f"   📋 Loaded {len(records)} records")
            print(f"   📊 Columns: {', '.join(metadata['columns'][:5])}{'...' if len(metadata['columns']) > 5 else ''}")
            
            logger.info(f"✅ CSV data loaded successfully: {len(records)} records")
            
            return {
                "status": "success",
                "input_file": input_file,
                "data_key": data_key,
                "records_loaded": len(records),
                "columns": metadata['columns'],
                "execution_time": self.get_execution_time()
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} execution failed: {e}")
            context.set(f"{self.name}.error", str(e), who=self.name)
            raise
    
    def _process_csv_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Process and clean a CSV row, converting data types.
        
        Args:
            row: Raw CSV row as string dictionary
            
        Returns:
            Processed row with appropriate data types
        """
        processed = {}
        
        for key, value in row.items():
            # Clean whitespace
            clean_key = key.strip()
            clean_value = value.strip() if value else ""
            
            # Convert data types based on content
            if clean_value.lower() in ('', 'null', 'none'):
                processed[clean_key] = None
            elif clean_value.lower() in ('true', 'false'):
                processed[clean_key] = clean_value.lower() == 'true'
            elif clean_value.isdigit():
                processed[clean_key] = int(clean_value)
            elif self._is_float(clean_value):
                processed[clean_key] = float(clean_value)
            elif self._is_date(clean_value):
                processed[clean_key] = clean_value  # Keep as string for now
            else:
                processed[clean_key] = clean_value
        
        return processed
    
    def _is_float(self, value: str) -> bool:
        """Check if string represents a float."""
        try:
            float(value)
            return '.' in value
        except ValueError:
            return False
    
    def _is_date(self, value: str) -> bool:
        """Check if string represents a date."""
        date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
        for fmt in date_formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        return False

@register_scriptlet
class DataProcessorScriptlet(BaseScriptlet):
    """
    Advanced data processor demonstrating Context operations.
    
    Demonstrates:
    - Reading data from Context
    - Complex data transformations
    - Using configuration from Context
    - Storing processed results back to Context
    """
    
    def __init__(self) -> None:
        """Initialize the data processor."""
        super().__init__()
        self.name = "data_processor"
        self.version = "1.0"
        self.description = "Process and transform data using Context operations"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data with operations defined in parameters.
        
        Args:
            context: Framework0 context for data sharing
            params: Parameters including input_key, output_key, and operations
            
        Returns:
            Dict containing processing results and statistics
        """
        try:
            logger.info(f"Starting {self.name} execution")
            
            # Extract parameters
            input_key = params["input_key"]
            output_key = params["output_key"]
            operations = params.get("operations", [])
            
            # Get input data from Context
            input_data = context.get(input_key)
            if input_data is None:
                raise ValueError(f"No data found in Context with key: {input_key}")
            
            print(f"🔄 Processing data: {input_key} → {output_key}")
            print(f"📊 Input: {len(input_data)} records")
            print(f"⚙️ Operations: {', '.join(operations)}")
            
            # Start with input data
            processed_data = input_data.copy()
            operation_results = {}
            
            # Apply operations in sequence
            for operation in operations:
                print(f"   🔧 Applying operation: {operation}")
                
                if operation == "filter_active":
                    processed_data = self._filter_active_employees(processed_data, context)
                    operation_results[operation] = f"Filtered to {len(processed_data)} active employees"
                    
                elif operation == "calculate_statistics":
                    stats = self._calculate_statistics(processed_data, context)
                    operation_results[operation] = f"Calculated {len(stats)} statistics"
                    
                elif operation == "add_salary_grades":
                    processed_data = self._add_salary_grades(processed_data, context)
                    operation_results[operation] = "Added salary grade classifications"
                    
                else:
                    logger.warning(f"Unknown operation: {operation}")
            
            # Store processed data in Context
            context.set(output_key, processed_data, who=self.name)
            
            # Store processing metadata
            processing_metadata = {
                "processed_at": datetime.now().isoformat(),
                "input_records": len(input_data),
                "output_records": len(processed_data),
                "operations_applied": operations,
                "operation_results": operation_results
            }
            context.set(f"{output_key}_processing", processing_metadata, who=self.name)
            
            print(f"   ✅ Processing complete: {len(processed_data)} records")
            
            logger.info(f"✅ Data processing completed successfully")
            
            return {
                "status": "success",
                "input_key": input_key,
                "output_key": output_key,
                "input_records": len(input_data),
                "output_records": len(processed_data),
                "operations_applied": operations,
                "execution_time": self.get_execution_time()
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} execution failed: {e}")
            context.set(f"{self.name}.error", str(e), who=self.name)
            raise
    
    def _filter_active_employees(self, data: List[Dict], context: Context) -> List[Dict]:
        """Filter for active employees based on configuration."""
        
        # Check if filtering is enabled in config
        filter_enabled = context.get("app_config.processing.filter_active_only", True)
        if not filter_enabled:
            return data
        
        active_data = [record for record in data if record.get("status") == "active"]
        context.set("processing.filter_active.count", len(active_data), who=self.name)
        
        return active_data
    
    def _calculate_statistics(self, data: List[Dict], context: Context) -> Dict[str, Any]:
        """Calculate statistics and store in Context."""
        
        if not data:
            return {}
        
        # Calculate salary statistics
        salaries = [record.get("salary", 0) for record in data if record.get("salary")]
        
        stats = {
            "total_employees": len(data),
            "salary_stats": {
                "min": min(salaries) if salaries else 0,
                "max": max(salaries) if salaries else 0,
                "average": sum(salaries) / len(salaries) if salaries else 0,
                "total": sum(salaries)
            },
            "department_counts": self._count_by_field(data, "department"),
            "status_counts": self._count_by_field(data, "status")
        }
        
        # Store statistics in Context
        context.set("processing.statistics", stats, who=self.name)
        
        return stats
    
    def _add_salary_grades(self, data: List[Dict], context: Context) -> List[Dict]:
        """Add salary grade classifications to employee records."""
        
        # Get salary threshold from config
        threshold = context.get("app_config.processing.salary_threshold", 70000)
        
        for record in data:
            salary = record.get("salary", 0)
            
            if salary >= threshold + 20000:
                grade = "Senior"
            elif salary >= threshold:
                grade = "Mid"
            else:
                grade = "Junior"
            
            record["salary_grade"] = grade
        
        return data
    
    def _count_by_field(self, data: List[Dict], field: str) -> Dict[str, int]:
        """Count occurrences of values in a field."""
        counts = {}
        for record in data:
            value = record.get(field, "Unknown")
            counts[value] = counts.get(value, 0) + 1
        return counts

@register_scriptlet
class ReportGeneratorScriptlet(BaseScriptlet):
    """
    Report generator with template variables and Context integration.
    
    Demonstrates:
    - Template variable substitution
    - Reading configuration and data from Context
    - Multiple output formats
    - File output operations
    """
    
    def __init__(self) -> None:
        """Initialize the report generator."""
        super().__init__()
        self.name = "report_generator"
        self.version = "1.0"
        self.description = "Generate reports with template variables and multiple formats"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate report from Context data with template variables.
        
        Args:
            context: Framework0 context for data sharing
            params: Parameters including data_key and template_variables
            
        Returns:
            Dict containing report generation results
        """
        try:
            logger.info(f"Starting {self.name} execution")
            
            # Extract parameters
            data_key = params["data_key"]
            template_vars = params.get("template_variables", {})
            output_formats = params.get("output_formats", ["console"])
            output_file = params.get("output_file")
            
            # Get data from Context
            report_data = context.get(data_key, [])
            statistics = context.get("processing.statistics", {})
            
            print(f"📄 Generating report for: {data_key}")
            print(f"📊 Data records: {len(report_data)}")
            
            # Build report content
            report = self._build_report(report_data, statistics, template_vars, context)
            
            # Output in requested formats
            outputs_generated = []
            
            if "console" in output_formats:
                self._output_to_console(report)
                outputs_generated.append("console")
            
            if "json" in output_formats and output_file:
                self._output_to_json(report, output_file)
                outputs_generated.append(f"json:{output_file}")
            
            # Store report in Context
            context.set("report.content", report, who=self.name)
            context.set("report.generated_at", datetime.now().isoformat(), who=self.name)
            
            logger.info(f"✅ Report generated successfully: {len(outputs_generated)} outputs")
            
            return {
                "status": "success",
                "data_key": data_key,
                "records_processed": len(report_data),
                "outputs_generated": outputs_generated,
                "template_variables_used": len(template_vars),
                "execution_time": self.get_execution_time()
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} execution failed: {e}")
            context.set(f"{self.name}.error", str(e), who=self.name)
            raise
    
    def _build_report(self, data: List[Dict], stats: Dict, template_vars: Dict, context: Context) -> Dict[str, Any]:
        """Build comprehensive report structure."""
        
        return {
            "header": {
                "title": template_vars.get("report_title", "Data Analysis Report"),
                "generated_by": template_vars.get("generated_by", "Framework0"),
                "company": template_vars.get("company_name", "Unknown Company"),
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "framework_version": "2.0.0-enhanced"
            },
            "summary": {
                "total_records": len(data),
                "processing_completed": True,
                "data_source": context.get("employees_metadata.source_file", "Unknown"),
            },
            "statistics": stats,
            "data_sample": data[:5] if data else [],  # First 5 records
            "metadata": {
                "context_keys": len(context.keys()),
                "processing_time": context.get("data_processor.execution_time", "Unknown")
            }
        }
    
    def _output_to_console(self, report: Dict) -> None:
        """Output report to console with formatting."""
        
        header = report["header"]
        summary = report["summary"]
        stats = report.get("statistics", {})
        
        print("\n" + "="*70)
        print(f"📊 {header['title']}")
        print(f"🏢 {header['company']}")
        print(f"📅 Generated: {header['generated_at']}")
        print(f"⚡ Framework0 v{header['framework_version']}")
        print("="*70)
        
        print(f"\n📋 SUMMARY")
        print(f"   Total Records: {summary['total_records']}")
        print(f"   Data Source: {summary['data_source']}")
        
        if stats:
            salary_stats = stats.get("salary_stats", {})
            if salary_stats:
                print(f"\n💰 SALARY ANALYSIS")
                print(f"   Average Salary: ${salary_stats.get('average', 0):,.2f}")
                print(f"   Salary Range: ${salary_stats.get('min', 0):,} - ${salary_stats.get('max', 0):,}")
            
            dept_counts = stats.get("department_counts", {})
            if dept_counts:
                print(f"\n🏢 DEPARTMENT BREAKDOWN")
                for dept, count in dept_counts.items():
                    print(f"   {dept}: {count} employees")
        
        print("="*70 + "\n")
    
    def _output_to_json(self, report: Dict, output_file: str) -> None:
        """Output report to JSON file."""
        
        # Ensure output directory exists
        output_path = pathlib.Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📄 JSON report saved: {output_file}")
```

### Step 4: Test Your Data Processing Recipe

Let's create the necessary directories and test the complete workflow.

**🗂️ Create directories:**

```bash
# Create necessary directories
mkdir -p FYI/exercises/data
mkdir -p FYI/exercises/output
```

**🚀 Execute the recipe:**

```bash
# Navigate to Framework0 directory
cd /home/hai/hai_vscode/MyDevelopment

# Activate Python environment
source ~/pyvenv/bin/activate

# Execute your data processing recipe
python orchestrator/runner.py --recipe FYI/exercises/data_processing_basics.yaml --debug
```

**Expected Output:**
```
🚀 Starting recipe execution: data_processing_basics

⚡ Step 1: load_configuration
📋 Loading configuration from: FYI/exercises/data/config.json
📁 Namespace: app_config
   ✅ Loaded section 'processing' with 4 settings
   ✅ Loaded section 'reporting' with 3 settings
   ✅ Loaded section 'database' with 3 settings

⚡ Step 2: load_employee_data (depends on: load_configuration)
📊 Loading CSV data from: FYI/exercises/data/sample_employees.csv
   ✅ Header validation passed: 6 columns
   📋 Loaded 8 records
   📊 Columns: id, name, department, salary, hire_date...

⚡ Step 3: process_employee_data (depends on: load_employee_data)
🔄 Processing data: employees → processed_employees
📊 Input: 8 records
⚙️ Operations: filter_active, calculate_statistics, add_salary_grades
   🔧 Applying operation: filter_active
   🔧 Applying operation: calculate_statistics
   🔧 Applying operation: add_salary_grades
   ✅ Processing complete: 7 records

⚡ Step 4: generate_report (depends on: process_employee_data)
📄 Generating report for: processed_employees
📊 Data records: 7 records

======================================================================
📊 Employee Data Analysis Report
🏢 Tutorial Corp
📅 Generated: 2025-01-05 14:30:15
⚡ Framework0 v2.0.0-enhanced
======================================================================

📋 SUMMARY
   Total Records: 7
   Data Source: /path/to/sample_employees.csv

💰 SALARY ANALYSIS
   Average Salary: $74,428.57
   Salary Range: $62,000 - $92,000

🏢 DEPARTMENT BREAKDOWN
   Engineering: 4 employees
   Marketing: 1 employees
   Sales: 2 employees
======================================================================

📄 JSON report saved: FYI/exercises/output/employee_report.json

🎉 Recipe execution completed successfully!
```

### Step 5: Understanding Context Data Flow

Let's examine how data flows through the Context system:

**Context Data After Execution:**
```
app_config.processing.filter_active_only → true
app_config.processing.salary_threshold → 70000
employees → [8 employee records]
employees_metadata → {source_file, loaded_at, total_records...}
processed_employees → [7 filtered employee records with salary_grade]
processing.statistics → {salary_stats, department_counts...}
report.content → {complete report structure}
```

## ✅ Checkpoint Questions

**Question 1:** How does data flow from the CSV loader to the report generator through Context?

**Question 2:** What happens to Context data when a step fails? How is error information stored?

**Question 3:** How would you modify the recipe to process multiple CSV files in parallel?

**Question 4:** How could you use Context to implement conditional step execution?

## 🎯 Advanced Challenges

### Challenge A: Dynamic Configuration
Modify the recipe to accept command-line parameters that override configuration values.

### Challenge B: Data Validation Pipeline
Add a validation step that checks data quality and stores validation results in Context.

### Challenge C: Multi-format Output
Extend the report generator to support XML and HTML output formats.

### Challenge D: Context History Analysis
Create a step that analyzes Context history to show data transformation flow.

## 📁 Exercise Deliverables

**Reusable Components Created:**

1. **`ConfigLoaderScriptlet`** - JSON configuration management with Context integration
2. **`CSVLoaderScriptlet`** - CSV data loading with validation and type conversion  
3. **`DataProcessorScriptlet`** - Advanced data processing with Context operations
4. **`ReportGeneratorScriptlet`** - Multi-format report generation with templates

**Recipe Pattern:** `data_processing_basics.yaml` demonstrates:
- Sequential step dependencies
- Configuration-driven processing
- Context-based data flow
- Multi-step data transformation pipeline

## 🔍 Key Learning Points

- **Context Mastery**: Store, retrieve, and share data between steps
- **Data Pipeline Patterns**: Load → Process → Report workflow
- **Configuration Management**: External config files with Context integration  
- **Error Handling**: Proper exception management and error storage
- **Variable Substitution**: Template-based report generation

## 🚀 What's Next?

In **Exercise 3**, you'll learn:
- Complex recipe dependencies and parallel execution
- Conditional step execution based on Context data
- Recipe composition and sub-recipe patterns
- Advanced error handling and recovery strategies

## 📝 Exercise Completion Checklist

- [ ] Created sample data files (CSV and JSON)
- [ ] Created `data_processing_basics.yaml` recipe
- [ ] Implemented all four data processing scriptlets
- [ ] Successfully executed the complete workflow
- [ ] Examined Context data flow and transformations
- [ ] Answered checkpoint questions
- [ ] Attempted at least one advanced challenge

**Ready for Exercise 3?** 
✅ **Share your results and any questions before we proceed to Recipe Dependencies!**