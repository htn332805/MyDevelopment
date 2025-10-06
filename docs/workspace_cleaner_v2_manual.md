# workspace_cleaner_v2.py - User Manual

## Overview
**File Path:** `tools/workspace_cleaner_v2.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:49:21.382400  
**File Size:** 57,483 bytes  

## Description
Enhanced Workspace Cleaner for Framework0 Production System

This module provides comprehensive workspace cleaning capabilities that integrate
with the consolidated Framework0 architecture. It removes temporary files, manages
build artifacts, and maintains workspace hygiene while preserving important data.

The cleaner is designed to work with the unified Context system, enhanced logging,
and follows strict backward compatibility requirements. It provides both selective
and comprehensive cleaning modes with detailed reporting.

Key Features:
- Safe cleaning with configurable exclusions and preservation rules
- Integration with Context system for state tracking during cleanup
- Comprehensive logging with debug support via environment variables
- Backup creation before destructive operations for rollback capability
- Performance metrics and cleanup analytics for optimization
- Cross-platform compatibility with path handling and permissions
- Extensible plugin architecture for custom cleaning rules
- JSON/YAML configuration system for rule management

Author: Framework0 Team
License: MIT
Version: Production (consolidated architecture)

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: add_cleanup_rule**
4. **Function: add_standard_rules**
5. **Function: save_configuration**
6. **Function: load_configuration**
7. **Function: execute_cleanup**
8. **Function: _create_backup**
9. **Function: _execute_single_rule**
10. **Function: _update_rule_metrics**
11. **Content generation: generate_report**
12. **Function: _add_rule_impl**
13. **Function: _add_standard_impl**
14. **Function: _save_config_impl**
15. **Function: _load_config_impl**
16. **Function: _execute_cleanup_impl**
17. **Class: CleanupRule (0 methods)**
18. **Class: CleanupResult (0 methods)**
19. **Class: WorkspaceCleanerV2 (10 methods)**

## Functions (16 total)

### `main`

**Signature:** `main() -> None`  
**Line:** 1035  
**Description:** Command-line interface for WorkspaceCleanerV2.

Provides comprehensive CLI for workspace cleaning with configuration management.

### `__init__`

**Signature:** `__init__(self, workspace_path: str) -> None`  
**Line:** 178  
**Description:** Initialize enhanced workspace cleaner with comprehensive configuration.

Args:
    workspace_path: Root path of workspace to clean
    context: Optional Context instance for state management
    enable_backups: Whether to create backups before destructive operations
    backup_directory: Custom backup directory (defaults to .cleanup_backups)
    max_backup_age_days: Maximum age of backups before cleanup
    enable_metrics: Whether to collect performance and operation metrics

Raises:
    ValueError: If workspace_path does not exist or is not accessible
    PermissionError: If insufficient permissions for workspace operations

### `add_cleanup_rule`

**Signature:** `add_cleanup_rule(self, rule: CleanupRule) -> None`  
**Line:** 248  
**Description:** Add a custom cleanup rule to the cleaner configuration.

Args:
    rule: CleanupRule instance defining the cleaning behavior

Raises:
    ValueError: If rule name conflicts with existing rule
    TypeError: If rule is not a CleanupRule instance

### `add_standard_rules`

**Signature:** `add_standard_rules(self) -> None`  
**Line:** 299  
**Description:** Add comprehensive standard cleanup rules for Framework0 workspace.

This method configures the most common cleanup rules that are safe
and beneficial for typical Framework0 workspace maintenance.

### `save_configuration`

**Signature:** `save_configuration(self, config_path: Optional[str]) -> None`  
**Line:** 416  
**Description:** Save current cleanup rules and settings to JSON/YAML configuration file.

Args:
    config_path: Optional path for config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    PermissionError: If unable to write to configuration file
    ValueError: If configuration data is invalid

### `load_configuration`

**Signature:** `load_configuration(self, config_path: Optional[str]) -> None`  
**Line:** 492  
**Description:** Load cleanup rules and settings from JSON/YAML configuration file.

Args:
    config_path: Optional path to config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    FileNotFoundError: If configuration file does not exist
    ValueError: If configuration format is invalid or unsupported
    PermissionError: If unable to read configuration file

### `execute_cleanup`

**Signature:** `execute_cleanup(self) -> List[CleanupResult]`  
**Line:** 598  
**Description:** Execute configured cleanup rules with comprehensive safety and monitoring.

Args:
    dry_run: Whether to perform actual cleanup or just simulate
    rules_filter: Optional list of rule names to execute (None = all enabled rules)
    skip_confirmation: Whether to skip user confirmation for destructive operations
    enable_progress: Whether to display progress information during execution

Returns:
    List[CleanupResult]: Detailed results for each executed cleanup rule

Example:
    >>> cleaner = WorkspaceCleanerV2("/path/to/workspace")
    >>> cleaner.add_standard_rules()
    >>> results = cleaner.execute_cleanup(dry_run=False, skip_confirmation=True)

### `_create_backup`

**Signature:** `_create_backup(self) -> Path`  
**Line:** 735  
**Description:** Create backup of workspace before destructive operations.

Returns:
    Path: Path to created backup directory
    
Raises:
    OSError: If backup creation fails

### `_execute_single_rule`

**Signature:** `_execute_single_rule(self, rule: CleanupRule, dry_run: bool, skip_confirmation: bool) -> CleanupResult`  
**Line:** 795  
**Description:** Execute a single cleanup rule with comprehensive error handling and metrics.

Args:
    rule: CleanupRule to execute
    dry_run: Whether to perform actual cleanup or simulation
    skip_confirmation: Whether to skip user confirmation prompts
    
Returns:
    CleanupResult: Detailed results of rule execution

### `_update_rule_metrics`

**Signature:** `_update_rule_metrics(self, rule_name: str, result: CleanupResult, execution_time: float, success: bool) -> None`  
**Line:** 919  
**Description:** Update performance metrics for a specific cleanup rule.

Args:
    rule_name: Name of the rule that was executed
    result: CleanupResult containing execution details
    execution_time: Time taken to execute the rule
    success: Whether the rule executed successfully

### `generate_report`

**Signature:** `generate_report(self, results: List[CleanupResult], output_path: Optional[str]) -> Dict[str, Any]`  
**Line:** 952  
**Description:** Generate comprehensive cleanup report with detailed analysis and metrics.

Args:
    results: List of CleanupResult from cleanup execution
    output_path: Optional path to save report (defaults to workspace/cleanup_report.json)
    
Returns:
    Dict[str, Any]: Comprehensive report data structure

### `_add_rule_impl`

**Signature:** `_add_rule_impl() -> None`  
**Line:** 259  
**Description:** Internal implementation with thread safety and validation.

### `_add_standard_impl`

**Signature:** `_add_standard_impl() -> None`  
**Line:** 306  
**Description:** Internal implementation of standard rule addition.

### `_save_config_impl`

**Signature:** `_save_config_impl() -> None`  
**Line:** 427  
**Description:** Internal implementation of configuration saving.

### `_load_config_impl`

**Signature:** `_load_config_impl() -> None`  
**Line:** 504  
**Description:** Internal implementation of configuration loading.

### `_execute_cleanup_impl`

**Signature:** `_execute_cleanup_impl() -> List[CleanupResult]`  
**Line:** 623  
**Description:** Internal implementation of cleanup execution with comprehensive tracking.


## Classes (3 total)

### `CleanupRule`

**Line:** 106  
**Description:** Structured cleanup rule definition for flexible cleaning configuration.

This class defines individual cleanup rules that specify what to clean,
how to clean it, and what conditions must be met for safe execution.

### `CleanupResult`

**Line:** 127  
**Description:** Comprehensive cleanup operation result with detailed metrics and reporting.

This class captures all aspects of a cleanup operation for analysis,
reporting, and audit trail generation.

### `WorkspaceCleanerV2`

**Line:** 144  
**Description:** Enhanced workspace cleaner with comprehensive Framework0 integration.

This class provides advanced workspace cleaning capabilities that integrate
seamlessly with the consolidated Framework0 architecture. It uses the unified
Context system for state management, enhanced logging for traceability, and
follows strict safety protocols to prevent data loss.

The cleaner operates on a rule-based system that allows fine-grained control
over what gets cleaned, when it gets cleaned, and how the cleaning is performed.
All operations are logged and can be tracked through the Context system.

Key Features:
- Rule-based cleaning with flexible configuration and custom validation
- Context integration for state tracking and distributed coordination
- Comprehensive safety checks with backup creation and rollback capabilities
- Performance monitoring and optimization with detailed analytics
- Cross-platform compatibility with proper path handling and permissions
- Extensible architecture supporting custom cleaning plugins and rules
- Comprehensive error handling with graceful degradation and recovery
- JSON/YAML configuration system for rule persistence and sharing

Thread Safety:
All operations are thread-safe when used with Context thread safety enabled.
The cleaner can be safely used in concurrent environments and distributed systems.

Example Usage:
    >>> cleaner = WorkspaceCleanerV2(workspace_path="/path/to/workspace")
    >>> cleaner.add_standard_rules()
    >>> results = cleaner.execute_cleanup(dry_run=False)
    >>> cleaner.generate_report(results)

**Methods (10 total):**
- `__init__`: Initialize enhanced workspace cleaner with comprehensive configuration.

Args:
    workspace_path: Root path of workspace to clean
    context: Optional Context instance for state management
    enable_backups: Whether to create backups before destructive operations
    backup_directory: Custom backup directory (defaults to .cleanup_backups)
    max_backup_age_days: Maximum age of backups before cleanup
    enable_metrics: Whether to collect performance and operation metrics

Raises:
    ValueError: If workspace_path does not exist or is not accessible
    PermissionError: If insufficient permissions for workspace operations
- `add_cleanup_rule`: Add a custom cleanup rule to the cleaner configuration.

Args:
    rule: CleanupRule instance defining the cleaning behavior

Raises:
    ValueError: If rule name conflicts with existing rule
    TypeError: If rule is not a CleanupRule instance
- `add_standard_rules`: Add comprehensive standard cleanup rules for Framework0 workspace.

This method configures the most common cleanup rules that are safe
and beneficial for typical Framework0 workspace maintenance.
- `save_configuration`: Save current cleanup rules and settings to JSON/YAML configuration file.

Args:
    config_path: Optional path for config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    PermissionError: If unable to write to configuration file
    ValueError: If configuration data is invalid
- `load_configuration`: Load cleanup rules and settings from JSON/YAML configuration file.

Args:
    config_path: Optional path to config file (defaults to workspace/.cleanup_config.json)
    
Raises:
    FileNotFoundError: If configuration file does not exist
    ValueError: If configuration format is invalid or unsupported
    PermissionError: If unable to read configuration file
- `execute_cleanup`: Execute configured cleanup rules with comprehensive safety and monitoring.

Args:
    dry_run: Whether to perform actual cleanup or just simulate
    rules_filter: Optional list of rule names to execute (None = all enabled rules)
    skip_confirmation: Whether to skip user confirmation for destructive operations
    enable_progress: Whether to display progress information during execution

Returns:
    List[CleanupResult]: Detailed results for each executed cleanup rule

Example:
    >>> cleaner = WorkspaceCleanerV2("/path/to/workspace")
    >>> cleaner.add_standard_rules()
    >>> results = cleaner.execute_cleanup(dry_run=False, skip_confirmation=True)
- `_create_backup`: Create backup of workspace before destructive operations.

Returns:
    Path: Path to created backup directory
    
Raises:
    OSError: If backup creation fails
- `_execute_single_rule`: Execute a single cleanup rule with comprehensive error handling and metrics.

Args:
    rule: CleanupRule to execute
    dry_run: Whether to perform actual cleanup or simulation
    skip_confirmation: Whether to skip user confirmation prompts
    
Returns:
    CleanupResult: Detailed results of rule execution
- `_update_rule_metrics`: Update performance metrics for a specific cleanup rule.

Args:
    rule_name: Name of the rule that was executed
    result: CleanupResult containing execution details
    execution_time: Time taken to execute the rule
    success: Whether the rule executed successfully
- `generate_report`: Generate comprehensive cleanup report with detailed analysis and metrics.

Args:
    results: List of CleanupResult from cleanup execution
    output_path: Optional path to save report (defaults to workspace/cleanup_report.json)
    
Returns:
    Dict[str, Any]: Comprehensive report data structure


## Usage Examples

### Example 1
```python
>>> cleaner = WorkspaceCleanerV2("/path/to/workspace")
            >>> cleaner.add_standard_rules()
            >>> results = cleaner.execute_cleanup(dry_run=False, skip_confirmation=True)
        """
```

### Example 2
```python
%(prog)s --dry-run                          # Preview what would be cleaned
  %(prog)s --execute --skip-confirmation      # Execute all rules without prompts
  %(prog)s --save-config my_rules.json       # Save current rules to config
  %(prog)s --load-config my_rules.json       # Load rules from config
  %(prog)s --add-standard --execute          # Add standard rules and execute
        """
    )
    
    # Basic operation arguments
```

### Example 3
```python
>>> cleaner = WorkspaceCleanerV2(workspace_path="/path/to/workspace")
        >>> cleaner.add_standard_rules()
        >>> results = cleaner.execute_cleanup(dry_run=False)
        >>> cleaner.generate_report(results)
    """
```

### Example 4
```python
cleaner = WorkspaceCleanerV2(workspace_path="/path/to/workspace")
        >>> cleaner.add_standard_rules()
        >>> results = cleaner.execute_cleanup(dry_run=False)
        >>> cleaner.generate_report(results)
    """

    def __init__(
        self,
        workspace_path: str,
        *,
        context: Optional[Context] = None,
        enable_backups: bool = True,
        backup_directory: Optional[str] = None,
        max_backup_age_days: int = 7,
        enable_metrics: bool = True
    ) -> None:
        """
        Initialize enhanced workspace cleaner with comprehensive configuration.

        Args:
            workspace_path: Root path of workspace to clean
            context: Optional Context instance for state management
            enable_backups: Whether to create backups before destructive operations
            backup_directory: Custom backup directory (defaults to .cleanup_backups)
            max_backup_age_days: Maximum age of backups before cleanup
            enable_metrics: Whether to collect performance and operation metrics

        Raises:
            ValueError: If workspace_path does not exist or is not accessible
            PermissionError: If insufficient permissions for workspace operations
        """
        # Validate and normalize workspace path
        self.workspace_path = Path(workspace_path).resolve()  # Convert to absolute path
        if not self.workspace_path.exists():
            raise ValueError(f"Workspace path does not exist: {workspace_path}")
        if not os.access(self.workspace_path, os.R_OK | os.W_OK):
            raise PermissionError(f"Insufficient permissions for workspace: {workspace_path}")

        # Initialize Context system for state management and coordination
        self.context = context or Context(  # Use provided context or create new one
            enable_history=True,            # Enable history for cleanup audit trail
            enable_metrics=True             # Enable metrics for performance monitoring
        )
        
        # Configure backup system for data protection
        self.enable_backups = enable_backups          # Whether backups are enabled
        self.backup_directory = Path(               # Backup directory configuration
            backup_directory or self.workspace_path / ".cleanup_backups"
        )
        self.max_backup_age_days = max_backup_age_days  # Backup retention policy
        
        # Initialize cleanup rule management system
        self.cleanup_rules: List[CleanupRule] = []    # List of configured cleanup rules
        self.rule_metrics: Dict[str, Dict[str, Any]] = defaultdict(dict)  # Rule performance metrics
        
        # Performance and monitoring configuration
        self.enable_metrics = enable_metrics          # Whether to collect detailed metrics
        self.execution_stats = {                     # Execution statistics tracking
            "total_operations": 0,                   # Total operations performed
            "total_bytes_freed": 0,                  # Total storage freed
            "total_files_processed": 0,              # Total files processed
            "total_execution_time": 0.0,             # Total execution time
            "error_count": 0,                        # Number of errors encountered
            "warning_count": 0                       # Number of warnings generated
        }
        
        # Thread safety and concurrency management
        self._lock = threading.RLock()               # Reentrant lock for thread safety
        
        # Initialize Context state with cleaner information
        self.context.set("cleaner.workspace_path", str(self.workspace_path), who="workspace_cleaner_init")
        self.context.set("cleaner.enable_backups", self.enable_backups, who="workspace_cleaner_init")
        self.context.set("cleaner.initialization_time", time.time(), who="workspace_cleaner_init")
        
        logger.info(f"WorkspaceCleanerV2 initialized for workspace: {self.workspace_path}")

    def add_cleanup_rule(self, rule: CleanupRule) -> None:
        """
        Add a custom cleanup rule to the cleaner configuration.

        Args:
            rule: CleanupRule instance defining the cleaning behavior

        Raises:
            ValueError: If rule name conflicts with existing rule
            TypeError: If rule is not a CleanupRule instance
        """
        def _add_rule_impl() -> None:
            """Internal implementation with thread safety and validation."""
            # Validate rule type and configuration
            if not isinstance(rule, CleanupRule):
                raise TypeError(f"Expected CleanupRule, got {type(rule).__name__}")
            
            # Check for name conflicts with existing rules
            existing_names = [r.name for r in self.cleanup_rules]
            if rule.name in existing_names:
                raise ValueError(f"Rule name '{rule.name}' already exists")
            
            # Add rule to configuration
            self.cleanup_rules.append(rule)
            
            # Initialize rule metrics tracking
            self.rule_metrics[rule.name] = {
                "added_time": time.time(),           # When rule was added
                "execution_count": 0,               # Number of times executed
                "total_files_processed": 0,         # Total files processed by this rule
                "total_bytes_freed": 0,             # Total bytes freed by this rule
                "average_execution_time": 0.0,      # Average execution time
                "last_execution_time": None,        # Last execution timestamp
                "error_count": 0,                   # Number of errors for this rule
                "success_rate": 1.0                 # Success rate percentage
            }
            
            # Update Context state with new rule information
            self.context.set(f"cleaner.rules.{rule.name}.enabled", rule.enabled, who="add_cleanup_rule")
            self.context.set(f"cleaner.rules.{rule.name}.pattern", rule.pattern, who="add_cleanup_rule")
            self.context.set(f"cleaner.rules.{rule.name}.description", rule.description, who="add_cleanup_rule")
            
            logger.info(f"Added cleanup rule: {rule.name} (pattern: {rule.pattern})")

        # Execute with thread safety protection
        if self._lock:
            with self._lock:
                _add_rule_impl()
        else:
            _add_rule_impl()

    def add_standard_rules(self) -> None:
        """
        Add comprehensive standard cleanup rules for Framework0 workspace.

        This method configures the most common cleanup rules that are safe
        and beneficial for typical Framework0 workspace maintenance.
        """
        def _add_standard_impl() -> None:
            """Internal implementation of standard rule addition."""
            # Python bytecode and cache cleanup
            self.add_cleanup_rule(CleanupRule(
                name="python_bytecode",                # Rule identifier
                pattern="**/__pycache__",              # Pattern for Python cache directories
                description="Remove Python bytecode cache directories",  # Human-readable description
                recursive=True,                        # Apply recursively to all subdirectories
                dry_run_safe=True,                     # Safe for dry-run operations
                requires_confirmation=False            # No confirmation needed for cache cleanup
            ))
            
            self.add_cleanup_rule(CleanupRule(
                name="python_compiled",                # Rule identifier
                pattern="**/*.pyc",                    # Pattern for compiled Python files
                description="Remove Python compiled files (.pyc)",  # Description
                recursive=True,                        # Recursive application
                dry_run_safe=True,                     # Safe for dry-run
                exclude_patterns=["venv/**", "pyvenv/**"]  # Exclude virtual environments
            ))
            
            # Temporary and build artifact cleanup
            self.add_cleanup_rule(CleanupRule(
                name="temp_files",                     # Rule identifier
                pattern="**/tmp_*",                    # Pattern for temporary files
                description="Remove temporary files and directories",  # Description
                recursive=True,                        # Recursive application
                minimum_age_hours=1.0,                 # Only remove files older than 1 hour
                exclude_patterns=["**/logs/**"]       # Preserve log files
            ))
            
            self.add_cleanup_rule(CleanupRule(
                name="build_artifacts",                # Rule identifier  
                pattern="**/build/**",                 # Pattern for build directories
                description="Remove build artifacts and directories",  # Description
                recursive=True,                        # Recursive application
                requires_confirmation=True,            # Require confirmation for safety
                exclude_patterns=["**/node_modules/**"]  # Exclude package managers
            ))
            
            # Log file management with size and age limits
            self.add_cleanup_rule(CleanupRule(
                name="old_log_files",                  # Rule identifier
                pattern="**/*.log",                    # Pattern for log files
                description="Remove old log files larger than 10MB or older than 7 days",  # Description
                recursive=True,                        # Recursive application
                minimum_age_hours=168.0,               # 7 days in hours
                maximum_size_mb=10.0,                  # Maximum size in megabytes
                exclude_patterns=["**/debug.log", "**/error.log"]  # Preserve important logs
            ))
            
            # Test and coverage artifact cleanup
            self.add_cleanup_rule(CleanupRule(
                name="test_artifacts",                 # Rule identifier
                pattern="**/.pytest_cache/**",        # Pattern for pytest cache
                description="Remove pytest cache and test artifacts",  # Description
                recursive=True,                        # Recursive application
                dry_run_safe=True                      # Safe for dry-run operations
            ))
            
            self.add_cleanup_rule(CleanupRule(
                name="coverage_files",                 # Rule identifier
                pattern="**/.coverage*",               # Pattern for coverage files
                description="Remove code coverage report files",  # Description
                recursive=True,                        # Recursive application
                minimum_age_hours=24.0,                # Only remove files older than 1 day
                exclude_patterns=["**/reports/**"]    # Preserve coverage reports
            ))
            
            # IDE and editor temporary files
            self.add_cleanup_rule(CleanupRule(
                name="editor_backups",                 # Rule identifier
                pattern="**/*~",                       # Pattern for editor backup files
                description="Remove editor backup files and temporary saves",  # Description
                recursive=True,                        # Recursive application
                dry_run_safe=True,                     # Safe for dry-run operations
                minimum_age_hours=0.5                  # Remove files older than 30 minutes
            ))
            
            # OS-specific temporary files and system artifacts
            if os.name == 'nt':  # Windows-specific rules
                self.add_cleanup_rule(CleanupRule(
                    name="windows_thumbs",             # Rule identifier
                    pattern="**/Thumbs.db",            # Pattern for Windows thumbnail cache
                    description="Remove Windows thumbnail cache files",  # Description
                    recursive=True,                    # Recursive application
                    dry_run_safe=True                  # Safe for dry-run operations
                ))
            else:  # Unix-like systems (Linux, macOS)
                self.add_cleanup_rule(CleanupRule(
                    name="macos_ds_store",             # Rule identifier
                    pattern="**/.DS_Store",            # Pattern for macOS metadata files
                    description="Remove macOS .DS_Store metadata files",  # Description
                    recursive=True,                    # Recursive application
                    dry_run_safe=True                  # Safe for dry-run operations
                ))

            # Update Context with standard rules configuration
            self.context.set("cleaner.standard_rules_added", True, who="add_standard_rules")
            self.context.set("cleaner.total_rules_count", len(self.cleanup_rules), who="add_standard_rules")
            
            logger.info(f"Added {len(self.cleanup_rules)} standard cleanup rules")

        # Execute with thread safety protection
        if self._lock:
            with self._lock:
                _add_standard_impl()
        else:
            _add_standard_impl()

    def save_configuration(self, config_path: Optional[str] = None) -> None:
        """
        Save current cleanup rules and settings to JSON/YAML configuration file.
        
        Args:
            config_path: Optional path for config file (defaults to workspace/.cleanup_config.json)
            
        Raises:
            PermissionError: If unable to write to configuration file
            ValueError: If configuration data is invalid
        """
        def _save_config_impl() -> None:
            """Internal implementation of configuration saving."""
            # Determine configuration file path
            if config_path is None:
                config_file = self.workspace_path / ".cleanup_config.json"
            else:
                config_file = Path(config_path)
                
            # Prepare configuration data structure
            config_data = {
                "workspace_cleaner_config": {
                    "version": "2.0",  # Configuration format version
                    "created_time": time.time(),  # When config was created
                    "workspace_path": str(self.workspace_path),  # Workspace path
                    "settings": {
                        "enable_backups": self.enable_backups,  # Backup configuration
                        "backup_directory": str(self.backup_directory),  # Backup location
                        "max_backup_age_days": self.max_backup_age_days,  # Backup retention
                        "enable_metrics": self.enable_metrics  # Metrics configuration
                    },
                    "cleanup_rules": []
                }
            }
            
            # Serialize cleanup rules to configuration format
            for rule in self.cleanup_rules:
                rule_data = {
                    "name": rule.name,  # Rule identifier
                    "pattern": rule.pattern,  # File pattern to match
                    "description": rule.description,  # Human-readable description
                    "enabled": rule.enabled,  # Whether rule is active
                    "recursive": rule.recursive,  # Recursive directory traversal
                    "dry_run_safe": rule.dry_run_safe,  # Safe for dry-run operations
                    "requires_confirmation": rule.requires_confirmation,  # Needs user confirmation
                    "exclude_patterns": rule.exclude_patterns,  # Exclusion patterns
                    "minimum_age_hours": rule.minimum_age_hours,  # Minimum file age
                    "maximum_size_mb": rule.maximum_size_mb  # Maximum file size limit
                    # Note: custom_validator functions cannot be serialized
                }
                config_data["workspace_cleaner_config"]["cleanup_rules"].append(rule_data)
            
            # Write configuration to file with proper error handling
            try:
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
                    
                # Update Context with configuration save information
                self.context.set("cleaner.config.last_save_time", time.time(), who="save_configuration")
                self.context.set("cleaner.config.last_save_path", str(config_file), who="save_configuration")
                self.context.set("cleaner.config.rules_saved", len(self.cleanup_rules), who="save_configuration")
                
                logger.info(f"Saved cleanup configuration to: {config_file} ({len(self.cleanup_rules)} rules)")
                
            except (OSError, PermissionError) as e:
                raise PermissionError(f"Unable to save configuration to {config_file}: {e}")
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid configuration data: {e}")
                
        # Execute with thread safety protection
        if self._lock:
            with self._lock:
                _save_config_impl()
        else:
            _save_config_impl()

    def load_configuration(self, config_path: Optional[str] = None) -> None:
        """
        Load cleanup rules and settings from JSON/YAML configuration file.
        
        Args:
            config_path: Optional path to config file (defaults to workspace/.cleanup_config.json)
            
        Raises:
            FileNotFoundError: If configuration file does not exist
            ValueError: If configuration format is invalid or unsupported
            PermissionError: If unable to read configuration file
        """
        def _load_config_impl() -> None:
            """Internal implementation of configuration loading."""
            # Determine configuration file path
            if config_path is None:
                config_file = self.workspace_path / ".cleanup_config.json"
            else:
                config_file = Path(config_path)
                
            # Validate configuration file exists and is readable
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_file}")
            if not os.access(config_file, os.R_OK):
                raise PermissionError(f"Unable to read configuration file: {config_file}")
                
            # Load and parse configuration file
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    if config_file.suffix.lower() == '.yaml' or config_file.suffix.lower() == '.yml':
                        import yaml  # Import YAML support if needed
                        config_data = yaml.safe_load(f)
                    else:
                        config_data = json.load(f)  # Default to JSON parsing
                        
            except (OSError, PermissionError) as e:
                raise PermissionError(f"Unable to read configuration file {config_file}: {e}")
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Invalid configuration file format: {e}")
                
            # Validate configuration structure and version
            if "workspace_cleaner_config" not in config_data:
                raise ValueError("Invalid configuration: missing 'workspace_cleaner_config' section")
                
            config = config_data["workspace_cleaner_config"]
            
            # Check configuration version compatibility
            config_version = config.get("version", "1.0")
            if not config_version.startswith("2."):
                logger.warning(f"Loading older configuration version {config_version}, may have compatibility issues")
                
            # Load settings if present
            if "settings" in config:
                settings = config["settings"]
                self.enable_backups = settings.get("enable_backups", self.enable_backups)
                self.max_backup_age_days = settings.get("max_backup_age_days", self.max_backup_age_days)
                self.enable_metrics = settings.get("enable_metrics", self.enable_metrics)
                
                # Update backup directory if specified
                if "backup_directory" in settings:
                    self.backup_directory = Path(settings["backup_directory"])
                    
            # Clear existing rules and load from configuration
            self.cleanup_rules.clear()
            self.rule_metrics.clear()
            
            # Load cleanup rules from configuration
            if "cleanup_rules" in config:
                for rule_data in config["cleanup_rules"]:
                    try:
                        # Create CleanupRule from configuration data
                        rule = CleanupRule(
                            name=rule_data["name"],
                            pattern=rule_data["pattern"],
                            description=rule_data["description"],
                            enabled=rule_data.get("enabled", True),
                            recursive=rule_data.get("recursive", False),
                            dry_run_safe=rule_data.get("dry_run_safe", True),
                            requires_confirmation=rule_data.get("requires_confirmation", False),
                            exclude_patterns=rule_data.get("exclude_patterns", []),
                            minimum_age_hours=rule_data.get("minimum_age_hours", 0.0),
                            maximum_size_mb=rule_data.get("maximum_size_mb", None)
                            # Note: custom_validator cannot be loaded from config
                        )
                        
                        # Add rule using existing method for proper initialization
                        self.add_cleanup_rule(rule)
                        
                    except (KeyError, TypeError, ValueError) as e:
                        logger.error(f"Skipping invalid rule configuration: {e}")
                        continue  # Skip invalid rules but continue loading others
                        
            # Update Context with configuration load information
            self.context.set("cleaner.config.last_load_time", time.time(), who="load_configuration")
            self.context.set("cleaner.config.last_load_path", str(config_file), who="load_configuration")
            self.context.set("cleaner.config.rules_loaded", len(self.cleanup_rules), who="load_configuration")
            
            logger.info(f"Loaded cleanup configuration from: {config_file} ({len(self.cleanup_rules)} rules)")
            
        # Execute with thread safety protection
        if self._lock:
            with self._lock:
                _load_config_impl()
        else:
            _load_config_impl()

    def execute_cleanup(
        self,
        *,
        dry_run: bool = True,
        rules_filter: Optional[List[str]] = None,
        skip_confirmation: bool = False,
        enable_progress: bool = True
    ) -> List[CleanupResult]:
        """
        Execute configured cleanup rules with comprehensive safety and monitoring.

        Args:
            dry_run: Whether to perform actual cleanup or just simulate
            rules_filter: Optional list of rule names to execute (None = all enabled rules)
            skip_confirmation: Whether to skip user confirmation for destructive operations
            enable_progress: Whether to display progress information during execution

        Returns:
            List[CleanupResult]: Detailed results for each executed cleanup rule

        Example:
            >>> cleaner = WorkspaceCleanerV2("/path/to/workspace")
            >>> cleaner.add_standard_rules()
            >>> results = cleaner.execute_cleanup(dry_run=False, skip_confirmation=True)
        """
        def _execute_cleanup_impl() -> List[CleanupResult]:
            """Internal implementation of cleanup execution with comprehensive tracking."""
            start_time = time.time()  # Record operation start time for metrics
            results: List[CleanupResult] = []  # Initialize results collection
            
            # Filter rules based on criteria
            rules_to_execute = [
                rule for rule in self.cleanup_rules
                if rule.enabled and (rules_filter is None or rule.name in rules_filter)
            ]
            
            if not rules_to_execute:
                logger.warning("No cleanup rules to execute based on current criteria")
                return results
            
            # Update Context with execution information
            self.context.set("cleaner.execution.start_time", start_time, who="execute_cleanup")
            self.context.set("cleaner.execution.dry_run", dry_run, who="execute_cleanup")
            self.context.set("cleaner.execution.rules_count", len(rules_to_execute), who="execute_cleanup")
            
            logger.info(f"Starting cleanup execution: {len(rules_to_execute)} rules, dry_run={dry_run}")
            
            # Create backup if enabled and not in dry-run mode
            backup_path = None
            if self.enable_backups and not dry_run:
                backup_path = self._create_backup()
                self.context.set("cleaner.execution.backup_path", str(backup_path), who="execute_cleanup")
            
            # Execute each cleanup rule with comprehensive error handling
            for i, rule in enumerate(rules_to_execute, 1):
                if enable_progress:
                    logger.info(f"Executing rule {i}/{len(rules_to_execute)}: {rule.name}")
                
                try:
                    # Execute individual rule with timing and metrics
                    rule_start_time = time.time()
                    rule_result = self._execute_single_rule(rule, dry_run, skip_confirmation)
                    rule_execution_time = time.time() - rule_start_time
                    
                    # Update rule-specific metrics
                    rule_result.execution_time_seconds = rule_execution_time
                    self._update_rule_metrics(rule.name, rule_result, rule_execution_time)
                    
                    # Add to results collection
                    results.append(rule_result)
                    
                    # Update Context with rule execution results
                    self.context.set(
                        f"cleaner.execution.rules.{rule.name}.files_removed", 
                        len(rule_result.files_removed), 
                        who="execute_cleanup"
                    )
                    self.context.set(
                        f"cleaner.execution.rules.{rule.name}.bytes_freed", 
                        rule_result.bytes_freed, 
                        who="execute_cleanup"
                    )
                    
                    logger.debug(f"Rule '{rule.name}' completed: {len(rule_result.files_removed)} files, "
                                f"{rule_result.bytes_freed} bytes, {rule_execution_time:.3f}s")
                
                except Exception as e:
                    # Handle rule execution errors gracefully
                    error_message = f"Error executing rule '{rule.name}': {str(e)}"
                    logger.error(error_message)
                    
                    # Create error result for failed rule
                    error_result = CleanupResult(
                        rule_name=rule.name,
                        execution_time_seconds=time.time() - rule_start_time if 'rule_start_time' in locals() else 0.0,
                        errors=[error_message]
                    )
                    results.append(error_result)
                    
                    # Update error metrics
                    self.execution_stats["error_count"] += 1
                    self._update_rule_metrics(rule.name, error_result, 0.0, success=False)
            
            # Calculate and record total execution metrics
            total_execution_time = time.time() - start_time
            total_files_removed = sum(len(r.files_removed) for r in results)
            total_bytes_freed = sum(r.bytes_freed for r in results)
            total_errors = sum(len(r.errors) for r in results)
            
            # Update global execution statistics
            self.execution_stats["total_operations"] += len(results)
            self.execution_stats["total_bytes_freed"] += total_bytes_freed
            self.execution_stats["total_files_processed"] += total_files_removed
            self.execution_stats["total_execution_time"] += total_execution_time
            self.execution_stats["error_count"] += total_errors
            
            # Update Context with final execution results
            self.context.set("cleaner.execution.end_time", time.time(), who="execute_cleanup")
            self.context.set("cleaner.execution.total_execution_time", total_execution_time, who="execute_cleanup")
            self.context.set("cleaner.execution.total_files_removed", total_files_removed, who="execute_cleanup")
            self.context.set("cleaner.execution.total_bytes_freed", total_bytes_freed, who="execute_cleanup")
            self.context.set("cleaner.execution.total_errors", total_errors, who="execute_cleanup")
            
            # Log execution summary
            logger.info(f"Cleanup execution completed: {total_files_removed} files removed, "
                       f"{total_bytes_freed:,} bytes freed, {total_execution_time:.3f}s total, "
                       f"{total_errors} errors")
            
            return results

        # Execute with thread safety protection
        if self._lock:
            with self._lock:
                return _execute_cleanup_impl()
        else:
            return _execute_cleanup_impl()

    def _create_backup(self) -> Path:
        """
        Create backup of workspace before destructive operations.
        
        Returns:
            Path: Path to created backup directory
            
        Raises:
            OSError: If backup creation fails
        """
        # Create backup directory if it doesn't exist
        self.backup_directory.mkdir(parents=True, exist_ok=True)
        
        # Generate unique backup name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}_{os.getpid()}"
        backup_path = self.backup_directory / backup_name
        
        try:
            # Create selective backup of important files only (not full workspace copy)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Backup configuration files and important data
            important_patterns = [
                "*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.cfg",
                "requirements*.txt", "setup.py", "pyproject.toml",
                "*.md", "*.rst", "*.txt", "LICENSE*", "CHANGELOG*"
            ]
            
            backed_up_files = 0
            for pattern in important_patterns:
                for file_path in self.workspace_path.glob(pattern):
                    if file_path.is_file():
                        # Create backup copy of important file
                        backup_file_path = backup_path / file_path.name
                        shutil.copy2(file_path, backup_file_path)
                        backed_up_files += 1
                        
            # Create backup manifest with file list and metadata
            manifest = {
                "backup_created": time.time(),
                "workspace_path": str(self.workspace_path),
                "backed_up_files": backed_up_files,
                "backup_type": "selective",
                "cleaner_version": "2.0"
            }
            
            manifest_path = backup_path / "backup_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
                
            logger.info(f"Created backup: {backup_path} ({backed_up_files} files)")
            return backup_path
            
        except (OSError, shutil.Error) as e:
            # Clean up partial backup on failure
            if backup_path.exists():
                shutil.rmtree(backup_path, ignore_errors=True)
            raise OSError(f"Backup creation failed: {e}")

    def _execute_single_rule(self, rule: CleanupRule, dry_run: bool, skip_confirmation: bool) -> CleanupResult:
        """
        Execute a single cleanup rule with comprehensive error handling and metrics.
        
        Args:
            rule: CleanupRule to execute
            dry_run: Whether to perform actual cleanup or simulation
            skip_confirmation: Whether to skip user confirmation prompts
            
        Returns:
            CleanupResult: Detailed results of rule execution
        """
        result = CleanupResult(rule_name=rule.name)  # Initialize result tracking
        
        try:
            # Find matching files using rule pattern
            if rule.recursive:
                matching_files = list(self.workspace_path.rglob(rule.pattern))
            else:
                matching_files = list(self.workspace_path.glob(rule.pattern))
                
            # Apply exclusion patterns to filter out protected files
            filtered_files = []
            for file_path in matching_files:
                should_exclude = False
                for exclude_pattern in rule.exclude_patterns:
                    if file_path.match(exclude_pattern):
                        should_exclude = True
                        result.skipped_files.append(str(file_path))
                        break
                        
                if not should_exclude:
                    filtered_files.append(file_path)
                    
            # Apply age and size filters
            eligible_files = []
            current_time = time.time()
            
            for file_path in filtered_files:
                try:
                    # Check if path exists and get stats
                    if not file_path.exists():
                        continue
                        
                    stat_info = file_path.stat()
                    
                    # Apply minimum age filter
                    if rule.minimum_age_hours > 0:
                        file_age_hours = (current_time - stat_info.st_mtime) / 3600
                        if file_age_hours < rule.minimum_age_hours:
                            result.skipped_files.append(f"{file_path} (too new: {file_age_hours:.1f}h)")
                            continue
                            
                    # Apply maximum size filter
                    if rule.maximum_size_mb is not None:
                        file_size_mb = stat_info.st_size / (1024 * 1024)
                        if file_size_mb > rule.maximum_size_mb:
                            result.skipped_files.append(f"{file_path} (too large: {file_size_mb:.1f}MB)")
                            continue
                            
                    # Apply custom validator if present
                    if rule.custom_validator and not rule.custom_validator(file_path):
                        result.skipped_files.append(f"{file_path} (failed custom validation)")
                        continue
                        
                    eligible_files.append(file_path)
                    
                except (OSError, PermissionError) as e:
                    result.warnings.append(f"Cannot access {file_path}: {e}")
                    continue
                    
            # Request confirmation if required and not skipped
            if rule.requires_confirmation and not skip_confirmation and not dry_run:
                if eligible_files:
                    print(f"\nRule '{rule.name}' will remove {len(eligible_files)} files:")
                    for file_path in eligible_files[:10]:  # Show first 10 files
                        print(f"  - {file_path}")
                    if len(eligible_files) > 10:
                        print(f"  ... and {len(eligible_files) - 10} more files")
                        
                    response = input("Proceed with deletion? [y/N]: ").strip().lower()
                    if response not in ['y', 'yes']:
                        result.skipped_files.extend([str(f) for f in eligible_files])
                        logger.info(f"Rule '{rule.name}' cancelled by user")
                        return result
                        
            # Process eligible files for cleanup
            for file_path in eligible_files:
                try:
                    # Calculate file size before removal
                    if file_path.exists():
                        file_size = file_path.stat().st_size if file_path.is_file() else 0
                        
                        if dry_run:
                            # Dry run: just log what would be removed
                            if file_path.is_file():
                                result.files_removed.append(str(file_path))
                            else:
                                result.directories_removed.append(str(file_path))
                            result.bytes_freed += file_size
                            
                        else:
                            # Actual removal
                            if file_path.is_file():
                                file_path.unlink()  # Remove file
                                result.files_removed.append(str(file_path))
                            elif file_path.is_dir():
                                shutil.rmtree(file_path)  # Remove directory
                                result.directories_removed.append(str(file_path))
                                
                            result.bytes_freed += file_size
                            
                except (OSError, PermissionError) as e:
                    error_msg = f"Cannot remove {file_path}: {e}"
                    result.errors.append(error_msg)
                    logger.error(error_msg)
                    
        except Exception as e:
            error_msg = f"Rule execution failed: {e}"
            result.errors.append(error_msg)
            logger.error(error_msg)
            
        return result

    def _update_rule_metrics(self, rule_name: str, result: CleanupResult, execution_time: float, success: bool = True) -> None:
        """
        Update performance metrics for a specific cleanup rule.
        
        Args:
            rule_name: Name of the rule that was executed
            result: CleanupResult containing execution details
            execution_time: Time taken to execute the rule
            success: Whether the rule executed successfully
        """
        if not self.enable_metrics:
            return
            
        metrics = self.rule_metrics[rule_name]
        
        # Update execution statistics
        metrics["execution_count"] += 1
        metrics["total_files_processed"] += len(result.files_removed) + len(result.directories_removed)
        metrics["total_bytes_freed"] += result.bytes_freed
        metrics["last_execution_time"] = time.time()
        
        # Calculate average execution time
        total_time = metrics.get("total_execution_time", 0.0) + execution_time
        metrics["total_execution_time"] = total_time
        metrics["average_execution_time"] = total_time / metrics["execution_count"]
        
        # Update error tracking
        if not success or result.errors:
            metrics["error_count"] += 1
            
        # Calculate success rate
        metrics["success_rate"] = 1.0 - (metrics["error_count"] / metrics["execution_count"])

    def generate_report(self, results: List[CleanupResult], output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive cleanup report with detailed analysis and metrics.
        
        Args:
            results: List of CleanupResult from cleanup execution
            output_path: Optional path to save report (defaults to workspace/cleanup_report.json)
            
        Returns:
            Dict[str, Any]: Comprehensive report data structure
        """
        # Calculate summary statistics
        total_files_removed = sum(len(r.files_removed) for r in results)
        total_directories_removed = sum(len(r.directories_removed) for r in results)
        total_bytes_freed = sum(r.bytes_freed for r in results)
        total_errors = sum(len(r.errors) for r in results)
        total_warnings = sum(len(r.warnings) for r in results)
        total_execution_time = sum(r.execution_time_seconds for r in results)
        
        # Create comprehensive report structure
        report = {
            "cleanup_report": {
                "generated_time": time.time(),
                "generator": "WorkspaceCleanerV2",
                "workspace_path": str(self.workspace_path),
                "context_id": self.context.context_id,
                "summary": {
                    "total_rules_executed": len(results),
                    "total_files_removed": total_files_removed,
                    "total_directories_removed": total_directories_removed,
                    "total_items_removed": total_files_removed + total_directories_removed,
                    "total_bytes_freed": total_bytes_freed,
                    "total_mb_freed": round(total_bytes_freed / (1024 * 1024), 2),
                    "total_execution_time_seconds": round(total_execution_time, 3),
                    "total_errors": total_errors,
                    "total_warnings": total_warnings,
                    "success_rate": round((len(results) - sum(1 for r in results if r.errors)) / len(results) * 100, 2) if results else 100
                },
                "rule_results": [],
                "performance_metrics": self.execution_stats.copy() if self.enable_metrics else None,
                "rule_metrics": dict(self.rule_metrics) if self.enable_metrics else None
            }
        }
        
        # Add detailed results for each rule
        for result in results:
            rule_report = {
                "rule_name": result.rule_name,
                "files_removed": result.files_removed,
                "directories_removed": result.directories_removed,
                "bytes_freed": result.bytes_freed,
                "mb_freed": round(result.bytes_freed / (1024 * 1024), 2),
                "execution_time_seconds": round(result.execution_time_seconds, 3),
                "errors": result.errors,
                "warnings": result.warnings,
                "skipped_files": result.skipped_files,
                "success": len(result.errors) == 0
            }
            report["cleanup_report"]["rule_results"].append(rule_report)
            
        # Save report to file if path specified
        if output_path is None:
            output_path = self.workspace_path / "cleanup_report.json"
        else:
            output_path = Path(output_path)
            
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
            # Update Context with report information
            self.context.set("cleaner.report.last_generated", time.time(), who="generate_report")
            self.context.set("cleaner.report.path", str(output_path), who="generate_report")
            self.context.set("cleaner.report.summary", report["cleanup_report"]["summary"], who="generate_report")
            
            logger.info(f"Generated cleanup report: {output_path}")
            
        except (OSError, PermissionError) as e:
            logger.error(f"Could not save report to {output_path}: {e}")
            
        return report


def main() -> None:
    """
    Command-line interface for WorkspaceCleanerV2.
    
    Provides comprehensive CLI for workspace cleaning with configuration management.
    """
    parser = argparse.ArgumentParser(
        description="Enhanced Workspace Cleaner for Framework0 Production System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --dry-run                          # Preview what would be cleaned
  %(prog)s --execute --skip-confirmation      # Execute all rules without prompts
  %(prog)s --save-config my_rules.json       # Save current rules to config
  %(prog)s --load-config my_rules.json       # Load rules from config
  %(prog)s --add-standard --execute          # Add standard rules and execute
        """
    )
    
    # Basic operation arguments
    parser.add_argument(
        "--workspace", "-w",
        default=".",
        help="Workspace path to clean (default: current directory)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview cleanup without making changes"
    )
    
    parser.add_argument(
        "--execute",
        action="store_true", 
        help="Execute cleanup operations"
    )
    
    parser.add_argument(
        "--skip-confirmation",
        action="store_true",
        help="Skip confirmation prompts for destructive operations"
    )
    
    # Configuration management arguments
    parser.add_argument(
        "--save-config",
        metavar="FILE",
        help="Save current configuration to file"
    )
    
    parser.add_argument(
        "--load-config", 
        metavar="FILE",
        help="Load configuration from file"
    )
    
    parser.add_argument(
        "--add-standard",
        action="store_true",
        help="Add standard cleanup rules"
    )
    
    # Rule filtering arguments
    parser.add_argument(
        "--rules",
        nargs="+",
        help="Specific rule names to execute"
    )
    
    # Output and reporting arguments
    parser.add_argument(
        "--report",
        metavar="FILE", 
        help="Generate detailed report to file"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Disable backup creation"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Set debug environment if requested
    if args.debug:
        os.environ["DEBUG"] = "1"
    
    try:
        # Initialize cleaner
        logger.info("=== Enhanced Workspace Cleaner V2 ===")
        cleaner = WorkspaceCleanerV2(
            workspace_path=args.workspace,
            enable_backups=not args.no_backup
        )
        
        # Load configuration if specified
        if args.load_config:
            logger.info(f"Loading configuration from: {args.load_config}")
            cleaner.load_configuration(args.load_config)
        
        # Add standard rules if requested
        if args.add_standard:
            logger.info("Adding standard cleanup rules")
            cleaner.add_standard_rules()
        
        # Save configuration if specified
        if args.save_config:
            logger.info(f"Saving configuration to: {args.save_config}")
            cleaner.save_configuration(args.save_config)
        
        # Execute cleanup if requested
        if args.execute or args.dry_run:
            logger.info(f"{'Previewing' if args.dry_run else 'Executing'} cleanup operations")
            
            results = cleaner.execute_cleanup(
                dry_run=args.dry_run,
                rules_filter=args.rules,
                skip_confirmation=args.skip_confirmation or args.dry_run
            )
            
            # Generate report
            if args.report:
                cleaner.generate_report(results, args.report)
            else:
                # Print summary to console
                total_files = sum(len(r.files_removed) for r in results)
                total_bytes = sum(r.bytes_freed for r in results)
                total_errors = sum(len(r.errors) for r in results)
                
                print(f"\nCleanup Summary:")
                print(f"  Rules executed: {len(results)}")
                print(f"  Files processed: {total_files}")
                print(f"  Storage freed: {total_bytes:,} bytes ({total_bytes/(1024*1024):.1f} MB)")
                print(f"  Errors: {total_errors}")
                
                if args.dry_run:
                    print("\n⚠️  This was a dry run - no files were actually removed")
                else:
                    print("\n✅ Cleanup completed successfully")
        
        elif not args.save_config and not args.load_config:
            parser.print_help()
            
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```


## Dependencies

This module requires the following dependencies:

- `argparse`
- `collections`
- `dataclasses`
- `datetime`
- `glob`
- `json`
- `orchestrator.context.context`
- `os`
- `pathlib`
- `shutil`
- `src.core.logger`
- `subprocess`
- `sys`
- `threading`
- `time`
- `typing`
- `yaml`


## Entry Points

The following functions can be used as entry points:

- `main()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
