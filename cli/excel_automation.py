#!/usr/bin/env python3
# cli/excel_automation.py

"""
Excel Automation Command Line Interface for Framework0.

This module provides a comprehensive CLI for Excel processing and automation
tasks. It supports all major features of the Excel processor including data
cleaning, analysis, visualization, and batch processing operations.

The CLI can be run independently with command line arguments or with JSON
configuration files for complex automation workflows.

Usage Examples:
    # Basic cleaning
    python cli/excel_automation.py clean input.xlsx --output cleaned.xlsx
    
    # Full automation with config
    python cli/excel_automation.py auto-process input.xlsx --config automation_config.json
    
    # Batch processing
    python cli/excel_automation.py batch-process /path/to/excel/files --output-dir /path/to/output

Features:
- Standalone CLI operation with comprehensive argument parsing
- JSON configuration support for complex workflows
- Batch processing capabilities for multiple files
- Integration with Framework0 logging and error handling
- Modular command structure for specific operations
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Framework0 imports
from analysis.excel_processor import (
    ExcelProcessorV1, 
    ExcelConfigV1, 
    auto_clean_excel_file, 
    batch_process_excel_files
)
from src.core.logger import get_logger

# Initialize module logger
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class ExcelAutomationCLI:
    """
    Command line interface for Excel automation operations.
    
    Provides structured CLI with subcommands for different Excel processing
    operations including cleaning, analysis, visualization, and batch processing.
    """
    
    def __init__(self) -> None:
        """Initialize CLI with argument parser and configuration."""
        # Initialize CLI state
        self.parser: argparse.ArgumentParser = self._create_argument_parser()
        self.config: Optional[ExcelConfigV1] = None
        self.debug: bool = False
        
        # Setup logger
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info("Excel Automation CLI initialized")

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        """
        Create comprehensive argument parser for CLI operations.
        
        Returns:
            argparse.ArgumentParser: Configured argument parser
        """
        # Create main parser
        parser = argparse.ArgumentParser(
            prog='excel_automation',
            description='Excel Automation CLI for Framework0',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s clean input.xlsx --output cleaned.xlsx
  %(prog)s analyze input.xlsx --pivot-table "Sales" --group-by "Region"
  %(prog)s visualize input.xlsx --chart-type bar --data-range "A1:C10"
  %(prog)s auto-process input.xlsx --config config.json
  %(prog)s batch-process ./excel_files/ --output-dir ./processed/
  %(prog)s create-config --output excel_config.json
            """
        )
        
        # Global arguments
        parser.add_argument('--debug', '-d', action='store_true',
                          help='Enable debug logging')
        parser.add_argument('--config', '-c', type=str,
                          help='Path to JSON configuration file')
        parser.add_argument('--output', '-o', type=str,
                          help='Output file path')
        
        # Create subparsers for different commands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Clean command
        self._add_clean_command(subparsers)
        
        # Analyze command  
        self._add_analyze_command(subparsers)
        
        # Visualize command
        self._add_visualize_command(subparsers)
        
        # Auto-process command
        self._add_auto_process_command(subparsers)
        
        # Batch processing command
        self._add_batch_process_command(subparsers)
        
        # Configuration command
        self._add_config_command(subparsers)
        
        return parser

def _add_clean_command(self, subparsers: Any) -> None:
        """Add data cleaning subcommand."""
        # Create clean subcommand parser
        clean_parser = subparsers.add_parser('clean', 
                                           help='Clean Excel data (remove duplicates, standardize formats)')
        clean_parser.add_argument('input_file', help='Input Excel file path')
        clean_parser.add_argument('--remove-duplicates', action='store_true', default=True,
                                help='Remove duplicate rows')
        clean_parser.add_argument('--normalize-columns', action='store_true', default=True,
                                help='Normalize column names')
        clean_parser.add_argument('--standardize-dates', action='store_true', default=True,
                                help='Standardize date formats')
        clean_parser.add_argument('--clean-text', choices=['title', 'upper', 'lower', 'proper'],
                                help='Standardize text casing')
        clean_parser.add_argument('--date-format', default='MM/DD/YYYY',
                                help='Target date format')

def _add_analyze_command(self, subparsers: Any) -> None:
        """Add data analysis subcommand."""
        # Create analyze subcommand parser
        analyze_parser = subparsers.add_parser('analyze', 
                                            help='Analyze Excel data (pivot tables, filters, summaries)')
        analyze_parser.add_argument('input_file', help='Input Excel file path')
        analyze_parser.add_argument('--pivot-table', type=str,
                                  help='Create pivot table for specified sheet')
        analyze_parser.add_argument('--group-by', nargs='+',
                                  help='Columns to group by in pivot table')
        analyze_parser.add_argument('--sum-columns', nargs='+',
                                  help='Columns to sum in pivot table')
        analyze_parser.add_argument('--filter-column', type=str,
                                  help='Column to filter')
        analyze_parser.add_argument('--filter-min', type=float,
                                  help='Minimum value for filter')
        analyze_parser.add_argument('--filter-max', type=float,
                                  help='Maximum value for filter')
        analyze_parser.add_argument('--create-summary', action='store_true',
                                  help='Create summary sheet')

def _add_visualize_command(self, subparsers: Any) -> None:
        """Add visualization subcommand."""
        # Create visualize subcommand parser
        viz_parser = subparsers.add_parser('visualize',
                                         help='Create charts and visualizations')
        viz_parser.add_argument('input_file', help='Input Excel file path')
        viz_parser.add_argument('--chart-type', choices=['bar', 'line', 'pie'], default='bar',
                              help='Type of chart to create')
        viz_parser.add_argument('--sheet-name', type=str,
                              help='Sheet containing data for chart')
        viz_parser.add_argument('--data-range', type=str,
                              help='Excel range for chart data (e.g., A1:C10)')
        viz_parser.add_argument('--chart-title', type=str, default='Chart',
                              help='Title for the chart')
        viz_parser.add_argument('--conditional-formatting', action='store_true',
                              help='Apply conditional formatting')

def _add_auto_process_command(self, subparsers: Any) -> None:
        """Add auto-processing subcommand."""
        # Create auto-process subcommand parser
        auto_parser = subparsers.add_parser('auto-process',
                                          help='Automatically process Excel file with full feature set')
        auto_parser.add_argument('input_file', help='Input Excel file path')
        auto_parser.add_argument('--create-toc', action='store_true', default=True,
                               help='Create table of contents for multi-sheet files')

def _add_batch_process_command(self, subparsers: Any) -> None:
        """Add batch processing subcommand."""
        # Create batch processing subcommand parser
        batch_parser = subparsers.add_parser('batch-process',
                                           help='Process multiple Excel files in directory')
        batch_parser.add_argument('input_directory', help='Directory containing Excel files')
        batch_parser.add_argument('--output-dir', type=str,
                                help='Output directory for processed files')
        batch_parser.add_argument('--file-pattern', type=str, default='*.xlsx',
                                help='File pattern to match (e.g., *.xlsx, *.xls)')

def _add_config_command(self, subparsers: Any) -> None:
        """Add configuration management subcommand."""
        # Create config subcommand parser
        config_parser = subparsers.add_parser('create-config',
                                            help='Create example configuration file')
        config_parser.add_argument('--template', choices=['basic', 'advanced'], default='basic',
                                 help='Configuration template type')
        config_parser.add_argument('--output', '-o', type=str,
                                 help='Output path for configuration file')

    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI with provided arguments.
        
        Args:
            args (Optional[List[str]]): Command line arguments, uses sys.argv if None
            
        Returns:
            int: Exit code (0 for success, 1 for error)
        """
        try:
            # Parse arguments
            parsed_args = self.parser.parse_args(args)
            
            # Set debug mode
            self.debug = parsed_args.debug
            if self.debug:
                os.environ["DEBUG"] = "1"
                self.logger = get_logger(f"{__name__}.{self.__class__.__name__}", debug=True)
            
            # Load configuration if provided
            if hasattr(parsed_args, 'config') and parsed_args.config:
                self._load_config(parsed_args.config)
            
            # Execute command
            if parsed_args.command == 'clean':
                return self._execute_clean_command(parsed_args)
            elif parsed_args.command == 'analyze':
                return self._execute_analyze_command(parsed_args)
            elif parsed_args.command == 'visualize':
                return self._execute_visualize_command(parsed_args)
            elif parsed_args.command == 'auto-process':
                return self._execute_auto_process_command(parsed_args)
            elif parsed_args.command == 'batch-process':
                return self._execute_batch_process_command(parsed_args)
            elif parsed_args.command == 'create-config':
                return self._execute_create_config_command(parsed_args)
            else:
                self.parser.print_help()
                return 1
                
        except KeyboardInterrupt:
            self.logger.info("Operation cancelled by user")
            return 1
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return 1

    def _load_config(self, config_path: str) -> None:
        """
        Load configuration from JSON file.
        
        Args:
            config_path (str): Path to configuration file
        """
        try:
            # Load and validate configuration
            self.config = ExcelConfigV1().load_from_json(config_path)
            self.logger.info(f"Loaded configuration from: {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise

def _execute_clean_command(self, args: Any) -> int:
        """
        Execute data cleaning command.
        
        Args:
            args: Parsed command arguments
            
        Returns:
            int: Exit code
        """
        try:
            # Validate input file exists
            if not Path(args.input_file).exists():
                raise FileNotFoundError(f"Input file not found: {args.input_file}")
            
            # Initialize processor
            processor = ExcelProcessorV1(args.input_file, debug=self.debug)
            processor.load_workbook()
            
            # Apply cleaning operations
            for sheet_name in processor.workbook.sheetnames:
                if args.remove_duplicates:
                    # Remove duplicates from each sheet
                    removed = processor.remove_duplicates_from_sheet(sheet_name)
                    self.logger.info(f"Removed {removed} duplicates from '{sheet_name}'")
                
                if args.normalize_columns:
                    # Normalize column names  
                    mappings = processor.normalize_column_names(sheet_name)
                    if mappings:
                        self.logger.info(f"Normalized {len(mappings)} columns in '{sheet_name}'")
                
                if args.clean_text:
                    # Get text columns (assume all string columns for now)
                    # In a real implementation, this would be more sophisticated
                    worksheet = processor.workbook[sheet_name]
                    headers = [cell.value for cell in worksheet[1] if cell.value]
                    processed = processor.clean_text_casing(sheet_name, headers, args.clean_text)
                    self.logger.info(f"Processed {processed} text cells in '{sheet_name}'")
            
            # Save processed file
            output_path = args.output or args.input_file
            processor.save_workbook(output_path)
            
            self.logger.info(f"✅ Cleaning completed: {output_path}")
            return 0
            
        except Exception as e:
            self.logger.error(f"Clean command failed: {e}")
            return 1

def _execute_analyze_command(self, args: Any) -> int:
        """
        Execute data analysis command.
        
        Args:
            args: Parsed command arguments
            
        Returns:
            int: Exit code
        """
        try:
            # Validate input file
            if not Path(args.input_file).exists():
                raise FileNotFoundError(f"Input file not found: {args.input_file}")
            
            # Initialize processor
            processor = ExcelProcessorV1(args.input_file, debug=self.debug)
            processor.load_workbook()
            
            # Create pivot table if requested
            if args.pivot_table and args.group_by:
                target_sheet = f"{args.pivot_table}_Pivot"
                processor.create_pivot_table_from_data(
                    source_sheet=args.pivot_table,
                    target_sheet=target_sheet,
                    rows=args.group_by,
                    values=args.sum_columns or [],
                    aggfunc='sum'
                )
                self.logger.info(f"Created pivot table in sheet '{target_sheet}'")
            
            # Apply filtering if requested
            if args.filter_column and (args.filter_min is not None or args.filter_max is not None):
                for sheet_name in processor.workbook.sheetnames:
                    try:
                        filtered_count = processor.filter_column_by_value_range(
                            sheet_name=sheet_name,
                            column_name=args.filter_column,
                            min_value=args.filter_min,
                            max_value=args.filter_max
                        )
                        self.logger.info(f"Filtered to {filtered_count} rows in '{sheet_name}'")
                    except KeyError:
                        # Column not found in this sheet, skip
                        continue
            
            # Create summary sheet if requested
            if args.create_summary:
                summary_sheet = processor.create_summary_sheet(
                    source_sheets=processor.workbook.sheetnames,
                    include_charts=True
                )
                self.logger.info(f"Created summary sheet: {summary_sheet}")
            
            # Save processed file
            output_path = args.output or args.input_file
            processor.save_workbook(output_path)
            
            self.logger.info(f"✅ Analysis completed: {output_path}")
            return 0
            
        except Exception as e:
            self.logger.error(f"Analyze command failed: {e}")
            return 1

def _execute_visualize_command(self, args: Any) -> int:
        """
        Execute visualization command.
        
        Args:
            args: Parsed command arguments
            
        Returns:
            int: Exit code
        """
        try:
            # Validate input file
            if not Path(args.input_file).exists():
                raise FileNotFoundError(f"Input file not found: {args.input_file}")
            
            # Initialize processor
            processor = ExcelProcessorV1(args.input_file, debug=self.debug)
            processor.load_workbook()
            
            # Create chart if requested
            if args.data_range and args.sheet_name:
                chart_id = processor.create_chart_from_data(
                    sheet_name=args.sheet_name,
                    chart_type=args.chart_type,
                    data_range=args.data_range,
                    chart_title=args.chart_title
                )
                self.logger.info(f"Created chart: {chart_id}")
            
            # Apply conditional formatting if requested
            if args.conditional_formatting and args.data_range and args.sheet_name:
                formatted_cells = processor.apply_conditional_formatting(
                    sheet_name=args.sheet_name,
                    data_range=args.data_range,
                    rule_type="color_scale"
                )
                self.logger.info(f"Applied conditional formatting to {formatted_cells} cells")
            
            # Save processed file
            output_path = args.output or args.input_file
            processor.save_workbook(output_path)
            
            self.logger.info(f"✅ Visualization completed: {output_path}")
            return 0
            
        except Exception as e:
            self.logger.error(f"Visualize command failed: {e}")
            return 1

def _execute_auto_process_command(self, args: Any) -> int:
        """
        Execute auto-processing command.
        
        Args:
            args: Parsed command arguments
            
        Returns:
            int: Exit code
        """
        try:
            # Use configuration if available, otherwise use defaults
            config = self.config if self.config else ExcelConfigV1()
            
            # Update config with command line arguments
            if args.create_toc:
                config.navigation["create_toc"] = True
                config.navigation["add_nav_buttons"] = True
            
            # Execute auto-cleaning
            output_path = auto_clean_excel_file(
                filepath=args.input_file,
                config=config,
                output_path=args.output
            )
            
            self.logger.info(f"✅ Auto-processing completed: {output_path}")
            return 0
            
        except Exception as e:
            self.logger.error(f"Auto-process command failed: {e}")
            return 1

def _execute_batch_process_command(self, args: Any) -> int:
        """
        Execute batch processing command.
        
        Args:
            args: Parsed command arguments
            
        Returns:
            int: Exit code
        """
        try:
            # Validate input directory
            if not Path(args.input_directory).exists():
                raise FileNotFoundError(f"Input directory not found: {args.input_directory}")
            
            # Use configuration if available
            config = self.config if self.config else ExcelConfigV1()
            
            # Execute batch processing
            processed_files = batch_process_excel_files(
                directory_path=args.input_directory,
                config=config,
                output_directory=args.output_dir
            )
            
            self.logger.info(f"✅ Batch processing completed: {len(processed_files)} files processed")
            return 0
            
        except Exception as e:
            self.logger.error(f"Batch process command failed: {e}")
            return 1

def _execute_create_config_command(self, args: Any) -> int:
        """
        Execute configuration creation command.
        
        Args:
            args: Parsed command arguments
            
        Returns:
            int: Exit code
        """
        try:
            # Create configuration based on template
            config = ExcelConfigV1()
            
            if args.template == 'advanced':
                # Customize for advanced use case
                config.data_cleaning.update({
                    "date_columns": ["Date", "Created", "Modified", "Timestamp"],
                    "text_columns": ["Name", "Description", "Category", "Notes"],
                    "currency_columns": ["Price", "Cost", "Amount", "Total"]
                })
                config.analysis.update({
                    "auto_pivot_tables": True,
                    "generate_summaries": True,
                    "apply_filters": True
                })
                config.visualization.update({
                    "auto_charts": True,
                    "conditional_formatting": True,
                    "create_dashboards": True
                })
            
            # Save configuration file
            output_path = args.output or f"excel_automation_config_{args.template}.json"
            config.save_to_json(output_path)
            
            self.logger.info(f"✅ Configuration file created: {output_path}")
            return 0
            
        except Exception as e:
            self.logger.error(f"Create config command failed: {e}")
            return 1


def main() -> int:
    """
    Main entry point for Excel automation CLI.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    # Create and run CLI
    cli = ExcelAutomationCLI()
    return cli.run()


if __name__ == '__main__':
    # Execute CLI if run directly
    sys.exit(main())