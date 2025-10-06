# context.sh - Shell Script Manual

## Overview
**File Path:** `tools/context.sh`  
**File Type:** Shell Script  
**Last Modified:** 2025-10-04T23:19:13.986420  
**File Size:** 21,312 bytes  

## Description
Context Server Shell Client - Cross-Platform Context Management This shell script provides a simple command-line interface for interacting with the Framework0 Enhanced Context Server. Supports get/set operations, monitoring, and debugging features for shell scripts and automation. Default configuration - can be overridden by environment variables

## Purpose and Application
This shell script is part of the Framework0 system and provides automation capabilities for:

### Key Features
1. **local: Log level: INFO, WARN, ERROR, DEBUG**
2. **local: Message content to log**
3. **return: Skip non-error messages in quiet mode**
4. **fi: Current timestamp for log entry**
5. **local: Color code for the log level**
6. **return: Skip debug messages unless verbose mode enabled**
7. **fi: Output to stderr with color**
8. **local: Array to track missing dependencies**
9. **fi: Check for jq (optional but recommended for JSON processing)**
10. **fi: Report missing critical dependencies**
11. **if: missing_deps[@]} -gt 0 ]]; then**
12. **return: Return connection error code**
13. **local: Input value to parse as JSON**
14. **echo: Valid JSON, return as-is**
15. **fi: Fallback: try to detect if input looks like JSON**
16. **echo: Looks like JSON, return as-is**
17. **fi: Not JSON, wrap as string value**
18. **local: Content to format**
19. **local: Desired format: json, pretty, plain, auto**
20. **echo: Colorized pretty JSON**
21. **else: Fallback to raw JSON**
22. **echo: Extract value field**
23. **else: Fallback to raw content**
24. **echo: Pretty format for terminal**
25. **else: Raw format for pipes/scripts**
26. **local: HTTP method: GET, POST, PUT, DELETE**
27. **local: API endpoint path**
28. **local: Request body data (optional)**
29. **local: Attribution for the request**
30. **local: Full URL for the request**
31. **local: Array to build curl arguments**
32. **else: Add who field to data**
33. **fi: Add URL as final argument**
34. **return: Server error code**
35. **fi: Return successful response**
36. **return: Connection error code**
37. **local: Context key to retrieve**
38. **return: Invalid arguments error**
39. **format_output: Format and display response**
40. **else: Return error code from make_request**
41. **local: Context key to set**
42. **local: Value to assign to key**
43. **return: Invalid arguments error**
44. **fi: Make POST request to set key value**
45. **format_output: Format and display response**
46. **else: Return error code from make_request**
47. **format_output: Use standard formatting**
48. **else: Return error code from make_request**
49. **format_output: Format and display response**
50. **else: Return error code from make_request**
51. **return: Connection error**
52. **local: Track last seen timestamp**
53. **else: Show last 5 or all**
54. **fi: Display new changes**
55. **fi: Update last timestamp**
56. **fi: Poll every 5 seconds**
57. **local: Command to execute**
58. **local: Arguments for the command**
59. **while: -gt 0 ]]; do**
60. **print_help: Show help and exit**
61. **shift: Remaining arguments for command**
62. **exit: Invalid arguments error**
63. **done: Validate command was provided**
64. **exit: Invalid arguments error**
65. **fi: Check dependencies and server connection**
66. **check_dependencies: Skip connection check for help and status commands**
67. **fi: Execute requested command**
68. **exit: Invalid arguments error**

## Functions (15 total)

### `print_help()`

**Type:** shell_function  
**Description:** Shell function: print_help  

### `log()`

**Type:** shell_function  
**Description:** Shell function: log  

### `check_dependencies()`

**Type:** shell_function  
**Description:** Shell function: check_dependencies  

### `validate_server_connection()`

**Type:** shell_function  
**Description:** Shell function: validate_server_connection  

### `parse_json_value()`

**Type:** shell_function  
**Description:** Shell function: parse_json_value  

### `format_output()`

**Type:** shell_function  
**Description:** Shell function: format_output  

### `make_request()`

**Type:** shell_function  
**Description:** Shell function: make_request  

### `cmd_get()`

**Type:** shell_function  
**Description:** Shell function: cmd_get  

### `cmd_set()`

**Type:** shell_function  
**Description:** Shell function: cmd_set  

### `cmd_list()`

**Type:** shell_function  
**Description:** Shell function: cmd_list  

### `cmd_history()`

**Type:** shell_function  
**Description:** Shell function: cmd_history  

### `cmd_status()`

**Type:** shell_function  
**Description:** Shell function: cmd_status  

### `cmd_monitor()`

**Type:** shell_function  
**Description:** Shell function: cmd_monitor  

### `cmd_clear()`

**Type:** shell_function  
**Description:** Shell function: cmd_clear  

### `main()`

**Type:** shell_function  
**Description:** Shell function: main  


## Usage

### Basic Execution
```bash
# Make script executable
chmod +x tools/context.sh

# Execute script
./tools/context.sh
```


## Dependencies

This script requires the following dependencies:

- `pip`


## Entry Points

The following functions serve as entry points:

- `main()` - Main execution function


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
