#!/usr/bin/env python3
"""
Workspace Cleaner - IAF0 Framework Cleanup Tool
==============================================================================
Clean up workspace by removing obsolete files and creating fresh baseline.

This tool:
1. Creates backup of removed files
2. Removes obsolete/duplicate components  
3. Creates fresh directory structure
4. Deploys consolidated components
5. Generates essential configurations
6. Validates baseline integrity
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple

class WorkspaceCleaner:
    """Comprehensive workspace cleanup and baseline creation tool."""
    
    def __init__(self, workspace_path: str):
        """Initialize cleaner with workspace path."""
        self.workspace_path = Path(workspace_path)  # Workspace root directory
        self.backup_dir = self.workspace_path / "backup_pre_cleanup"  # Backup location
        self.cleaned_files: List[str] = []  # Track cleaned files
        self.preserved_files: List[str] = []  # Track preserved files
        self.errors: List[str] = []  # Track any errors
        
        # Files and directories to preserve (consolidated components)
        self.preserve_patterns = {
            # Core consolidated framework files
            "orchestrator/context/context.py",  # Unified Context system
            "scriptlets/framework.py",  # Consolidated scriptlet framework
            "src/analysis/framework.py",  # Analysis framework
            "src/analysis/components.py",  # Analysis components
            "src/analysis/registry.py",  # Analysis registry
            "src/core/logger.py",  # Core logger
            
            # Test suites
            "tests/test_analysis_framework.py",  # Analysis tests
            "tests/test_scriptlet_framework.py",  # Scriptlet tests
            
            # Essential configs and docs
            "README.md",  # Main documentation
            "requirements.txt",  # Dependencies
            "CONTRIBUTING.md",  # Contributing guide
            ".github/copilot-instructions.md",  # Copilot instructions
            
            # Tools
            "tools/",  # Keep tools directory
            
            # Virtual environment
            ".venv/",  # Python virtual environment
        }
        
        # Directories to remove (obsolete/fragmented components)
        self.remove_patterns = {
            "engine/",  # Legacy engine components
            "enhanced_scriptlets/",  # Superseded by consolidated framework
            "orchestrator/context0.py",  # Old context version
            "orchestrator/runner_v2.py",  # Superseded version
            "orchestrator/runner/",  # Old runner components
            "scriptlets/core/",  # Replaced by consolidated framework
            "scriptlets/steps/",  # Legacy steps
            "examples/",  # Old examples (will recreate fresh)
            "unit_test/",  # Replaced by proper tests/ directory
            "server/",  # Legacy server components
            "storage/",  # Legacy storage components
            "cli/",  # Legacy CLI (will recreate if needed)
            "__pycache__/",  # All cache directories
        }
        
        # Files to remove (obsolete individual files)
        self.remove_files = {
            "Context_exercise.ipynb",  # Legacy notebook
            "Context_Module_Manual.md",  # Superseded by README
            "Runner_Module_Manual.md",  # Superseded by README
            "tmux_layout_manual.md",  # Legacy manual
            "user_manual.md",  # Superseded by README
            "repository_overview.md",  # Will regenerate
            "Untitled.ipynb",  # Temporary notebook
            "extract_gpu_info.py",  # Unrelated utility
            "orchestrator/__pycache__/",  # Cache files
            "src/__pycache__/",  # Cache files
        }

    def run_cleanup(self) -> Dict[str, any]:
        """Execute complete workspace cleanup process."""
        print("🧹 Starting workspace cleanup for IAF0 baseline...")
        print(f"📁 Workspace: {self.workspace_path}")
        print(f"💾 Backup location: {self.backup_dir}")
        
        try:
            # Step 1: Create backup
            print("\n📦 Creating backup of files to be removed...")
            self._create_backup()
            
            # Step 2: Remove obsolete files
            print("\n🗑️  Removing obsolete files and directories...")
            self._remove_obsolete_files()
            
            # Step 3: Create fresh directory structure
            print("\n📂 Creating fresh baseline directory structure...")
            self._create_fresh_directories()
            
            # Step 4: Deploy consolidated components
            print("\n🚀 Ensuring consolidated components are properly deployed...")
            self._verify_consolidated_components()
            
            # Step 5: Create essential configurations
            print("\n⚙️  Creating essential configuration files...")
            self._create_essential_configs()
            
            # Step 6: Generate fresh documentation
            print("\n📚 Generating fresh documentation...")
            self._generate_fresh_documentation()
            
            # Step 7: Verify baseline integrity
            print("\n✅ Verifying baseline integrity...")
            integrity_results = self._verify_baseline_integrity()
            
            # Step 8: Generate cleanup report
            print("\n📊 Generating cleanup report...")
            report = self._generate_cleanup_report(integrity_results)
            
            print("\n🎉 Workspace cleanup completed successfully!")
            return report
            
        except Exception as e:
            error_msg = f"Cleanup failed: {str(e)}"
            self.errors.append(error_msg)
            print(f"\n❌ {error_msg}")
            return {"success": False, "error": error_msg, "errors": self.errors}

    def _create_backup(self) -> None:
        """Create backup of files that will be removed."""
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)  # Remove existing backup
        self.backup_dir.mkdir(parents=True, exist_ok=True)  # Create backup directory
        
        backup_count = 0  # Counter for backed up items
        
        # Backup directories to be removed
        for pattern in self.remove_patterns:
            source_path = self.workspace_path / pattern
            if source_path.exists():
                backup_path = self.backup_dir / pattern
                backup_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent dirs
                if source_path.is_dir():
                    shutil.copytree(source_path, backup_path)  # Copy directory
                else:
                    shutil.copy2(source_path, backup_path)  # Copy file
                backup_count += 1
                print(f"  📦 Backed up: {pattern}")
        
        # Backup individual files to be removed
        for file_pattern in self.remove_files:
            source_path = self.workspace_path / file_pattern
            if source_path.exists():
                backup_path = self.backup_dir / file_pattern
                backup_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent dirs
                if source_path.is_dir():
                    shutil.copytree(source_path, backup_path)  # Copy directory
                else:
                    shutil.copy2(source_path, backup_path)  # Copy file
                backup_count += 1
                print(f"  📦 Backed up: {file_pattern}")
        
        print(f"  ✅ Backup complete: {backup_count} items backed up")

    def _remove_obsolete_files(self) -> None:
        """Remove obsolete files and directories."""
        removed_count = 0  # Counter for removed items
        
        # Remove obsolete directories
        for pattern in self.remove_patterns:
            target_path = self.workspace_path / pattern
            if target_path.exists():
                if target_path.is_dir():
                    shutil.rmtree(target_path)  # Remove directory tree
                else:
                    target_path.unlink()  # Remove file
                self.cleaned_files.append(str(pattern))
                removed_count += 1
                print(f"  🗑️  Removed: {pattern}")
        
        # Remove obsolete individual files
        for file_pattern in self.remove_files:
            target_path = self.workspace_path / file_pattern
            if target_path.exists():
                if target_path.is_dir():
                    shutil.rmtree(target_path)  # Remove directory tree
                else:
                    target_path.unlink()  # Remove file
                self.cleaned_files.append(str(file_pattern))
                removed_count += 1
                print(f"  🗑️  Removed: {file_pattern}")
        
        # Remove all __pycache__ directories recursively
        for pycache_dir in self.workspace_path.rglob("__pycache__"):
            if pycache_dir.is_dir():
                shutil.rmtree(pycache_dir)  # Remove cache directory
                self.cleaned_files.append(str(pycache_dir.relative_to(self.workspace_path)))
                removed_count += 1
                print(f"  🗑️  Removed cache: {pycache_dir.relative_to(self.workspace_path)}")
        
        print(f"  ✅ Cleanup complete: {removed_count} items removed")

    def _create_fresh_directories(self) -> None:
        """Create fresh baseline directory structure."""
        fresh_dirs = [
            "src",  # Source code root
            "src/core",  # Core components
            "src/analysis",  # Analysis framework
            "orchestrator",  # Orchestration layer
            "orchestrator/context",  # Context system
            "scriptlets",  # Scriptlet framework
            "tests",  # Test suites
            "tools",  # Development tools
            "docs",  # Documentation
            "examples",  # Fresh examples
            "configs",  # Configuration files
        ]
        
        created_count = 0  # Counter for created directories
        
        for dir_path in fresh_dirs:
            full_path = self.workspace_path / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)  # Create directory
                created_count += 1
                print(f"  📂 Created: {dir_path}")
            else:
                print(f"  📂 Exists: {dir_path}")
        
        print(f"  ✅ Directory structure ready: {created_count} new directories created")

    def _verify_consolidated_components(self) -> None:
        """Verify that all consolidated components are properly in place."""
        essential_files = [
            "orchestrator/context/context.py",  # Context system
            "scriptlets/framework.py",  # Scriptlet framework
            "src/analysis/framework.py",  # Analysis framework
            "src/analysis/components.py",  # Analysis components
            "src/analysis/registry.py",  # Analysis registry
            "src/core/logger.py",  # Core logger
        ]
        
        verified_count = 0  # Counter for verified files
        missing_files = []  # Track missing essential files
        
        for file_path in essential_files:
            full_path = self.workspace_path / file_path
            if full_path.exists():
                self.preserved_files.append(file_path)
                verified_count += 1
                print(f"  ✅ Verified: {file_path}")
            else:
                missing_files.append(file_path)
                print(f"  ❌ Missing: {file_path}")
        
        if missing_files:
            error_msg = f"Missing essential files: {missing_files}"
            self.errors.append(error_msg)
            print(f"  ⚠️  Warning: {error_msg}")
        
        print(f"  ✅ Component verification: {verified_count}/{len(essential_files)} files verified")

    def _create_essential_configs(self) -> None:
        """Create essential configuration files for fresh baseline."""
        
        # Create pyproject.toml for modern Python project configuration
        pyproject_content = '''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "iaf0-framework"
version = "0.1.0"
description = "Integrated Analysis Framework (IAF0) - Modular Python Automation"
authors = [
    {name = "IAF0 Team"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pytest>=7.0.0",
    "pyyaml>=6.0",
    "psutil>=5.9.0",
    "joblib>=1.3.0",
    "black>=23.0.0"
]

[tool.black]
line-length = 88
target-version = ['py311']
include = '\\.pyi?$'

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "--disable-warnings -q"
'''
        
        # Create setup.cfg for additional tool configurations
        setup_cfg_content = '''[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,.venv,build,dist

[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
'''
        
        # Create .gitignore for clean repository
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.venv/
env/
ENV/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
backup_pre_cleanup/
*.log
'''

        configs = [
            ("pyproject.toml", pyproject_content),
            ("setup.cfg", setup_cfg_content),
            (".gitignore", gitignore_content),
        ]
        
        created_count = 0  # Counter for created config files
        
        for filename, content in configs:
            config_path = self.workspace_path / filename
            if not config_path.exists():
                config_path.write_text(content)  # Write configuration file
                created_count += 1
                print(f"  ⚙️  Created: {filename}")
            else:
                print(f"  ⚙️  Exists: {filename}")
        
        print(f"  ✅ Configuration setup: {created_count} new config files created")

    def _generate_fresh_documentation(self) -> None:
        """Generate fresh documentation for baseline framework."""
        
        # Create docs/getting_started.md
        getting_started_content = '''# Getting Started with IAF0 Framework

## Quick Start

### 1. Context System Usage
```python
from orchestrator.context import Context

# Create context instance
ctx = Context()

# Store and retrieve data
ctx.set("app.name", "MyApp", who="setup")
app_name = ctx.get("app.name")

# Track changes
history = ctx.get_history()
```

### 2. Scriptlet Development
```python
from scriptlets import BaseScriptlet, register_scriptlet

@register_scriptlet
class DataProcessor(BaseScriptlet):
    def run(self, input_data=None):
        # Process data with context access
        config = self.context.get("processing.config", {})
        result = self.process_data(input_data, config)
        
        # Store results
        self.context.set("processing.result", result, who=self.name)
        return {"status": "success", "processed": len(result)}
```

### 3. Analysis Framework
```python
from src.analysis import EnhancedSummarizer, AnalysisConfig

# Configure analysis
config = AnalysisConfig(statistical_precision=4, debug_mode=True)

# Run analysis
summarizer = EnhancedSummarizer(config)
result = summarizer.analyze([1, 2, 3, 4, 5])
```

## Testing
```bash
pytest --disable-warnings -q
```

## Development Tools
```bash
# Format code
python -m black .

# Run compliance check
python tools/lint_checker.py

# Update documentation
python tools/documentation_updater.py
```
'''
        
        # Create examples/basic_usage.py
        basic_usage_content = '''#!/usr/bin/env python3
"""
Basic Usage Example - IAF0 Framework Integration
================================================
Demonstrates how to use Context, Scriptlet, and Analysis frameworks together.
"""

from orchestrator.context import Context
from scriptlets.framework import BaseScriptlet, register_scriptlet
from src.analysis.framework import BaseAnalyzerV2, AnalysisConfig


@register_scriptlet
class DataProcessor(BaseScriptlet):
    """Example scriptlet for data processing."""
    
    def run(self, input_data=None):
        """Process input data and store results in context."""
        # Get configuration from context
        config = self.context.get("processing.config", {"multiplier": 2})
        
        # Process data
        if input_data:
            result = [x * config.get("multiplier", 2) for x in input_data]
        else:
            result = []
        
        # Store results in context
        self.context.set("processing.result", result, who=self.name)
        self.context.set("processing.count", len(result), who=self.name)
        
        return {"status": "success", "processed": len(result), "result": result}


class CustomAnalyzer(BaseAnalyzerV2):
    """Example analyzer for statistical analysis."""
    
    def analyze(self, data, **kwargs):
        """Analyze data and return comprehensive results."""
        if not data:
            return self._create_result({"error": "No data provided"})
        
        # Perform statistical analysis
        stats = {
            "count": len(data),
            "sum": sum(data),
            "mean": sum(data) / len(data),
            "min": min(data),
            "max": max(data)
        }
        
        # Generate insights
        insights = []
        if stats["mean"] > 10:
            insights.append("Data has high average value")
        if stats["max"] - stats["min"] > 20:
            insights.append("Data has wide range")
        
        return self._create_result({
            "statistics": stats,
            "insights": insights,
            "data_quality": "good" if len(data) > 5 else "limited"
        })


def main():
    """Demonstrate integrated usage of IAF0 frameworks."""
    print("🚀 IAF0 Framework Integration Example")
    
    # 1. Initialize Context
    context = Context()
    context.set("processing.config", {"multiplier": 3}, who="main")
    print("✅ Context initialized")
    
    # 2. Use Scriptlet with Context
    processor = DataProcessor(context=context)
    input_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    result = processor.run(input_data)
    print(f"✅ Scriptlet processed: {result}")
    
    # 3. Get processed data from Context
    processed_data = context.get("processing.result")
    print(f"✅ Retrieved from context: {processed_data}")
    
    # 4. Analyze with Analysis Framework
    config = AnalysisConfig(statistical_precision=2, debug_mode=True)
    analyzer = CustomAnalyzer(config)
    
    analysis_result = analyzer.analyze(processed_data)
    print(f"✅ Analysis complete: {analysis_result.summary}")
    
    # 5. Store analysis in Context
    context.set("analysis.result", analysis_result.data, who="analyzer")
    context.set("analysis.insights", analysis_result.data.get("insights", []), who="analyzer")
    
    # 6. Show Context history
    print("\\n📊 Context Change History:")
    history = context.get_history()
    for change in history[-5:]:  # Show last 5 changes
        print(f"  {change.who} set {change.key}: {change.after}")
    
    print("\\n🎉 Integration example completed successfully!")


if __name__ == "__main__":
    main()
'''
        
        docs = [
            ("docs/getting_started.md", getting_started_content),
            ("examples/basic_usage.py", basic_usage_content),
        ]
        
        created_count = 0  # Counter for created documentation files
        
        for filepath, content in docs:
            doc_path = self.workspace_path / filepath
            doc_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories
            doc_path.write_text(content)  # Write documentation file
            created_count += 1
            print(f"  📚 Created: {filepath}")
        
        print(f"  ✅ Documentation generated: {created_count} files created")

    def _verify_baseline_integrity(self) -> Dict[str, any]:
        """Verify the integrity of the fresh baseline."""
        integrity_results = {
            "essential_files": {"status": "checking", "files": [], "missing": []},
            "directory_structure": {"status": "checking", "dirs": [], "missing": []},
            "import_integrity": {"status": "checking", "imports": [], "errors": []},
            "overall_status": "checking"
        }
        
        # Check essential files
        essential_files = [
            "orchestrator/context/context.py",
            "scriptlets/framework.py",
            "src/analysis/framework.py",
            "src/analysis/components.py",
            "src/analysis/registry.py",
            "src/core/logger.py",
            "tests/test_analysis_framework.py",
            "tests/test_scriptlet_framework.py",
        ]
        
        for file_path in essential_files:
            full_path = self.workspace_path / file_path
            if full_path.exists():
                integrity_results["essential_files"]["files"].append(file_path)
                print(f"  ✅ File exists: {file_path}")
            else:
                integrity_results["essential_files"]["missing"].append(file_path)
                print(f"  ❌ File missing: {file_path}")
        
        integrity_results["essential_files"]["status"] = "complete"
        
        # Check directory structure
        required_dirs = [
            "src", "src/core", "src/analysis",
            "orchestrator", "orchestrator/context",
            "scriptlets", "tests", "tools", "docs", "examples"
        ]
        
        for dir_path in required_dirs:
            full_path = self.workspace_path / dir_path
            if full_path.exists() and full_path.is_dir():
                integrity_results["directory_structure"]["dirs"].append(dir_path)
                print(f"  ✅ Directory exists: {dir_path}")
            else:
                integrity_results["directory_structure"]["missing"].append(dir_path)
                print(f"  ❌ Directory missing: {dir_path}")
        
        integrity_results["directory_structure"]["status"] = "complete"
        
        # Determine overall status
        has_missing_files = len(integrity_results["essential_files"]["missing"]) > 0
        has_missing_dirs = len(integrity_results["directory_structure"]["missing"]) > 0
        
        if not has_missing_files and not has_missing_dirs:
            integrity_results["overall_status"] = "passed"
            print(f"  ✅ Baseline integrity: PASSED")
        else:
            integrity_results["overall_status"] = "failed"
            print(f"  ❌ Baseline integrity: FAILED")
        
        return integrity_results

    def _generate_cleanup_report(self, integrity_results: Dict) -> Dict[str, any]:
        """Generate comprehensive cleanup report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "workspace_path": str(self.workspace_path),
            "backup_location": str(self.backup_dir),
            "files_removed": len(self.cleaned_files),
            "files_preserved": len(self.preserved_files),
            "errors": len(self.errors),
            "integrity_check": integrity_results,
            "summary": {
                "status": "success" if integrity_results["overall_status"] == "passed" else "partial",
                "removed_files": self.cleaned_files[:10],  # First 10 for brevity
                "preserved_files": self.preserved_files,
                "error_messages": self.errors
            }
        }
        
        # Save report to file
        report_path = self.workspace_path / "cleanup_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)  # Save formatted JSON report
        
        print(f"\n📊 Cleanup Report Summary:")
        print(f"  📁 Workspace: {self.workspace_path}")
        print(f"  🗑️  Files removed: {report['files_removed']}")
        print(f"  💾 Files preserved: {report['files_preserved']}")
        print(f"  ⚠️  Errors: {report['errors']}")
        print(f"  ✅ Integrity: {integrity_results['overall_status'].upper()}")
        print(f"  📋 Full report: {report_path}")
        
        return report


def main():
    """Main entry point for workspace cleaner."""
    if len(sys.argv) > 1:
        workspace_path = sys.argv[1]  # Use provided path
    else:
        workspace_path = os.getcwd()  # Use current directory
    
    print(f"🧹 IAF0 Workspace Cleaner")
    print(f"📁 Target workspace: {workspace_path}")
    
    cleaner = WorkspaceCleaner(workspace_path)
    result = cleaner.run_cleanup()
    
    if result.get("success", True):
        print("\n🎉 Workspace cleanup completed successfully!")
        print("✅ Fresh IAF0 baseline framework is ready for development")
    else:
        print(f"\n❌ Cleanup completed with issues: {result.get('error', 'Unknown error')}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())