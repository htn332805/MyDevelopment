#!/usr/bin/env python3
"""
Workspace Restructurer for Framework0 Baseline Compliance

This module restructures the entire workspace to comply with the Framework0
baseline directory layout specified in README.md and all development guidelines.
It follows the modular approach with full type safety and comprehensive logging.

Author: Framework0 Development Team  
Date: 2025-10-05
Version: 1.0.0-baseline
"""

import os  # For environment variable access and file system operations
import json  # For JSON serialization of restructuring metadata and analysis
import shutil  # For file and directory operations during restructuring
import subprocess  # For executing git commands and version control operations
from pathlib import Path  # For cross-platform file path handling and operations
from typing import Dict, Any, List, Optional, Set  # For complete type safety and clarity
from dataclasses import dataclass, field  # For structured data classes with defaults
from datetime import datetime  # For timestamping restructuring operations and metadata

# Initialize module logger with debug support from environment
try:
    from src.core.logger import get_logger  # Import Framework0 unified logging system
    logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")  # Create logger instance
except ImportError:  # Handle missing logger during restructuring
    import logging  # Fallback to standard logging
    logging.basicConfig(level=logging.INFO)  # Configure basic logging
    logger = logging.getLogger(__name__)  # Create fallback logger


@dataclass
class RestructureOperation:
    """
    Data class representing a single workspace restructuring operation.
    """
    operation_type: str  # Type of operation (move, copy, create, delete, rename)
    source_path: str  # Source file or directory path (empty for create operations)
    destination_path: str  # Destination file or directory path
    description: str  # Human-readable description of the operation
    priority: int = 0  # Operation priority (0=highest, higher numbers=lower priority)
    requires_backup: bool = True  # Whether operation requires backup before execution
    git_tracked: bool = False  # Whether source file is tracked by git
    dependencies: List[str] = field(default_factory=list)  # Operations that must complete first
    validation_rules: List[str] = field(default_factory=list)  # Post-operation validation requirements


@dataclass
class RestructuringPlan:
    """
    Complete workspace restructuring plan with all operations and metadata.
    """
    version: str  # Restructuring plan version for tracking and compatibility
    timestamp: str  # Plan generation timestamp for auditing and versioning
    workspace_root: str  # Absolute path to workspace root directory
    target_structure: Dict[str, List[str]] = field(default_factory=dict)  # Target directory structure
    operations: List[RestructureOperation] = field(default_factory=list)  # All restructuring operations
    backup_location: str = ""  # Location for backup files during restructuring
    validation_checks: List[str] = field(default_factory=list)  # Post-restructuring validation requirements
    rollback_plan: List[str] = field(default_factory=list)  # Rollback procedures if restructuring fails


class WorkspaceRestructurer:
    """
    Comprehensive workspace restructurer for Framework0 baseline compliance.
    """
    
    def __init__(self, workspace_root: str) -> None:
        """
        Initialize workspace restructurer with current workspace configuration.
        
        Args:
            workspace_root: Absolute path to the workspace root directory
        """
        self.workspace_root = Path(workspace_root).resolve()  # Resolve absolute workspace path
        
        # Target Framework0 directory structure from README.md
        self.target_structure = {  # Define target directory layout
            "orchestrator/": [  # Core orchestration engine
                "context/",  # Context management system
                "enhanced_memory_bus.py",  # Advanced memory management
                "enhanced_recipe_parser.py",  # YAML recipe processing
                "dependency_graph.py",  # DAG execution management
                "persistence/",  # Data persistence layer
                "recipes/",  # Recipe definitions and templates
                "__init__.py"  # Package initialization
            ],
            "scriptlets/": [  # Modular scriptlet framework
                "framework.py",  # Base scriptlet interface
                "core/",  # Core scriptlet components
                "steps/",  # Reusable scriptlet implementations
                "__init__.py"  # Package initialization
            ],
            "src/": [  # Core framework layer
                "core/",  # Fundamental utilities and patterns
                "analysis/",  # Performance analysis tools
                "visualization/",  # Data visualization and reporting
                "modules/",  # Domain-specific modules
                "__init__.py"  # Package initialization
            ],
            "server/": [  # Server infrastructure
                "enhanced_context_server.py",  # Distributed context management
                "__init__.py"  # Package initialization
            ],
            "tests/": [  # Comprehensive testing suite
                "unit/",  # Unit tests
                "integration/",  # Integration tests
                "performance/",  # Performance tests including WebSocket async
                "__init__.py"  # Package initialization
            ],
            "tools/": [  # Development tools
                "baseline_framework_analyzer.py",  # Framework analysis
                "comprehensive_doc_generator.py",  # Documentation generation
                "documentation_updater.py",  # Documentation maintenance
                "lint_checker.py",  # Code compliance checking
                "workspace_restructurer.py",  # This restructuring tool
                "__init__.py"  # Package initialization
            ],
            "docs/": [  # Documentation
                "api_reference.md",  # API documentation
                "getting_started.md",  # Quick start guide
                "architecture.md",  # Architecture documentation
                "deployment_guide.md",  # Deployment instructions
                "troubleshooting.md"  # Troubleshooting guide
            ],
            "cli/": [  # Command-line interface
                "main.py",  # CLI entry point
                "__init__.py"  # Package initialization
            ],
            "storage/": [  # Data storage and persistence
                "db_adapter.py",  # Database adapter
                "__init__.py"  # Package initialization
            ],
            "analysis/": [  # Analysis and reporting
                "charting.py",  # Chart generation
                "exporter.py",  # Data export utilities
                "summarizer.py",  # Text summarization
                "__init__.py"  # Package initialization
            ]
        }
        
        # Initialize restructuring plan
        self.restructuring_plan = RestructuringPlan(
            version="1.0.0-baseline",  # Plan version
            timestamp=datetime.now().isoformat(),  # Current timestamp
            workspace_root=str(self.workspace_root),  # Workspace root path
            target_structure=self.target_structure,  # Target structure
            backup_location=str(self.workspace_root / ".restructuring_backup")  # Backup location
        )
        
        logger.info(f"Initialized workspace restructurer for: {self.workspace_root}")
    
    def analyze_current_structure(self) -> Dict[str, Any]:
        """
        Analyze current workspace structure and identify all files/directories.
        
        Returns:
            Dict[str, Any]: Complete analysis of current workspace structure
        """
        logger.info("Analyzing current workspace structure")
        
        # Discover all files and directories
        current_files = []  # List of all files in workspace
        current_dirs = []  # List of all directories in workspace
        git_tracked_files = set()  # Set of git-tracked files
        
        # Get git-tracked files for safe handling
        try:
            result = subprocess.run(  # Execute git ls-files command
                ["git", "ls-files"], 
                cwd=self.workspace_root,  # Run in workspace directory
                capture_output=True,  # Capture command output
                text=True,  # Return text instead of bytes
                check=True  # Raise exception on error
            )
            if result.stdout.strip():  # If git output exists
                git_tracked_files = set(result.stdout.strip().split('\n'))  # Parse git files
            logger.info(f"Found {len(git_tracked_files)} git-tracked files")
        except subprocess.CalledProcessError as e:  # Handle git command errors
            logger.warning(f"Could not get git-tracked files: {e}")
        
        # Exclude directories from analysis
        exclude_dirs = {
            "__pycache__", ".git", ".vscode", "node_modules",
            ".pytest_cache", "venv", ".venv", "env", ".env",
            "build", "dist", ".tox", "logs", "backup_pre_cleanup",
            "visualization_output", "context_dumps"
        }
        
        # Scan workspace for all files and directories
        for item in self.workspace_root.rglob("*"):  # Recursively find all items
            # Skip excluded directories
            if any(part in exclude_dirs for part in item.parts):
                continue
                
            if item.is_file():  # If item is a file
                relative_path = item.relative_to(self.workspace_root)  # Get relative path
                current_files.append({  # Add file information
                    "path": str(relative_path),  # Relative path string
                    "full_path": str(item),  # Full absolute path
                    "size": item.stat().st_size,  # File size in bytes
                    "git_tracked": str(relative_path) in git_tracked_files,  # Git tracking status
                    "extension": item.suffix,  # File extension
                    "directory": str(relative_path.parent)  # Parent directory
                })
            elif item.is_dir():  # If item is a directory
                relative_path = item.relative_to(self.workspace_root)  # Get relative path
                if str(relative_path) != ".":  # Skip root directory
                    current_dirs.append({  # Add directory information
                        "path": str(relative_path),  # Relative path string
                        "full_path": str(item),  # Full absolute path
                        "file_count": len(list(item.glob("*"))),  # Number of direct children
                        "is_empty": not any(item.iterdir())  # Whether directory is empty
                    })
        
        # Analyze structure compliance
        compliance_analysis = self._analyze_compliance(current_files, current_dirs)  # Check compliance
        
        structure_analysis = {  # Complete structure analysis
            "total_files": len(current_files),  # Total file count
            "total_directories": len(current_dirs),  # Total directory count
            "git_tracked_files": len(git_tracked_files),  # Git-tracked file count
            "current_files": current_files,  # All file details
            "current_directories": current_dirs,  # All directory details
            "compliance_analysis": compliance_analysis,  # Compliance check results
            "analysis_timestamp": datetime.now().isoformat()  # Analysis timestamp
        }
        
        logger.info(f"Structure analysis completed: {len(current_files)} files, {len(current_dirs)} directories")
        return structure_analysis  # Return complete analysis
    
    def _analyze_compliance(self, files: List[Dict[str, Any]], directories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze current structure compliance with Framework0 baseline layout.
        
        Args:
            files: List of file information dictionaries
            directories: List of directory information dictionaries
            
        Returns:
            Dict[str, Any]: Compliance analysis results
        """
        logger.info("Analyzing Framework0 baseline compliance")
        
        # Check for required directories
        required_dirs = set(self.target_structure.keys())  # Required top-level directories
        existing_dirs = set()  # Current top-level directories
        
        # Find existing top-level directories
        for d in directories:
            path_parts = d["path"].split("/")
            if len(path_parts) == 1:  # Top-level directory
                existing_dirs.add(d["path"] + "/")
        
        missing_dirs = required_dirs - existing_dirs  # Directories that need to be created
        extra_dirs = existing_dirs - required_dirs  # Directories that don't fit baseline
        
        # Check for misplaced files
        misplaced_files = []  # Files not in correct locations
        
        for file_info in files:  # Check each file
            file_path = file_info["path"]  # Get file path
            correct_location = self._determine_correct_location(file_path)  # Determine where it should be
            
            if correct_location and not file_path.startswith(correct_location):  # If file is misplaced
                misplaced_files.append({  # Add to misplaced files
                    "current_path": file_path,  # Current file location
                    "correct_location": correct_location,  # Where it should be
                    "reason": self._get_relocation_reason(file_path, correct_location)  # Why it needs to move
                })
        
        # Analyze package structure compliance
        package_compliance = self._check_package_structure()  # Check Python package structure
        
        compliance_results = {  # Complete compliance analysis
            "compliance_score": self._calculate_compliance_score(missing_dirs, extra_dirs, misplaced_files),  # Overall score
            "missing_directories": list(missing_dirs),  # Directories to create
            "extra_directories": list(extra_dirs),  # Directories to relocate or remove
            "misplaced_files": misplaced_files,  # Files to relocate
            "package_compliance": package_compliance,  # Package structure compliance
            "total_issues": len(missing_dirs) + len(extra_dirs) + len(misplaced_files),  # Total compliance issues
            "recommendations": self._generate_compliance_recommendations(missing_dirs, extra_dirs, misplaced_files)  # Fix recommendations
        }
        
        logger.info(f"Compliance analysis: {compliance_results['compliance_score']:.1f}% compliant, {compliance_results['total_issues']} issues")
        return compliance_results  # Return analysis results
    
    def _determine_correct_location(self, file_path: str) -> Optional[str]:
        """
        Determine the correct location for a file based on Framework0 guidelines.
        
        Args:
            file_path: Current file path to analyze
            
        Returns:
            Optional[str]: Correct directory location or None if no relocation needed
        """
        file_name = Path(file_path).name  # Get filename
        file_ext = Path(file_path).suffix  # Get file extension
        
        # Framework0 file classification rules
        if file_name.startswith("test_") and file_ext == ".py":  # Test files
            return "tests/"
        elif file_name in ["lint_checker.py", "documentation_updater.py", "comprehensive_doc_generator.py", "baseline_framework_analyzer.py", "workspace_restructurer.py"]:  # Development tools
            return "tools/"
        elif file_ext == ".md" and file_name != "README.md" and not file_path.startswith("docs/"):  # Documentation files (except README)
            return "docs/"
        elif "context" in file_name.lower() and file_ext == ".py" and not file_path.startswith("orchestrator/"):  # Context-related files
            return "orchestrator/"
        elif file_name in ["recipe_parser.py", "enhanced_recipe_parser.py", "runner.py", "dependency_graph.py", "memory_bus.py", "enhanced_memory_bus.py"] and not file_path.startswith("orchestrator/"):  # Orchestration files
            return "orchestrator/"
        elif ("scriptlet" in file_path.lower() or file_path.startswith("engine/")) and not file_path.startswith("scriptlets/"):  # Scriptlet files
            return "scriptlets/"
        elif ("server" in file_name.lower() or "context_server" in file_name) and file_ext == ".py" and not file_path.startswith("server/"):  # Server files
            return "server/"
        elif file_path.startswith("analysis/") and not file_path.startswith("src/analysis/"):  # Analysis files
            return "src/analysis/"
        elif file_path.startswith("cli/") and file_ext == ".py":  # CLI files
            return "cli/"
        elif file_path.startswith("storage/") and file_ext == ".py":  # Storage files
            return "storage/"
        elif file_ext == ".py" and not any(file_path.startswith(prefix) for prefix in ["tests/", "tools/", "orchestrator/", "scriptlets/", "server/", "src/", "cli/", "storage/"]):  # General Python files
            return "src/"
        
        return None  # No relocation needed
    
    def _get_relocation_reason(self, current_path: str, correct_location: str) -> str:
        """
        Generate human-readable reason for file relocation.
        
        Args:
            current_path: Current file location
            correct_location: Target location for file
            
        Returns:
            str: Human-readable relocation reason
        """
        reasons = {  # Map locations to reasons
            "tests/": "Test files should be organized in the tests/ directory",
            "tools/": "Development tools belong in the tools/ directory",
            "docs/": "Documentation files should be in the docs/ directory",
            "orchestrator/": "Orchestration components belong in orchestrator/",
            "scriptlets/": "Scriptlet components belong in scriptlets/",
            "server/": "Server infrastructure belongs in server/",
            "src/": "Core framework code belongs in src/",
            "src/analysis/": "Analysis tools belong in src/analysis/",
            "cli/": "CLI components belong in cli/",
            "storage/": "Storage components belong in storage/"
        }
        
        return reasons.get(correct_location, f"File should be moved to {correct_location} for Framework0 compliance")  # Return reason
    
    def _check_package_structure(self) -> Dict[str, Any]:
        """
        Check Python package structure compliance with Framework0 guidelines.
        
        Returns:
            Dict[str, Any]: Package structure compliance analysis
        """
        required_init_files = []  # List of required __init__.py files
        
        for directory in self.target_structure.keys():  # Check each target directory
            if directory.endswith("/"):  # If it's a directory
                init_path = f"{directory}__init__.py"  # Required __init__.py path
                full_init_path = self.workspace_root / init_path  # Full path to __init__.py
                
                required_init_files.append({  # Add to required files
                    "path": init_path,  # Relative path
                    "exists": full_init_path.exists(),  # Whether file exists
                    "required": True  # File is required
                })
        
        missing_init_files = [f for f in required_init_files if not f["exists"]]  # Missing __init__.py files
        
        return {  # Package structure analysis
            "required_init_files": len(required_init_files),  # Total required __init__.py files
            "existing_init_files": len([f for f in required_init_files if f["exists"]]),  # Existing __init__.py files
            "missing_init_files": missing_init_files,  # Missing __init__.py files
            "compliance_percentage": (len(required_init_files) - len(missing_init_files)) / len(required_init_files) * 100 if required_init_files else 100  # Compliance percentage
        }
    
    def _calculate_compliance_score(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> float:
        """
        Calculate overall compliance score as percentage.
        
        Args:
            missing_dirs: Set of missing directories
            extra_dirs: Set of extra directories
            misplaced_files: List of misplaced files
            
        Returns:
            float: Compliance score as percentage (0-100)
        """
        total_required_dirs = len(self.target_structure)  # Total required directories
        total_issues = len(missing_dirs) + len(extra_dirs) + len(misplaced_files)  # Total compliance issues
        
        if total_issues == 0:  # If no issues
            return 100.0  # Perfect compliance
        
        # Calculate score based on issues vs requirements
        max_possible_issues = total_required_dirs * 2  # Maximum possible issues
        compliance_score = max(0, 100 - (total_issues / max_possible_issues * 100))  # Calculate score
        
        return min(100, compliance_score)  # Ensure score doesn't exceed 100
    
    def _generate_compliance_recommendations(self, missing_dirs: Set[str], extra_dirs: Set[str], misplaced_files: List[Dict[str, Any]]) -> List[str]:
        """
        Generate actionable compliance recommendations.
        
        Args:
            missing_dirs: Set of missing directories
            extra_dirs: Set of extra directories  
            misplaced_files: List of misplaced files
            
        Returns:
            List[str]: List of actionable recommendations
        """
        recommendations = []  # List of recommendations
        
        if missing_dirs:  # If directories are missing
            recommendations.append(f"Create {len(missing_dirs)} missing Framework0 directories: {', '.join(sorted(missing_dirs))}")
        
        if extra_dirs:  # If extra directories exist
            recommendations.append(f"Evaluate {len(extra_dirs)} extra directories for integration: {', '.join(sorted(extra_dirs))}")
        
        if misplaced_files:  # If files are misplaced
            recommendations.append(f"Relocate {len(misplaced_files)} misplaced files to their correct Framework0 locations")
        
        if not (missing_dirs or extra_dirs or misplaced_files):  # If fully compliant
            recommendations.append("Workspace structure is fully compliant with Framework0 baseline")
        
        return recommendations  # Return all recommendations
    
    def generate_restructuring_plan(self, structure_analysis: Dict[str, Any]) -> RestructuringPlan:
        """
        Generate comprehensive restructuring plan based on structure analysis.
        
        Args:
            structure_analysis: Current workspace structure analysis
            
        Returns:
            RestructuringPlan: Complete restructuring plan with all operations
        """
        logger.info("Generating comprehensive restructuring plan")
        
        operations = []  # List of restructuring operations
        compliance = structure_analysis["compliance_analysis"]  # Get compliance analysis
        
        # Phase 1: Create backup directory
        operations.append(RestructureOperation(  # Add backup creation operation
            operation_type="create",  # Create operation
            source_path="",  # No source for create
            destination_path=self.restructuring_plan.backup_location,  # Backup directory
            description="Create backup directory for restructuring safety",  # Operation description
            priority=0,  # Highest priority
            requires_backup=False  # No backup needed for backup directory
        ))
        
        # Phase 2: Create missing directories
        for missing_dir in compliance["missing_directories"]:  # Create each missing directory
            operations.append(RestructureOperation(  # Add directory creation operation
                operation_type="create",  # Create operation
                source_path="",  # No source for create
                destination_path=missing_dir,  # Target directory
                description=f"Create Framework0 required directory: {missing_dir}",  # Operation description
                priority=1,  # High priority
                requires_backup=False,  # No backup needed for new directories
                validation_rules=[f"Directory {missing_dir} must exist and be accessible"]  # Validation requirements
            ))
        
        # Phase 3: Create missing __init__.py files
        package_compliance = compliance["package_compliance"]  # Get package compliance
        for missing_init in package_compliance["missing_init_files"]:  # Create each missing __init__.py
            operations.append(RestructureOperation(  # Add __init__.py creation operation
                operation_type="create",  # Create operation
                source_path="",  # No source for create
                destination_path=missing_init["path"],  # __init__.py path
                description=f"Create Python package initializer: {missing_init['path']}",  # Operation description
                priority=2,  # Medium-high priority
                requires_backup=False,  # No backup needed for new files
                validation_rules=[f"File {missing_init['path']} must exist and be valid Python"]  # Validation requirements
            ))
        
        # Phase 4: Move misplaced files
        for misplaced in compliance["misplaced_files"]:  # Move each misplaced file
            current_path = misplaced["current_path"]  # Current file location
            correct_location = misplaced["correct_location"]  # Correct file location
            filename = Path(current_path).name  # Get filename
            new_path = f"{correct_location}{filename}"  # New file path
            
            operations.append(RestructureOperation(  # Add file move operation
                operation_type="move",  # Move operation
                source_path=current_path,  # Source file path
                destination_path=new_path,  # Destination file path
                description=f"Relocate {filename}: {misplaced['reason']}",  # Operation description
                priority=3,  # Medium priority
                requires_backup=True,  # Backup required for moves
                git_tracked=current_path in {f["path"] for f in structure_analysis["current_files"] if f["git_tracked"]},  # Git tracking status
                validation_rules=[f"File {new_path} must exist and be identical to original"]  # Validation requirements
            ))
        
        # Update restructuring plan with operations
        self.restructuring_plan.operations = operations  # Set operations
        self.restructuring_plan.validation_checks = self._generate_validation_checks(operations)  # Generate validation checks
        self.restructuring_plan.rollback_plan = self._generate_rollback_plan(operations)  # Generate rollback plan
        
        logger.info(f"Restructuring plan generated: {len(operations)} operations across multiple phases")
        return self.restructuring_plan  # Return complete plan
    
    def _generate_validation_checks(self, operations: List[RestructureOperation]) -> List[str]:
        """
        Generate post-restructuring validation checks.
        
        Args:
            operations: List of restructuring operations
            
        Returns:
            List[str]: List of validation check descriptions
        """
        validation_checks = []  # List of validation checks
        
        # Standard validation checks
        validation_checks.extend([  # Add standard checks
            "All Framework0 required directories exist and are accessible",
            "All Python packages have valid __init__.py files",
            "No files were lost or corrupted during restructuring",
            "Git repository integrity is maintained",
            "All moved files retained their original content and permissions",
            "Python imports continue to work after restructuring",
            "Framework0 baseline compliance score is 100%"
        ])
        
        # Operation-specific validation checks
        for operation in operations:  # Add operation-specific checks
            validation_checks.extend(operation.validation_rules)  # Add operation validation rules
        
        return list(set(validation_checks))  # Return unique validation checks
    
    def _generate_rollback_plan(self, operations: List[RestructureOperation]) -> List[str]:
        """
        Generate rollback plan for failed restructuring.
        
        Args:
            operations: List of restructuring operations
            
        Returns:
            List[str]: List of rollback procedure steps
        """
        rollback_steps = []  # List of rollback steps
        
        rollback_steps.extend([  # Add rollback procedures
            "Stop all Framework0 processes and services",
            "Create emergency backup of current state",
            f"Restore files from backup location: {self.restructuring_plan.backup_location}",
            "Verify git repository integrity with 'git status'",
            "Run 'git fsck' to check repository consistency",
            "Restore original file permissions and ownership",
            "Verify Python imports work with test execution",
            "Document rollback reason and lessons learned",
            "Clean up temporary restructuring files",
            "Restore workspace to pre-restructuring state"
        ])
        
        return rollback_steps  # Return rollback procedures
    
    def save_restructuring_plan(self, output_path: Optional[Path] = None) -> Path:
        """
        Save comprehensive restructuring plan to file for review.
        
        Args:
            output_path: Optional custom output path for plan file
            
        Returns:
            Path: Path to saved restructuring plan file
        """
        if output_path is None:  # If no output path specified
            output_path = self.workspace_root / "WORKSPACE_RESTRUCTURING_PLAN.json"  # Default path
        
        # Convert restructuring plan to serializable format
        plan_data = {  # Plan data structure
            "version": self.restructuring_plan.version,  # Plan version
            "timestamp": self.restructuring_plan.timestamp,  # Plan timestamp
            "workspace_root": self.restructuring_plan.workspace_root,  # Workspace root
            "target_structure": self.restructuring_plan.target_structure,  # Target structure
            "backup_location": self.restructuring_plan.backup_location,  # Backup location
            "operations": [],  # Operations list
            "validation_checks": self.restructuring_plan.validation_checks,  # Validation checks
            "rollback_plan": self.restructuring_plan.rollback_plan  # Rollback procedures
        }
        
        # Convert operations to serializable format
        for operation in self.restructuring_plan.operations:  # Process each operation
            plan_data["operations"].append({  # Add operation data
                "operation_type": operation.operation_type,  # Operation type
                "source_path": operation.source_path,  # Source path
                "destination_path": operation.destination_path,  # Destination path
                "description": operation.description,  # Operation description
                "priority": operation.priority,  # Operation priority
                "requires_backup": operation.requires_backup,  # Backup requirement
                "git_tracked": operation.git_tracked,  # Git tracking status
                "dependencies": operation.dependencies,  # Operation dependencies
                "validation_rules": operation.validation_rules  # Validation requirements
            })
        
        # Save plan to file
        with open(output_path, 'w', encoding='utf-8') as f:  # Open output file
            json.dump(plan_data, f, indent=2, ensure_ascii=False)  # Write JSON data
        
        logger.info(f"Restructuring plan saved to: {output_path}")
        return output_path  # Return output path


def main() -> None:
    """
    Main function to analyze workspace and generate restructuring plan.
    """
    logger.info("🚀 Starting Framework0 workspace restructuring analysis")
    
    try:
        # Detect workspace root directory
        workspace_root = Path.cwd()  # Use current working directory
        
        # Initialize workspace restructurer
        restructurer = WorkspaceRestructurer(str(workspace_root))  # Create restructurer
        
        # Analyze current workspace structure
        structure_analysis = restructurer.analyze_current_structure()  # Analyze structure
        
        # Generate restructuring plan
        restructuring_plan = restructurer.generate_restructuring_plan(structure_analysis)  # Generate plan
        
        # Save restructuring plan for review
        plan_path = restructurer.save_restructuring_plan()  # Save plan
        
        # Generate summary report
        logger.info("📊 Workspace Restructuring Analysis Summary:")
        logger.info(f"   • Current Files: {structure_analysis['total_files']}")
        logger.info(f"   • Current Directories: {structure_analysis['total_directories']}")
        logger.info(f"   • Compliance Score: {structure_analysis['compliance_analysis']['compliance_score']:.1f}%")
        logger.info(f"   • Required Operations: {len(restructuring_plan.operations)}")
        logger.info(f"   • Plan Location: {plan_path}")
        
        # Display compliance issues
        compliance = structure_analysis["compliance_analysis"]  # Get compliance analysis
        if compliance["total_issues"] > 0:  # If issues exist
            logger.info("🔧 Compliance Issues Found:")
            for recommendation in compliance["recommendations"]:  # Display each recommendation
                logger.info(f"   • {recommendation}")
        else:  # If fully compliant
            logger.info("✅ Workspace is fully compliant with Framework0 baseline!")
        
        logger.info("📋 Next Steps:")
        logger.info("   1. Review the generated restructuring plan")
        logger.info("   2. Confirm operations are acceptable")  
        logger.info("   3. Execute restructuring with appropriate tool")
        logger.info("   4. Validate restructured workspace")
        
    except Exception as e:  # Handle analysis errors
        logger.error(f"❌ Workspace restructuring analysis failed: {e}")
        raise  # Re-raise for debugging


if __name__ == "__main__":
    main()  # Execute main function