#!/usr/bin/env python3
"""
Framework0 Workspace Cleaner - Production Baseline Manager
==============================================================================
Maintains Framework0 baseline while enabling clean development cycles.

This tool preserves the essential Framework0 components established during
restructuring and uses them as the foundation for future development. It
provides controlled cleanup that maintains the baseline integrity while
removing development artifacts and experimental code.

Key Features:
- Preserves Framework0 baseline components (orchestrator, src, scriptlets)
- Maintains essential documentation and configuration
- Removes development artifacts while keeping core structure
- Creates development-ready workspace from baseline
- Backup and restore capabilities for safety
- Comprehensive logging and reporting

Usage:
    python tools/framework0_workspace_cleaner.py --mode [clean|reset|backup]

Author: Framework0 Team
Version: 1.0.0 (Post-Restructure Baseline)
License: MIT
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from orchestrator.context.context import Context
    from src.core.logger import get_logger

    HAS_FRAMEWORK = True
except ImportError:
    # Fallback if Framework0 components aren't available
    HAS_FRAMEWORK = False
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


@dataclass
class CleanupReport:
    """Comprehensive cleanup operation report."""

    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    mode: str = ""
    files_removed: List[str] = field(default_factory=list)
    files_preserved: List[str] = field(default_factory=list)
    directories_created: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    backup_location: Optional[str] = None

    @property
    def duration_seconds(self) -> float:
        """Calculate operation duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for JSON serialization."""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "mode": self.mode,
            "files_removed": len(self.files_removed),
            "files_preserved": len(self.files_preserved),
            "directories_created": len(self.directories_created),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "backup_location": self.backup_location,
            "success": len(self.errors) == 0,
        }


class Framework0WorkspaceCleaner:
    """
    Framework0-aware workspace cleaner that maintains baseline integrity.

    This cleaner is designed to work with the Framework0 baseline established
    during the workspace restructuring. It preserves essential components while
    providing clean development environments.
    """

    def __init__(self, workspace_path: str = None):
        """Initialize Framework0 workspace cleaner."""
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.report = CleanupReport()

        # Initialize logger and context if available
        if HAS_FRAMEWORK:
            self.logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
            self.context = Context()
        else:
            self.logger = logger
            self.context = None

        self.logger.info(f"Framework0 Workspace Cleaner initialized for: {self.workspace_path}")

        # Framework0 baseline components - ALWAYS PRESERVE
        self.framework0_core = {
            # Core orchestrator components
            "orchestrator/__init__.py",
            "orchestrator/context_client.py",
            "orchestrator/enhanced_memory_bus.py",
            "orchestrator/enhanced_recipe_parser.py",
            "orchestrator/runner.py",
            "orchestrator/context/",
            "orchestrator/persistence/",
            "orchestrator/recipes/",
            # Source framework components
            "src/__init__.py",
            "src/core/",
            "src/analysis/",
            "src/visualization/",
            "src/basic_usage.py",
            "src/dash_demo.py",
            "src/integration_demo.py",
            # Scriptlet framework
            "scriptlets/__init__.py",
            "scriptlets/framework.py",
            # Server configuration
            "server/__init__.py",
            "server/server_config.py",
            # Analysis framework
            "analysis/__init__.py",
            # CLI framework
            "cli/__init__.py",
            # Storage framework
            "storage/__init__.py",
            # Essential documentation
            "README.md",
            "CONTRIBUTING.md",
            ".github/copilot-instructions.md",
            # Configuration files
            "requirements.txt",
            "pyproject.toml",
            "setup.cfg",
            "docker-compose.yml",
            "Dockerfile",
            # Essential tools
            "tools/__init__.py",
            "tools/baseline_framework_analyzer.py",
            "tools/baseline_documentation_updater.py",
            "tools/documentation_updater.py",
            "tools/framework0_workspace_cleaner.py",  # This file itself
            "tools/post_restructure_validator.py",
            # Test framework
            "tests/__init__.py",
            "tests/test_core_functionality.py",
            "tests/test_enhanced_context_server.py",
            "tests/test_enhanced_memory_bus.py",
            "tests/test_enhanced_recipe_parser.py",
            "tests/test_framework0_integration.py",
            # Build and deployment
            "start_server.sh",
        }

        # Development artifacts - REMOVE during cleanup
        self.development_artifacts = {
            # Cache and temporary files
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".pytest_cache/",
            ".coverage",
            "htmlcov/",
            # IDE and editor files
            ".vscode/settings.json",
            ".idea/",
            "*.swp",
            "*.swo",
            "*~",
            # Logs and debug files
            "*.log",
            "debug_*.py",
            "temp_*.py",
            "test_*.tmp",
            # Development databases and data
            "*.db",
            "*.sqlite",
            "data/*.json",
            "output/",
            "tmp/",
            # Backup files from development
            "*.backup",
            "*.bak",
            "*_old.*",
            "*_backup.*",
            # Jupyter checkpoints
            ".ipynb_checkpoints/",
            # Experimental directories
            "experiments/",
            "prototypes/",
            "sandbox/",
            "playground/",
        }

        # Optional components - PRESERVE with warning
        self.optional_components = {
            "examples/",  # May contain user examples
            "docs/",  # Additional documentation
            "visualization_output/",  # Generated visualizations
            "context_dumps/",  # Context state dumps
            ".venv/",  # Virtual environment
            ".git/",  # Git repository
        }

    def create_backup(self, backup_name: str = None) -> str:
        """Create backup of workspace before cleanup."""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"framework0_backup_{timestamp}"

        backup_path = self.workspace_path.parent / backup_name

        self.logger.info(f"Creating workspace backup: {backup_path}")

        try:
            if backup_path.exists():
                shutil.rmtree(backup_path)

            # Define ignore patterns for backup (exclude large/unnecessary directories)
            def ignore_large_dirs(dir_path: str, contents: list[str]) -> list[str]:
                """Ignore function to exclude large directories and temp files from backup."""
                ignored = []
                for item in contents:
                    # Ignore virtual environments, cache, and large directories
                    if item in {
                        ".venv",
                        "venv",
                        "__pycache__",
                        ".git",
                        "node_modules",
                        ".pytest_cache",
                        ".coverage",
                        "dist",
                        "build",
                        ".tox",
                        "visualization_output",
                    } or item.endswith(".pyc"):
                        ignored.append(item)
                return ignored

            shutil.copytree(self.workspace_path, backup_path, ignore=ignore_large_dirs)

            self.report.backup_location = str(backup_path)
            self.logger.info(f"✅ Backup created successfully: {backup_path}")
            return str(backup_path)

        except Exception as e:
            error_msg = f"Failed to create backup: {e}"
            self.logger.error(error_msg)
            self.report.errors.append(error_msg)
            raise

    def preserve_framework0_baseline(self) -> None:
        """Ensure Framework0 baseline components are preserved."""
        self.logger.info("🛡️  Verifying Framework0 baseline preservation...")

        missing_components = []

        for component in self.framework0_core:
            component_path = self.workspace_path / component

            if not component_path.exists():
                missing_components.append(component)
                self.logger.warning(f"⚠️  Missing Framework0 component: {component}")
            else:
                self.report.files_preserved.append(str(component_path))

        if missing_components:
            warning_msg = f"Missing {len(missing_components)} Framework0 baseline components"
            self.report.warnings.append(warning_msg)
            self.logger.warning(f"⚠️  {warning_msg}")

        self.logger.info(
            f"✅ Framework0 baseline verified: {len(self.framework0_core) - len(missing_components)}/{len(self.framework0_core)} components present"
        )

    def clean_development_artifacts(self, dry_run: bool = False) -> None:
        """Remove development artifacts while preserving Framework0 baseline."""
        self.logger.info("🧹 Cleaning development artifacts...")

        removed_count = 0

        for root, dirs, files in os.walk(self.workspace_path):
            # Skip Framework0 core directories
            root_path = Path(root)
            relative_root = root_path.relative_to(self.workspace_path)

            # Check if this is a Framework0 core directory
            if any(
                str(relative_root).startswith(core_path.rstrip("/"))
                for core_path in self.framework0_core
                if core_path.endswith("/")
            ):
                continue

            # Remove matching artifacts
            for pattern in self.development_artifacts:
                if pattern.endswith("/"):
                    # Directory pattern
                    pattern_name = pattern.rstrip("/")
                    if pattern_name in dirs:
                        dir_path = root_path / pattern_name
                        self.logger.debug(f"Removing directory: {dir_path}")

                        if not dry_run:
                            try:
                                shutil.rmtree(dir_path)
                                self.report.files_removed.append(str(dir_path))
                                removed_count += 1
                            except Exception as e:
                                error_msg = f"Failed to remove {dir_path}: {e}"
                                self.logger.error(error_msg)
                                self.report.errors.append(error_msg)
                else:
                    # File pattern
                    import glob

                    matching_files = glob.glob(str(root_path / pattern))
                    for file_path in matching_files:
                        file_path = Path(file_path)

                        # Skip if it's a Framework0 core file
                        relative_file = file_path.relative_to(self.workspace_path)
                        if str(relative_file) in self.framework0_core:
                            continue

                        self.logger.debug(f"Removing file: {file_path}")

                        if not dry_run:
                            try:
                                file_path.unlink()
                                self.report.files_removed.append(str(file_path))
                                removed_count += 1
                            except Exception as e:
                                error_msg = f"Failed to remove {file_path}: {e}"
                                self.logger.error(error_msg)
                                self.report.errors.append(error_msg)

        self.logger.info(f"✅ Cleaned {removed_count} development artifacts")

    def create_development_structure(self) -> None:
        """Create fresh development directories for new work."""
        self.logger.info("🏗️  Creating development structure...")

        dev_directories = [
            "experiments",  # For experimental features
            "prototypes",  # For prototype implementations
            "examples/new",  # For new examples
            "docs/development",  # For development documentation
            "tests/integration",  # For integration tests
            "tests/performance",  # For performance tests
            "data/input",  # For input data
            "data/output",  # For output data
            "logs",  # For log files
            "tmp",  # For temporary files
        ]

        for directory in dev_directories:
            dir_path = self.workspace_path / directory

            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    self.report.directories_created.append(str(dir_path))
                    self.logger.debug(f"Created directory: {dir_path}")

                    # Create .gitkeep file to preserve empty directories
                    gitkeep_path = dir_path / ".gitkeep"
                    gitkeep_path.touch()

                except Exception as e:
                    error_msg = f"Failed to create directory {dir_path}: {e}"
                    self.logger.error(error_msg)
                    self.report.errors.append(error_msg)

        self.logger.info(f"✅ Created {len(self.report.directories_created)} development directories")

    def create_development_template_files(self) -> None:
        """Create template files to guide development."""
        self.logger.info("📝 Creating development template files...")

        templates = {
            "experiments/README.md": """# Experiments Directory

Place experimental features and proof-of-concepts here.

## Structure
- Each experiment should have its own subdirectory
- Include README.md explaining the experiment
- Test files should go in tests/integration/

## Framework0 Integration
- Use `from orchestrator.context.context import Context` for state management
- Use `from src.core.logger import get_logger` for logging  
- Follow existing patterns in src/ directory
""",
            "prototypes/README.md": """# Prototypes Directory

Develop production-ready prototypes here before integration.

## Guidelines
- Follow Framework0 patterns and architecture
- Include comprehensive tests
- Document integration points
- Plan migration path to src/ or orchestrator/

## Integration Checklist
- [ ] Uses Framework0 Context system
- [ ] Follows logging patterns
- [ ] Has unit tests
- [ ] Has integration tests
- [ ] Documentation complete
""",
            "examples/new/README.md": """# New Examples

Create examples demonstrating Framework0 capabilities.

## Example Structure
- Include working code samples
- Provide clear documentation  
- Show integration patterns
- Demonstrate best practices

## Framework0 Features to Showcase
- Context management
- Recipe execution
- Analysis framework
- Visualization system
- Scriptlet development
""",
        }

        for file_path, content in templates.items():
            full_path = self.workspace_path / file_path

            if not full_path.exists():
                try:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                    self.logger.debug(f"Created template: {full_path}")
                except Exception as e:
                    error_msg = f"Failed to create template {full_path}: {e}"
                    self.logger.error(error_msg)
                    self.report.errors.append(error_msg)

        self.logger.info("✅ Development templates created")

    def validate_framework0_integrity(self) -> bool:
        """Validate that Framework0 baseline is intact after cleanup."""
        self.logger.info("🔍 Validating Framework0 integrity...")

        validation_errors = []

        # Check critical imports
        critical_imports = [
            "orchestrator.context.context",
            "orchestrator.enhanced_memory_bus",
            "orchestrator.enhanced_recipe_parser",
            "src.core.logger",
            "src.analysis.framework",
            "scriptlets.framework",
        ]

        for import_path in critical_imports:
            try:
                __import__(import_path)
                self.logger.debug(f"✅ Import validated: {import_path}")
            except ImportError as e:
                validation_errors.append(f"Import failed: {import_path} - {e}")
                self.logger.error(f"❌ Import validation failed: {import_path}")

        # Check essential files exist
        for component in self.framework0_core:
            if not component.endswith("/"):  # Skip directory entries
                component_path = self.workspace_path / component
                if not component_path.exists():
                    validation_errors.append(f"Missing essential file: {component}")

        if validation_errors:
            self.report.errors.extend(validation_errors)
            self.logger.error(f"❌ Framework0 integrity validation failed: {len(validation_errors)} errors")
            return False
        else:
            self.logger.info("✅ Framework0 integrity validated successfully")
            return True

    def generate_cleanup_report(self) -> str:
        """Generate comprehensive cleanup report."""
        self.report.end_time = datetime.now()

        report_path = self.workspace_path / "logs" / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(report_path, "w") as f:
                json.dump(self.report.to_dict(), f, indent=2)

            self.logger.info(f"📊 Cleanup report generated: {report_path}")
            return str(report_path)

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")
            return ""

    def run_clean_mode(self, dry_run: bool = False, create_backup: bool = True) -> bool:
        """Execute clean mode - remove development artifacts while preserving baseline."""
        self.report.mode = "clean"
        self.logger.info("🚀 Starting Framework0 workspace cleaning (clean mode)")

        try:
            # Create backup if requested
            if create_backup and not dry_run:
                self.create_backup()

            # Preserve Framework0 baseline
            self.preserve_framework0_baseline()

            # Clean development artifacts
            self.clean_development_artifacts(dry_run=dry_run)

            # Validate integrity
            if not dry_run:
                integrity_ok = self.validate_framework0_integrity()
                if not integrity_ok:
                    self.logger.error("❌ Framework0 integrity validation failed")
                    return False

            # Generate report
            if not dry_run:
                self.generate_cleanup_report()

            self.logger.info("✅ Framework0 workspace cleaning completed successfully")
            return True

        except Exception as e:
            error_msg = f"Cleanup failed: {e}"
            self.logger.error(error_msg)
            self.report.errors.append(error_msg)
            return False

    def run_reset_mode(self, create_backup: bool = True) -> bool:
        """Execute reset mode - clean artifacts and create fresh development structure."""
        self.report.mode = "reset"
        self.logger.info("🚀 Starting Framework0 workspace reset (reset mode)")

        try:
            # Create backup
            if create_backup:
                self.create_backup()

            # Clean development artifacts
            self.clean_development_artifacts()

            # Create fresh development structure
            self.create_development_structure()

            # Create template files
            self.create_development_template_files()

            # Validate integrity
            integrity_ok = self.validate_framework0_integrity()
            if not integrity_ok:
                self.logger.error("❌ Framework0 integrity validation failed")
                return False

            # Generate report
            self.generate_cleanup_report()

            self.logger.info("✅ Framework0 workspace reset completed successfully")
            return True

        except Exception as e:
            error_msg = f"Reset failed: {e}"
            self.logger.error(error_msg)
            self.report.errors.append(error_msg)
            return False

    def run_backup_mode(self, backup_name: str = None) -> bool:
        """Execute backup mode - create backup only."""
        self.report.mode = "backup"
        self.logger.info("🚀 Starting Framework0 workspace backup")

        try:
            backup_path = self.create_backup(backup_name)
            self.logger.info(f"✅ Backup completed: {backup_path}")
            return True

        except Exception as e:
            error_msg = f"Backup failed: {e}"
            self.logger.error(error_msg)
            self.report.errors.append(error_msg)
            return False


def main():
    """Main entry point for Framework0 workspace cleaner."""
    parser = argparse.ArgumentParser(
        description="Framework0 Workspace Cleaner - Maintains baseline while enabling clean development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/framework0_workspace_cleaner.py --mode clean
  python tools/framework0_workspace_cleaner.py --mode reset --no-backup  
  python tools/framework0_workspace_cleaner.py --mode backup --name "pre_feature_work"
  python tools/framework0_workspace_cleaner.py --mode clean --dry-run
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["clean", "reset", "backup"],
        default="clean",
        help="Cleanup mode: clean (remove artifacts), reset (clean + fresh structure), backup (backup only)",
    )

    parser.add_argument("--workspace", default=None, help="Workspace directory path (default: current directory)")

    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes (clean mode only)"
    )

    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation (faster but less safe)")

    parser.add_argument("--name", help="Backup name for backup mode")

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Set debug environment variable if requested
    if args.debug:
        os.environ["DEBUG"] = "1"

    # Initialize cleaner
    cleaner = Framework0WorkspaceCleaner(args.workspace)

    # Execute requested mode
    success = False

    if args.mode == "clean":
        success = cleaner.run_clean_mode(dry_run=args.dry_run, create_backup=not args.no_backup)
    elif args.mode == "reset":
        success = cleaner.run_reset_mode(create_backup=not args.no_backup)
    elif args.mode == "backup":
        success = cleaner.run_backup_mode(args.name)

    # Exit with appropriate code
    if success:
        print(f"\n🎉 Framework0 workspace {args.mode} completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Framework0 workspace {args.mode} failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
