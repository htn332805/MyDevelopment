# Excel Automation Framework - User Guide

## Overview

The Excel Automation Framework provides comprehensive tools for automating Excel processing tasks including data cleaning, analysis, visualization, and batch operations. It integrates seamlessly with Framework0 patterns and provides both programmatic API and command-line interfaces.

## Features

### 1. Data Cleaning & Transformation
- **Duplicate Removal**: Remove duplicate rows across sheets with configurable criteria
- **Format Standardization**: Standardize date formats, currency, and text casing
- **Data Cleaning**: Auto-clean raw exports by removing extra spaces, fixing encodings
- **Column Normalization**: Normalize column names for consistency
- **Sheet Management**: Split/merge sheets based on business rules
- **Navigation**: Auto-generate table of contents with navigation buttons for large workbooks

### 2. Data Analysis & Reporting  
- **Pivot Tables**: Automatically generate pivot tables from raw data
- **Filtering**: Filter columns by value ranges with flexible criteria
- **Highlighting**: Highlight cells based on value thresholds
- **Summaries**: Create comprehensive summary sheets with KPIs and statistics
- **Scheduled Analysis**: Support for recurring analysis tasks

### 3. Visualization & Dashboards
- **Charts**: Auto-generate bar, line, and pie charts from data
- **Conditional Formatting**: Apply color scales, above/below average formatting
- **Dashboard Creation**: Create interactive dashboards that refresh with new data
- **Chart Formatting**: Advanced chart formatting with axis titles, gridlines, positioning

### 4. Command Line Interface
- **Standalone Operation**: Run as CLI command with comprehensive argument parsing
- **Configuration Support**: JSON configuration files for complex workflows
- **Batch Processing**: Process multiple Excel files in directories
- **Flexible Commands**: Modular commands for specific operations

## Quick Start

### Installation

The framework requires Python 3.8+ and the following dependencies:
```bash
pip install pandas openpyxl xlsxwriter matplotlib seaborn plotly
```

### Basic Usage - Programmatic API

```python
from analysis.excel_processor import ExcelProcessorV1, ExcelConfigV1

# Initialize processor
processor = ExcelProcessorV1('data.xlsx', debug=True)
processor.load_workbook()

# Clean data
removed = processor.remove_duplicates_from_sheet('Sales Data')
mappings = processor.normalize_column_names('Sales Data')

# Create analysis
processor.create_pivot_table_from_data(
    source_sheet='Sales Data',
    target_sheet='Sales Pivot', 
    rows=['Region', 'Product'],
    values=['Sales', 'Profit'],
    aggfunc='sum'
)

# Add visualization
processor.create_chart_from_data(
    sheet_name='Sales Pivot',
    chart_type='bar',
    data_range='A1:D10',
    chart_title='Sales by Region'
)

# Save results
processor.save_workbook('processed_data.xlsx')
```

### Basic Usage - Command Line Interface

```bash
# Auto-process a file with default settings
python cli/excel_automation.py auto-process input.xlsx --output cleaned.xlsx

# Clean data with specific operations
python cli/excel_automation.py clean input.xlsx --remove-duplicates --normalize-columns

# Create analysis with pivot tables
python cli/excel_automation.py analyze input.xlsx --pivot-table "Sales" --group-by "Region" "Product"

# Add visualizations
python cli/excel_automation.py visualize input.xlsx --chart-type bar --sheet-name "Sales" --data-range "A1:C10"

# Batch process multiple files
python cli/excel_automation.py batch-process ./excel_files/ --output-dir ./processed/

# Create configuration template
python cli/excel_automation.py create-config --template advanced --output config.json
```

## Configuration System

### JSON Configuration Format

```json
{
  "data_cleaning": {
    "remove_duplicates": true,
    "standardize_dates": true,
    "clean_text_casing": "title",
    "normalize_columns": true,
    "date_columns": ["Date", "Created", "Modified"],
    "text_columns": ["Name", "Description", "Category"],
    "currency_columns": ["Price", "Cost", "Amount"]
  },
  "analysis": {
    "create_pivot_tables": true,
    "generate_summaries": true,
    "apply_filters": true,
    "highlight_outliers": true
  },
  "visualization": {
    "create_charts": true,
    "apply_conditional_formatting": true,
    "create_dashboards": true,
    "chart_types": ["bar", "line", "pie"]
  },
  "navigation": {
    "create_toc": true,
    "add_nav_buttons": true,
    "toc_threshold": 6
  }
}
```

### Using Configuration

```python
# Load configuration
config = ExcelConfigV1()
config.load_from_json('my_config.json')

# Use with processor
result_path = auto_clean_excel_file('input.xlsx', config=config)
```

## API Reference

### ExcelProcessorV1 Class

#### Core Methods

- `__init__(filepath, debug=False)` - Initialize processor
- `load_workbook()` - Load Excel workbook 
- `save_workbook(output_path=None)` - Save workbook

#### Data Cleaning Methods

- `remove_duplicates_from_sheet(sheet_name, columns=None, keep_first=True)` - Remove duplicates
- `standardize_date_formats(sheet_name, date_columns, target_format="MM/DD/YYYY")` - Standardize dates
- `clean_text_casing(sheet_name, text_columns, case_type="title")` - Clean text casing
- `normalize_column_names(sheet_name)` - Normalize column names

#### Sheet Management Methods

- `split_sheet_by_column(sheet_name, split_column, prefix="Sheet")` - Split sheet by column values
- `merge_sheets(sheet_names, target_sheet_name, remove_source=False)` - Merge multiple sheets
- `create_table_of_contents(toc_sheet_name="Table of Contents")` - Create TOC
- `add_navigation_buttons(toc_sheet_name)` - Add navigation buttons

#### Analysis Methods

- `create_pivot_table_from_data(source_sheet, target_sheet, rows, columns=None, values=None, aggfunc='sum')` - Create pivot table
- `filter_column_by_value_range(sheet_name, column_name, min_value=None, max_value=None)` - Filter by range
- `highlight_cells_by_value_range(sheet_name, column_name, min_value=None, max_value=None, highlight_color="FFFF00")` - Highlight cells

#### Visualization Methods  

- `create_chart_from_data(sheet_name, chart_type, data_range, chart_title, x_axis_title, y_axis_title)` - Create chart
- `apply_conditional_formatting(sheet_name, data_range, rule_type, format_style)` - Apply formatting
- `create_summary_sheet(source_sheets, summary_sheet_name="Summary", include_charts=True)` - Create summary

### ExcelConfigV1 Class

- `__init__()` - Initialize configuration with defaults
- `load_from_json(config_path)` - Load from JSON file
- `save_to_json(config_path)` - Save to JSON file

### Utility Functions

- `auto_clean_excel_file(filepath, config=None, output_path=None)` - Auto-clean with config
- `batch_process_excel_files(directory_path, config=None, output_directory=None)` - Batch process
- `create_example_config()` - Create example configuration

## Command Line Reference

### Global Options
- `--debug, -d` - Enable debug logging
- `--config CONFIG, -c` - Path to JSON configuration file  
- `--output OUTPUT, -o` - Output file path

### Commands

#### clean
Clean Excel data (remove duplicates, standardize formats)
```bash
excel_automation clean INPUT_FILE [options]
```
Options:
- `--remove-duplicates` - Remove duplicate rows
- `--normalize-columns` - Normalize column names
- `--standardize-dates` - Standardize date formats
- `--clean-text {title,upper,lower,proper}` - Standardize text casing
- `--date-format FORMAT` - Target date format

#### analyze  
Analyze Excel data (pivot tables, filters, summaries)
```bash
excel_automation analyze INPUT_FILE [options]
```
Options:
- `--pivot-table SHEET` - Create pivot table for sheet
- `--group-by COLUMNS` - Columns to group by
- `--sum-columns COLUMNS` - Columns to sum
- `--filter-column COLUMN` - Column to filter
- `--filter-min VALUE` - Minimum filter value
- `--filter-max VALUE` - Maximum filter value
- `--create-summary` - Create summary sheet

#### visualize
Create charts and visualizations
```bash  
excel_automation visualize INPUT_FILE [options]
```
Options:
- `--chart-type {bar,line,pie}` - Chart type
- `--sheet-name SHEET` - Source sheet name
- `--data-range RANGE` - Data range (e.g., A1:C10)
- `--chart-title TITLE` - Chart title
- `--conditional-formatting` - Apply conditional formatting

#### auto-process
Automatically process with full feature set
```bash
excel_automation auto-process INPUT_FILE [options] 
```
Options:
- `--create-toc` - Create table of contents

#### batch-process
Process multiple files in directory
```bash
excel_automation batch-process INPUT_DIR [options]
```
Options:
- `--output-dir DIR` - Output directory
- `--file-pattern PATTERN` - File pattern (e.g., *.xlsx)

#### create-config
Create configuration file
```bash
excel_automation create-config [options]
```
Options:
- `--template {basic,advanced}` - Configuration template
- `--output PATH` - Output file path

## Examples

### Example 1: Sales Data Processing

```python
# Process monthly sales data
processor = ExcelProcessorV1('monthly_sales.xlsx')
processor.load_workbook()

# Clean the data
processor.remove_duplicates_from_sheet('Sales')
processor.normalize_column_names('Sales') 
processor.standardize_date_formats('Sales', ['Sale_Date'])

# Create analysis
processor.create_pivot_table_from_data(
    source_sheet='Sales',
    target_sheet='Sales_Summary',
    rows=['Region', 'Salesperson'], 
    values=['Amount'],
    aggfunc='sum'
)

# Add filtering and highlighting
processor.filter_column_by_value_range('Sales', 'Amount', min_value=1000)
processor.highlight_cells_by_value_range('Sales', 'Amount', min_value=5000)

# Create visualizations
processor.create_chart_from_data(
    sheet_name='Sales_Summary',
    chart_type='bar',
    data_range='A1:C10',
    chart_title='Sales by Region'
)

processor.save_workbook('processed_sales.xlsx')
```

### Example 2: Multi-file Customer Data Processing

```bash
# Create advanced configuration
python cli/excel_automation.py create-config --template advanced --output customer_config.json

# Process all customer files in directory
python cli/excel_automation.py batch-process ./customer_data/ \
    --config customer_config.json \
    --output-dir ./processed_customers/
```

### Example 3: Automated Report Generation

```python
# Configuration for automated reporting
config = ExcelConfigV1()
config.analysis['create_pivot_tables'] = True
config.visualization['create_charts'] = True
config.navigation['create_toc'] = True

# Process multiple report files  
import glob
for file_path in glob.glob('reports/*.xlsx'):
    try:
        result = auto_clean_excel_file(file_path, config=config)
        print(f"✅ Processed: {result}")
    except Exception as e:
        print(f"❌ Failed to process {file_path}: {e}")
```

## Error Handling

The framework provides comprehensive error handling and logging:

```python
import logging
import os

# Enable debug logging
os.environ["DEBUG"] = "1"

try:
    processor = ExcelProcessorV1('data.xlsx', debug=True)
    processor.load_workbook()
    # ... operations
    processor.save_workbook()
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
except ValueError as e:
    logging.error(f"Invalid data: {e}")  
except Exception as e:
    logging.error(f"Unexpected error: {e}")
```

## Best Practices

1. **Always use debug mode** during development for detailed logging
2. **Validate input data** before processing large datasets
3. **Use configuration files** for complex, repeatable workflows
4. **Test with sample data** before processing production files
5. **Create backups** of important files before processing
6. **Use appropriate chart types** for your data visualization needs
7. **Leverage batch processing** for multiple files with similar structure

## Troubleshooting

### Common Issues

**Issue**: ImportError when running tests
**Solution**: Ensure all dependencies are installed and paths are correct

**Issue**: Memory errors with large Excel files  
**Solution**: Process files in chunks or increase available memory

**Issue**: Charts not displaying correctly
**Solution**: Verify data range format and chart type compatibility

**Issue**: Configuration not being applied
**Solution**: Check JSON syntax and configuration file path

### Getting Help

- Check debug logs by enabling debug mode
- Verify file paths and permissions
- Ensure Excel file is not open in another application
- Review configuration JSON for syntax errors

For additional support, refer to the Framework0 documentation and logging output.