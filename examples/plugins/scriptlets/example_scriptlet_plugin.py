#!/usr/bin/env python3
"""
Framework0 Example Scriptlet Plugin

Demonstrates IScriptletPlugin interface implementation with script execution,
variable management, output capture, and enhanced logging integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-example-scriptlet
"""

import os  # For environment and file operations
import sys  # For system operations
import subprocess  # For process execution
import tempfile  # For temporary file creation
import shutil  # For file operations
import json  # For JSON handling
import time  # For timing operations
from typing import Dict, Any, List, Optional  # Type safety
from pathlib import Path  # For path operations
from dataclasses import dataclass, field  # Structured data classes

# Import Framework0 plugin interfaces with fallback
try:
    from src.core.plugin_interfaces_v2 import (
        BaseFrameworkPlugin,
        PluginMetadata,
        PluginCapability,
        PluginPriority,
        PluginExecutionContext,
        PluginExecutionResult,
    )
    _HAS_PLUGIN_INTERFACES = True
except ImportError:
    _HAS_PLUGIN_INTERFACES = False
    
    # Fallback definitions for standalone operation
    from enum import Enum
    
    class PluginCapability(Enum):
        """Fallback capability enum."""
        SCRIPT_EXECUTION = "script_execution"
        VARIABLE_MANAGEMENT = "variable_management"
        OUTPUT_CAPTURE = "output_capture"
        ENVIRONMENT_SETUP = "environment_setup"
    
    class PluginPriority(Enum):
        """Fallback priority enum."""
        HIGH = 10
        NORMAL = 50
    
    @dataclass
    class PluginMetadata:
        """Fallback metadata class."""
        plugin_id: str
        name: str
        version: str
        description: str = ""
        author: str = ""
        plugin_type: str = "scriptlet"
        priority: PluginPriority = PluginPriority.NORMAL
    
    @dataclass
    class PluginExecutionContext:
        """Fallback execution context."""
        correlation_id: str = ""
        operation: str = "execute"
        parameters: Dict[str, Any] = field(default_factory=dict)
    
    @dataclass
    class PluginExecutionResult:
        """Fallback execution result."""
        success: bool = True
        result: Any = None
        error: str = ""
        execution_time: float = 0.0
    
    class BaseFrameworkPlugin:
        """Fallback base plugin class."""
        def __init__(self):
            self._logger = None
        
        def initialize(self, context):
            return True
        
        def cleanup(self):
            return True


@dataclass
class ScriptDefinition:
    """Script definition for scriptlet execution."""
    
    script_id: str  # Unique script identifier
    name: str  # Script name
    language: str  # Script language (python, bash, etc.)
    content: str  # Script content/code
    variables: Dict[str, Any] = field(default_factory=dict)  # Script variables
    environment: Dict[str, str] = field(default_factory=dict)  # Environment vars
    timeout: int = 300  # Script timeout in seconds
    working_directory: Optional[str] = None  # Working directory


@dataclass
class ExecutionEnvironment:
    """Execution environment for scripts."""
    
    environment_id: str  # Environment identifier
    name: str  # Environment name
    interpreter_path: str  # Path to interpreter
    base_environment: Dict[str, str] = field(
        default_factory=dict
    )  # Base environment variables
    working_directory: str = ""  # Working directory
    setup_scripts: List[str] = field(default_factory=list)  # Setup scripts


@dataclass
class ScriptExecutionResult:
    """Result of script execution."""
    
    success: bool  # Execution success status
    exit_code: int  # Process exit code
    stdout: str  # Standard output
    stderr: str  # Standard error
    execution_time: float  # Execution time in seconds
    variables_captured: Dict[str, Any] = field(
        default_factory=dict
    )  # Captured variables
    artifacts: List[str] = field(default_factory=list)  # Generated artifacts


class ExampleScriptletPlugin(BaseFrameworkPlugin):
    """
    Example Scriptlet Plugin for Framework0.
    
    Demonstrates comprehensive scriptlet capabilities including:
    - Script execution across multiple languages
    - Variable management and capture
    - Output and error capture
    - Environment setup and management
    """
    
    def __init__(self):
        """Initialize the scriptlet plugin."""
        super().__init__()
        
        # Plugin state
        self._execution_environments: Dict[str, ExecutionEnvironment] = {}
        self._script_registry: Dict[str, ScriptDefinition] = {}
        self._execution_history: List[Dict[str, Any]] = []
        self._variable_store: Dict[str, Any] = {}
        
        # Performance metrics
        self._scripts_executed = 0
        self._total_execution_time = 0.0
        self._environments_created = 0
        
        # Supported languages
        self._supported_languages = {
            "python": {"extensions": [".py"], "shebang": "#!/usr/bin/env python3"},
            "bash": {"extensions": [".sh"], "shebang": "#!/bin/bash"},
            "javascript": {"extensions": [".js"], "interpreter": "node"},
            "powershell": {"extensions": [".ps1"], "interpreter": "pwsh"}
        }
        
        # Create default execution environment
        self._create_default_environment()
        
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata information."""
        return PluginMetadata(
            plugin_id="example_scriptlet_plugin",
            name="Example Scriptlet Plugin",
            version="1.0.0",
            description=("Demonstrates comprehensive scriptlet capabilities "
                        "with script execution and variable management"),
            author="Framework0 Development Team",
            plugin_type="scriptlet",
            priority=PluginPriority.HIGH
        )
        
    def get_capabilities(self) -> List[PluginCapability]:
        """Get list of plugin capabilities."""
        return [
            PluginCapability.SCRIPT_EXECUTION,
            PluginCapability.VARIABLE_MANAGEMENT,
            PluginCapability.OUTPUT_CAPTURE,
            PluginCapability.ENVIRONMENT_SETUP
        ]
        
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin functionality based on operation type."""
        start_time = time.time()
        
        try:
            operation = context.operation
            parameters = context.parameters
            
            if self._logger:
                self._logger.info(f"Executing scriptlet operation: {operation}")
            
            # Route to appropriate operation handler
            if operation == "execute_script":
                result = self._handle_script_execution(parameters, context)
            elif operation == "manage_variables":
                result = self._handle_variable_management(parameters, context)
            elif operation == "setup_environment":
                result = self._handle_environment_setup(parameters, context)
            elif operation == "get_status":
                result = self._handle_status_request(parameters, context)
            else:
                result = PluginExecutionResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )
            
            # Calculate execution time
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            self._total_execution_time += execution_time
            
            if self._logger:
                status = "successful" if result.success else "failed"
                self._logger.info(
                    f"Scriptlet operation {operation} {status} "
                    f"(time: {execution_time:.3f}s)"
                )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Scriptlet plugin execution failed: {e}"
            
            if self._logger:
                self._logger.error(error_msg)
            
            return PluginExecutionResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
    
    def execute_script(
        self,
        script_definition: Dict[str, Any],
        environment_id: Optional[str] = None,
        context: Optional[PluginExecutionContext] = None
    ) -> ScriptExecutionResult:
        """Execute script with given definition and environment."""
        try:
            # Parse script definition
            script = self._parse_script_definition(script_definition)
            
            if self._logger:
                self._logger.info(
                    f"Starting script execution: {script.name} ({script.language})"
                )
            
            # Get execution environment
            env = self._get_execution_environment(environment_id)
            
            # Execute script based on language
            if script.language == "python":
                result = self._execute_python_script(script, env)
            elif script.language == "bash":
                result = self._execute_bash_script(script, env)
            elif script.language == "javascript":
                result = self._execute_javascript_script(script, env)
            elif script.language == "powershell":
                result = self._execute_powershell_script(script, env)
            else:
                return ScriptExecutionResult(
                    success=False,
                    exit_code=-1,
                    stdout="",
                    stderr=f"Unsupported script language: {script.language}",
                    execution_time=0.0
                )
            
            # Update execution history
            self._update_execution_history(script, result, env)
            self._scripts_executed += 1
            
            if self._logger:
                status = "successful" if result.success else "failed"
                self._logger.info(
                    f"Script execution {status}: {script.name} "
                    f"(exit code: {result.exit_code})"
                )
            
            return result
            
        except Exception as e:
            error_msg = f"Script execution failed: {e}"
            if self._logger:
                self._logger.error(error_msg)
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=error_msg,
                execution_time=0.0
            )
    
    def manage_variables(
        self,
        operation_type: str,
        variables: Dict[str, Any],
        context: Optional[PluginExecutionContext] = None
    ) -> Dict[str, Any]:
        """Manage script variables (set, get, delete, list)."""
        try:
            if operation_type == "set":
                self._variable_store.update(variables)
                return {"operation": "set", "variables_set": list(variables.keys())}
                
            elif operation_type == "get":
                requested_vars = variables.get("variables", [])
                result_vars = {}
                for var in requested_vars:
                    result_vars[var] = self._variable_store.get(var)
                return {"operation": "get", "variables": result_vars}
                
            elif operation_type == "delete":
                requested_vars = variables.get("variables", [])
                deleted = []
                for var in requested_vars:
                    if var in self._variable_store:
                        del self._variable_store[var]
                        deleted.append(var)
                return {"operation": "delete", "variables_deleted": deleted}
                
            elif operation_type == "list":
                return {
                    "operation": "list",
                    "variables": dict(self._variable_store),
                    "count": len(self._variable_store)
                }
            else:
                raise ValueError(f"Unknown variable operation: {operation_type}")
                
        except Exception as e:
            return {"operation": operation_type, "error": str(e), "success": False}
    
    def _handle_script_execution(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle script execution operation."""
        script_definition = parameters.get("script_definition", {})
        environment_id = parameters.get("environment_id")
        
        result = self.execute_script(script_definition, environment_id, context)
        
        return PluginExecutionResult(
            success=result.success,
            result={
                "exit_code": result.exit_code,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": result.execution_time,
                "variables_captured": result.variables_captured,
                "artifacts": result.artifacts
            },
            error=result.stderr if not result.success else ""
        )
    
    def _handle_variable_management(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle variable management operations."""
        operation_type = parameters.get("operation_type", "list")
        variables = parameters.get("variables", {})
        
        result = self.manage_variables(operation_type, variables, context)
        
        return PluginExecutionResult(
            success=result.get("success", True),
            result=result,
            error=result.get("error", "")
        )
    
    def _handle_environment_setup(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle environment setup operations."""
        try:
            env_definition = parameters.get("environment_definition", {})
            env = self._create_execution_environment(env_definition)
            
            result_data = {
                "environment_id": env.environment_id,
                "name": env.name,
                "interpreter_path": env.interpreter_path,
                "working_directory": env.working_directory
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Environment setup failed: {e}"
            )
    
    def _handle_status_request(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Handle status request operation."""
        try:
            status_data = {
                "plugin_status": {
                    "scripts_executed": self._scripts_executed,
                    "environments_created": self._environments_created,
                    "total_execution_time": self._total_execution_time,
                    "registered_scripts": len(self._script_registry),
                    "variables_stored": len(self._variable_store),
                    "supported_languages": list(self._supported_languages.keys())
                },
                "execution_environments": [
                    {
                        "environment_id": env_id,
                        "name": env.name,
                        "interpreter_path": env.interpreter_path
                    }
                    for env_id, env in self._execution_environments.items()
                ],
                "recent_execution_history": [
                    {
                        "script_name": entry["script_name"],
                        "language": entry["language"],
                        "success": entry["success"],
                        "execution_time": entry["execution_time"]
                    }
                    for entry in self._execution_history[-5:]  # Last 5 executions
                ]
            }
            
            return PluginExecutionResult(success=True, result=status_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Status request failed: {e}"
            )
    
    def _parse_script_definition(
        self,
        definition: Dict[str, Any]
    ) -> ScriptDefinition:
        """Parse script definition from dictionary."""
        return ScriptDefinition(
            script_id=definition.get("script_id", f"script_{int(time.time())}"),
            name=definition.get("name", "Untitled Script"),
            language=definition.get("language", "python"),
            content=definition.get("content", ""),
            variables=definition.get("variables", {}),
            environment=definition.get("environment", {}),
            timeout=definition.get("timeout", 300),
            working_directory=definition.get("working_directory")
        )
    
    def _get_execution_environment(
        self,
        environment_id: Optional[str]
    ) -> ExecutionEnvironment:
        """Get execution environment by ID or default."""
        if environment_id and environment_id in self._execution_environments:
            return self._execution_environments[environment_id]
        return self._execution_environments["default"]
    
    def _create_default_environment(self):
        """Create default execution environment."""
        default_env = ExecutionEnvironment(
            environment_id="default",
            name="Default Environment",
            interpreter_path=sys.executable,
            base_environment=dict(os.environ),
            working_directory=str(Path.cwd())
        )
        self._execution_environments["default"] = default_env
    
    def _create_execution_environment(
        self,
        definition: Dict[str, Any]
    ) -> ExecutionEnvironment:
        """Create new execution environment from definition."""
        env = ExecutionEnvironment(
            environment_id=definition.get("environment_id", f"env_{int(time.time())}"),
            name=definition.get("name", "Custom Environment"),
            interpreter_path=definition.get(
                "interpreter_path",
                sys.executable
            ),
            base_environment=definition.get("base_environment", dict(os.environ)),
            working_directory=definition.get(
                "working_directory",
                str(Path.cwd())
            ),
            setup_scripts=definition.get("setup_scripts", [])
        )
        
        self._execution_environments[env.environment_id] = env
        self._environments_created += 1
        return env
    
    def _execute_python_script(
        self,
        script: ScriptDefinition,
        env: ExecutionEnvironment
    ) -> ScriptExecutionResult:
        """Execute Python script."""
        start_time = time.time()
        
        try:
            # Create temporary script file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False
            ) as temp_file:
                # Add variable injection if needed
                if script.variables:
                    var_injection = "\n".join([
                        f"{k} = {repr(v)}" for k, v in script.variables.items()
                    ])
                    temp_file.write(var_injection + "\n\n")
                
                temp_file.write(script.content)
                temp_file_path = temp_file.name
            
            # Prepare environment
            exec_env = env.base_environment.copy()
            exec_env.update(script.environment)
            
            # Execute script
            result = subprocess.run(
                [env.interpreter_path, temp_file_path],
                capture_output=True,
                text=True,
                timeout=script.timeout,
                env=exec_env,
                cwd=script.working_directory or env.working_directory
            )
            
            execution_time = time.time() - start_time
            
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
            
            return ScriptExecutionResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                variables_captured={},  # Could implement variable capture
                artifacts=[]
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Script execution timed out after {script.timeout}s",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Python script execution failed: {e}",
                execution_time=execution_time
            )
    
    def _execute_bash_script(
        self,
        script: ScriptDefinition,
        env: ExecutionEnvironment
    ) -> ScriptExecutionResult:
        """Execute Bash script."""
        start_time = time.time()
        
        try:
            # Create temporary script file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.sh',
                delete=False
            ) as temp_file:
                temp_file.write("#!/bin/bash\n")
                
                # Add variable exports
                if script.variables:
                    for k, v in script.variables.items():
                        temp_file.write(f'export {k}="{v}"\n')
                    temp_file.write("\n")
                
                temp_file.write(script.content)
                temp_file_path = temp_file.name
            
            # Make script executable
            os.chmod(temp_file_path, 0o755)
            
            # Prepare environment
            exec_env = env.base_environment.copy()
            exec_env.update(script.environment)
            
            # Execute script
            result = subprocess.run(
                ["/bin/bash", temp_file_path],
                capture_output=True,
                text=True,
                timeout=script.timeout,
                env=exec_env,
                cwd=script.working_directory or env.working_directory
            )
            
            execution_time = time.time() - start_time
            
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
            
            return ScriptExecutionResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Script execution timed out after {script.timeout}s",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Bash script execution failed: {e}",
                execution_time=execution_time
            )
    
    def _execute_javascript_script(
        self,
        script: ScriptDefinition,
        env: ExecutionEnvironment
    ) -> ScriptExecutionResult:
        """Execute JavaScript script."""
        # Check if Node.js is available
        if not shutil.which("node"):
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr="Node.js not found. Please install Node.js to run JavaScript scripts.",
                execution_time=0.0
            )
        
        start_time = time.time()
        
        try:
            # Create temporary script file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.js',
                delete=False
            ) as temp_file:
                # Add variable injection
                if script.variables:
                    for k, v in script.variables.items():
                        temp_file.write(f"const {k} = {json.dumps(v)};\n")
                    temp_file.write("\n")
                
                temp_file.write(script.content)
                temp_file_path = temp_file.name
            
            # Prepare environment
            exec_env = env.base_environment.copy()
            exec_env.update(script.environment)
            
            # Execute script
            result = subprocess.run(
                ["node", temp_file_path],
                capture_output=True,
                text=True,
                timeout=script.timeout,
                env=exec_env,
                cwd=script.working_directory or env.working_directory
            )
            
            execution_time = time.time() - start_time
            
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
            
            return ScriptExecutionResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Script execution timed out after {script.timeout}s",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"JavaScript script execution failed: {e}",
                execution_time=execution_time
            )
    
    def _execute_powershell_script(
        self,
        script: ScriptDefinition,
        env: ExecutionEnvironment
    ) -> ScriptExecutionResult:
        """Execute PowerShell script."""
        # Check if PowerShell is available
        if not shutil.which("pwsh") and not shutil.which("powershell"):
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr="PowerShell not found. Please install PowerShell Core.",
                execution_time=0.0
            )
        
        start_time = time.time()
        
        try:
            # Create temporary script file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.ps1',
                delete=False
            ) as temp_file:
                # Add variable assignments
                if script.variables:
                    for k, v in script.variables.items():
                        if isinstance(v, str):
                            temp_file.write(f'${k} = "{v}"\n')
                        else:
                            temp_file.write(f'${k} = {v}\n')
                    temp_file.write("\n")
                
                temp_file.write(script.content)
                temp_file_path = temp_file.name
            
            # Prepare environment
            exec_env = env.base_environment.copy()
            exec_env.update(script.environment)
            
            # Determine PowerShell executable
            ps_executable = "pwsh" if shutil.which("pwsh") else "powershell"
            
            # Execute script
            result = subprocess.run(
                [ps_executable, "-File", temp_file_path],
                capture_output=True,
                text=True,
                timeout=script.timeout,
                env=exec_env,
                cwd=script.working_directory or env.working_directory
            )
            
            execution_time = time.time() - start_time
            
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
            
            return ScriptExecutionResult(
                success=result.returncode == 0,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"Script execution timed out after {script.timeout}s",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ScriptExecutionResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=f"PowerShell script execution failed: {e}",
                execution_time=execution_time
            )
    
    def _update_execution_history(
        self,
        script: ScriptDefinition,
        result: ScriptExecutionResult,
        env: ExecutionEnvironment
    ):
        """Update execution history with script execution result."""
        history_entry = {
            "script_id": script.script_id,
            "script_name": script.name,
            "language": script.language,
            "environment_id": env.environment_id,
            "success": result.success,
            "exit_code": result.exit_code,
            "execution_time": result.execution_time,
            "timestamp": time.time(),
            "stdout_length": len(result.stdout),
            "stderr_length": len(result.stderr)
        }
        
        self._execution_history.append(history_entry)
        
        # Keep only last 100 executions
        if len(self._execution_history) > 100:
            self._execution_history = self._execution_history[-100:]


# Plugin registration and example usage
if __name__ == "__main__":
    # Create plugin instance
    plugin = ExampleScriptletPlugin()
    
    # Initialize plugin
    init_context = {"logger": None}
    plugin.initialize(init_context)
    
    print("✅ Example Scriptlet Plugin Implemented!")
    print(f"\nPlugin Metadata:")
    metadata = plugin.get_metadata()
    print(f"   Name: {metadata.name}")
    print(f"   Version: {metadata.version}")
    print(f"   Type: {metadata.plugin_type}")
    print(f"   Description: {metadata.description}")
    
    print(f"\nCapabilities: {[cap.value for cap in plugin.get_capabilities()]}")
    
    # Example Python script
    python_script = {
        "script_id": "example_python_001",
        "name": "Example Python Script",
        "language": "python",
        "content": '''
import os
import sys
print(f"Hello from Python!")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Variable greeting: {greeting}")
''',
        "variables": {"greeting": "Hello Framework0!"},
        "timeout": 30
    }
    
    # Execute Python script
    print(f"\nExecuting Python Script...")
    python_result = plugin.execute_script(python_script)
    print(f"Python Script Result:")
    print(f"   Success: {python_result.success}")
    print(f"   Exit Code: {python_result.exit_code}")
    print(f"   Execution Time: {python_result.execution_time:.3f}s")
    print(f"   Output: {python_result.stdout.strip()}")
    if python_result.stderr:
        print(f"   Error: {python_result.stderr}")
    
    # Example Bash script
    bash_script = {
        "script_id": "example_bash_001",
        "name": "Example Bash Script",
        "language": "bash",
        "content": '''
echo "Hello from Bash!"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Message variable: $message"
ls -la | head -5
''',
        "variables": {"message": "Framework0 is awesome!"},
        "timeout": 30
    }
    
    # Execute Bash script
    print(f"\nExecuting Bash Script...")
    bash_result = plugin.execute_script(bash_script)
    print(f"Bash Script Result:")
    print(f"   Success: {bash_result.success}")
    print(f"   Exit Code: {bash_result.exit_code}")
    print(f"   Execution Time: {bash_result.execution_time:.3f}s")
    if bash_result.stdout:
        print(f"   Output: {bash_result.stdout.strip()}")
    if bash_result.stderr:
        print(f"   Error: {bash_result.stderr}")
    
    # Variable management example
    print(f"\nTesting Variable Management...")
    
    # Set variables
    var_result = plugin.manage_variables("set", {
        "test_var1": "Hello World",
        "test_var2": 42,
        "test_var3": {"nested": "data"}
    })
    print(f"Set Variables: {var_result}")
    
    # Get variables
    var_result = plugin.manage_variables("get", {
        "variables": ["test_var1", "test_var2", "nonexistent"]
    })
    print(f"Get Variables: {var_result}")
    
    # List all variables
    var_result = plugin.manage_variables("list", {})
    print(f"List Variables: {var_result['count']} variables stored")
    
    print("\nKey Features Demonstrated:")
    print("   ✓ Multi-language script execution (Python, Bash, JS, PowerShell)")
    print("   ✓ Variable injection and management")
    print("   ✓ Output and error capture")
    print("   ✓ Timeout and error handling")
    print("   ✓ Execution environment management")
    print("   ✓ Performance metrics tracking")
    print("   ✓ Execution history maintenance")
    
    # Cleanup
    plugin.cleanup()