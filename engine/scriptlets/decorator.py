# engine/scriptlets/decorator.py
# This module defines various decorators used in the IAF0 framework for scriptlets and analysis.
# Decorators enhance functionality without modifying core logic, following the decorator pattern.
# Key decorators include:
# - @track_resources: Monitors execution time, CPU, and memory usage, logging to stderr.
# - @debug_trace: Captures inputs, outputs, variable changes (diffs), and exceptions for verbose debugging.
# - @cache_analysis: Caches results of expensive computations, especially in analysis modules.
# These are applied to scriptlet run methods or analysis functions.
# The module uses standard libraries and third-party ones like psutil for resource monitoring.
# Decorators preserve original function metadata using functools.wraps.

import functools  # Imported for wraps to preserve function metadata in decorators.
import time  # Imported for measuring execution time in track_resources.
import psutil  # Imported for monitoring CPU and memory usage.
import json  # Imported for serializing diffs and traces in debug_trace.
import inspect  # Imported for inspecting function signatures and arguments in debug_trace.
import logging  # Imported for logging resource usage and debug traces.
from typing import Any, Callable, Dict, List  # Imported for type hints to improve code clarity.
import joblib  # Imported for persistent caching in @cache_analysis (file-based if needed).

# Set up module-level logger for decorator events.
logger = logging.getLogger(__name__)  # Creates a logger named after the module for consistency.

def track_resources(func: Callable) -> Callable:
    # Decorator to track resources: time, CPU, memory.
    # Logs usage to stderr after function execution.
    # Args:
    #   func: The function to decorate.
    # Returns: Wrapped function.
    @functools.wraps(func)  # Preserves original function's name, docstring, etc.
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Wrapper function that adds resource tracking.
        start_time = time.time()  # Records start time for duration calculation.
        start_cpu = psutil.cpu_percent()  # Records initial CPU usage %.
        start_mem = psutil.Process(os.getpid()).memory_info().rss  # Records initial memory usage in bytes (RSS).
        
        result = func(*args, **kwargs)  # Calls the original function with args and kwargs.
        
        end_time = time.time()  # Records end time.
        end_cpu = psutil.cpu_percent()  # Records final CPU usage %.
        end_mem = psutil.Process(os.getpid()).memory_info().rss  # Records final memory usage.
        
        duration = end_time - start_time  # Calculates execution duration in seconds.
        cpu_delta = end_cpu - start_cpu  # Calculates CPU usage delta (approximate).
        mem_delta = end_mem - start_mem  # Calculates memory usage delta in bytes.
        
        log_msg = f"[resource] duration_sec={duration:.2f}, cpu_delta={cpu_delta:.2f}%, mem_delta={mem_delta / 1024:.2f}KB"  # Formats log message.
        print(log_msg, file=sys.stderr)  # Prints to stderr as per framework logging pattern.
        logger.info(log_msg)  # Logs the message for potential aggregation.
        
        return result  # Returns the original function's result.
    return wrapper  # Returns the wrapped function.

def debug_trace(func: Callable) -> Callable:
    # Decorator for debug tracing: captures inputs, outputs, var changes, exceptions.
    # Logs structured JSON diffs to stderr when in debug mode.
    # Args:
    #   func: Function to decorate.
    # Returns: Wrapped function.
    @functools.wraps(func)  # Preserves metadata.
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Wrapper that adds tracing.
        if not os.environ.get('DEBUG_MODE', 'false').lower() == 'true':  # Checks if debug mode is enabled via env var.
            return func(*args, **kwargs)  # Early return if not in debug mode.
        
        # Capture inputs.
        sig = inspect.signature(func)  # Gets the function signature for arg binding.
        bound_args = sig.bind(*args, **kwargs)  # Binds args to parameters.
        inputs = bound_args.arguments  # Gets dict of input arguments.
        logger.debug(f"Inputs: {json.dumps(inputs)}")  # Logs inputs as JSON.
        
        try:  # Starts try block for execution and exception capture.
            result = func(*args, **kwargs)  # Calls original function.
            # Capture outputs (assume result is output; extend for more).
            outputs = {'result': result}  # Wraps result in dict for logging.
            logger.debug(f"Outputs: {json.dumps(outputs)}")  # Logs outputs.
            
            # Variable diffs (example: assume ctx in args; track changes).
            if 'ctx' in inputs:  # Checks if context is in args (common in scriptlets).
                ctx_before = inputs['ctx'].to_dict().copy()  # Copies context before (assumes to_dict method).
                ctx_after = inputs['ctx'].to_dict()  # Gets context after (post-run).
                diffs = {k: {'before': ctx_before.get(k), 'after': v} for k, v in ctx_after.items() if ctx_before.get(k) != v}  # Computes diffs.
                if diffs:  # If there are changes.
                    diff_log = {"event": "var_change", "step": func.__name__, "diffs": diffs, "timestamp": time.time()}  # Creates diff log dict.
                    print(json.dumps(diff_log), file=sys.stderr)  # Prints structured diff to stderr.
                    logger.debug(json.dumps(diff_log))  # Logs the diff.
            
            return result  # Returns the result.
        except Exception as e:  # Catches exceptions.
            exc_log = {"event": "exception", "step": func.__name__, "error": str(e), "timestamp": time.time()}  # Creates exception log.
            print(json.dumps(exc_log), file=sys.stderr)  # Prints to stderr.
            logger.error(json.dumps(exc_log))  # Logs the error.
            raise  # Re-raises the exception.
    return wrapper  # Returns the wrapped function.

def cache_analysis(func: Callable) -> Callable:
    # Decorator for caching analysis computations.
    # Uses joblib.Memory for persistent caching (file-based).
    # Args:
    #   func: Function to cache.
    # Returns: Cached wrapped function.
    memory = joblib.Memory(location='cache_dir', verbose=0)  # Creates a Memory instance with cache directory (created if needed).
    cached_func = memory.cache(func)  # Caches the function using joblib.
    
    @functools.wraps(func)  # Preserves metadata.
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Wrapper that calls the cached function.
        return cached_func(*args, **kwargs)  # Executes the cached version.
    return wrapper  # Returns the wrapped cached function.

# No additional code; this module provides decorators for use in scriptlets and analysis.
# In IAF0, these are imported and applied in steps/ (e.g., @track_resources on run).
# For example, in compute_numbers.py: @track_resources def run(self, ...).
# Cache_analysis is used in analysis/ modules like summarizer.py for repeated computations.