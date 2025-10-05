#!/usr/bin/env python3
"""
Framework0 Scriptlet: ComputeNumbers

This scriptlet processes numerical data from CSV files and calculates
basic statistics, storing results in the Framework0 context system.

Module: engine.steps.python.compute_numbers
Class: ComputeNumbers
"""

import os  # For environment variable access
import csv  # For CSV file processing
import statistics  # For statistical calculations
from pathlib import Path  # For path handling
from typing import Dict, List  # For type annotations

try:
    from scriptlets.framework import BaseScriptlet  # Framework0 base class
except ImportError:
    # Fallback base class if framework not available
    class BaseScriptlet:
        """Fallback base scriptlet class."""
        
        def __init__(self, context=None, **kwargs):
            """Initialize base scriptlet."""
            self.context = context
            self.logger = None
            
        def run(self, **kwargs):
            """Run method must be implemented by subclasses."""
            raise NotImplementedError("Scriptlet must implement run method")


class ComputeNumbers(BaseScriptlet):
    """
    Scriptlet for processing numerical data from CSV files.
    
    This scriptlet reads CSV files containing numerical data,
    extracts numbers, calculates basic statistics, and stores
    results in the Framework0 context for use by other components.
    """
    
    def __init__(self, context=None, **kwargs):
        """Initialize ComputeNumbers scriptlet."""
        super().__init__(context, **kwargs)  # Initialize base class
        
    def run(self, context, args, **kwargs) -> int:
        """
        Execute ComputeNumbers scriptlet processing.
        
        Args:
            **kwargs: Scriptlet arguments including 'src' for data source
            
        Returns:
            Dict[str, any]: Execution results with statistics
        """
        try:
            # Get source file path from arguments
            src_path = args.get('src', 'orchestrator/Data/numbers.csv')
            
            self._log_info(f"Processing data file: {src_path}")
            
            # Convert to absolute path for better resolution
            if not os.path.isabs(src_path):
                # Try different base paths
                base_paths = [
                    Path.cwd(),
                    Path.cwd().parent if Path.cwd().name == 'isolated_recipe' else Path.cwd(),
                ]
                
                resolved_path = None
                for base_path in base_paths:
                    candidate = base_path / src_path
                    if candidate.exists():
                        resolved_path = candidate
                        break
                
                if resolved_path:
                    src_path = str(resolved_path)
                else:
                    self._log_error(f"Data file not found: {src_path}")
                    return 1  # Error exit code
            
            # Check if source file exists
            if not Path(src_path).exists():
                error_msg = f"Data file not found: {src_path}"
                self._log_error(error_msg)
                return 1  # Error exit code
            
            # Read and process CSV data
            numbers = self._read_csv_data(src_path)
            if not numbers:
                error_msg = "No valid numbers found in data file"
                self._log_error(error_msg)
                return 1  # Error exit code
            
            # Calculate statistics
            stats = self._calculate_statistics(numbers)
            
            # Store results in context
            if context:
                context.set("numbers.stats_v1", stats, who="compute_numbers")
                context.set("numbers.count", len(numbers), who="compute_numbers")
                context.set("numbers.source", src_path, who="compute_numbers")
            
            self._log_info(f"Successfully processed {len(numbers)} numbers")
            self._log_info(f"Statistics: {stats}")
            
            return 0  # Success exit code
        
        except Exception as e:
            error_msg = f"ComputeNumbers execution failed: {e}"
            self._log_error(error_msg)
            return 1  # Error exit code
    
    def _read_csv_data(self, file_path: str) -> List[float]:
        """
        Read numerical data from CSV file.
        
        Args:
            file_path: Path to CSV file to read
            
        Returns:
            List[float]: List of numbers extracted from CSV
        """
        numbers = []  # Store extracted numbers
        
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                # Try to detect delimiter
                sample = csvfile.read(1024)
                csvfile.seek(0)
                
                # Use csv.Sniffer to detect format
                try:
                    dialect = csv.Sniffer().sniff(sample)
                    reader = csv.reader(csvfile, dialect)
                except Exception:
                    # Fallback to comma delimiter
                    reader = csv.reader(csvfile)
                
                # Read rows and extract numbers
                for row_idx, row in enumerate(reader):
                    for col_idx, cell in enumerate(row):
                        try:
                            # Try to convert cell to number
                            number = float(cell.strip())
                            numbers.append(number)
                        except (ValueError, AttributeError):
                            # Skip non-numeric cells
                            continue
            
            self._log_info(f"Extracted {len(numbers)} numbers from CSV")
            
        except Exception as e:
            self._log_error(f"Failed to read CSV file {file_path}: {e}")
        
        return numbers
    
    def _calculate_statistics(self, numbers: List[float]) -> Dict[str, float]:
        """
        Calculate basic statistics for list of numbers.
        
        Args:
            numbers: List of numbers to analyze
            
        Returns:
            Dict[str, float]: Dictionary of calculated statistics
        """
        if not numbers:
            return {"count": 0}
        
        stats = {
            "count": len(numbers),
            "sum": sum(numbers),
            "mean": statistics.mean(numbers),
            "median": statistics.median(numbers),
            "min": min(numbers),
            "max": max(numbers),
        }
        
        # Add standard deviation if we have multiple values
        if len(numbers) > 1:
            stats["stdev"] = statistics.stdev(numbers)
        else:
            stats["stdev"] = 0.0
        
        return stats
    
    def _log_info(self, message: str) -> None:
        """Log info message using available logger."""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"INFO: ComputeNumbers: {message}")
    
    def _log_error(self, message: str) -> None:
        """Log error message using available logger."""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"ERROR: ComputeNumbers: {message}")


# Export the scriptlet class
__all__ = ["ComputeNumbers"]