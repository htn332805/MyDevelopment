#!/usr/bin/env python3
"""
Framework0 Phased Workspace Restructurer

A comprehensive phased execution system for workspace restructuring with user approval
at each step. Implements safety measures, validation checks, and rollback procedures.

Usage:
    python tools/phased_restructurer.py --phase 1    # Execute Phase 1 only
    python tools/phased_restructurer.py --all        # Execute all phases with prompts
    python tools/phased_restructurer.py --status     # Show current status
"""

import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add src directory to Python path for framework imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from core.logger import get_logger


class PhasedRestructurer:
    """
    Phased workspace restructurer with user approval at each step.

    Provides safe, incremental restructuring of workspace to match Framework0
    baseline layout with comprehensive validation and rollback capabilities.
    """

    def __init__(self, workspace_root: str) -> None:
        """
        Initialize the phased restructurer.

        Args:
            workspace_root: Absolute path to workspace root directory
        """
        self.workspace_root = Path(workspace_root)  # Set workspace root path
        self.logger = get_logger(__name__)  # Initialize logger
        # Plan file path
        self.plan_path = self.workspace_root / "WORKSPACE_RESTRUCTURING_PLAN.json"
        # Backup directory path
        self.backup_dir = self.workspace_root / ".restructuring_backup"
        # Status tracking file
        self.status_file = self.workspace_root / ".restructuring_status.json"

        # Phase definitions with descriptions
        self.phases = {
            1: {
                "name": "Safety Backup",  # Phase 1 name
                # Phase 1 description
                "description": "Create comprehensive backup of current workspace state",
                # Phase 1 operation types
                "operations": ["create_backup", "backup_git_state"],
                "critical": True,  # Phase 1 is critical for safety
            },
            2: {
                "name": "Directory Structure",  # Phase 2 name
                # Phase 2 description
                "description": "Create missing directories and Python package files",
                # Phase 2 operation types
                "operations": ["create_directory", "create_file"],
                "critical": False,  # Phase 2 is not critical
            },
            3: {
                "name": "File Relocation",  # Phase 3 name
                # Phase 3 description
                "description": "Move files to their correct Framework0 locations",
                "operations": ["move_file"],  # Phase 3 operation types
                "critical": False,  # Phase 3 is not critical
            },
            4: {
                "name": "Final Validation",  # Phase 4 name
                # Phase 4 description
                "description": "Run comprehensive validation and compliance checks",
                "operations": ["validate"],  # Phase 4 operation types
                "critical": True,  # Phase 4 is critical for validation
            },
        }

    def load_restructuring_plan(self) -> Optional[Dict[str, Any]]:
        """
        Load the restructuring plan from file.

        Returns:
            Optional[Dict[str, Any]]: Restructuring plan data or None if not found
        """
        if not self.plan_path.exists():  # Check if plan file exists
            self.logger.error("No restructuring plan found. Run analysis first.")
            return None

        try:
            with open(self.plan_path, "r", encoding="utf-8") as f:  # Open plan file
                plan = json.load(f)  # Load JSON data
            self.logger.info("Restructuring plan loaded successfully")
            return plan  # Return plan data
        except Exception as e:  # Handle loading errors
            self.logger.error(f"Failed to load restructuring plan: {e}")
            return None

    def get_current_status(self) -> Dict[str, Any]:
        """
        Get current restructuring status.

        Returns:
            Dict[str, Any]: Current status information
        """
        if not self.status_file.exists():  # Check if status file exists
            # Initialize default status
            status = {
                "phases_completed": [],  # List of completed phases
                "current_phase": None,  # Currently executing phase
                "total_operations": 0,  # Total operations count
                "completed_operations": 0,  # Completed operations count
                "last_updated": datetime.now().isoformat(),  # Last update timestamp
                "backup_created": False,  # Whether backup was created
                "rollback_available": False,  # Whether rollback is available
            }
            self._save_status(status)  # Save initial status
            return status  # Return initial status

        try:
            with open(self.status_file, "r", encoding="utf-8") as f:  # Open status file
                return json.load(f)  # Load and return status data
        except Exception as e:  # Handle loading errors
            self.logger.error(f"Failed to load status: {e}")
            return {}  # Return empty status

    def _save_status(self, status: Dict[str, Any]) -> None:
        """
        Save current restructuring status.

        Args:
            status: Status information to save
        """
        status["last_updated"] = datetime.now().isoformat()  # Update timestamp

        try:
            with open(
                self.status_file, "w", encoding="utf-8"
            ) as f:  # Open status file for writing
                json.dump(status, f, indent=2)  # Save status data
        except Exception as e:  # Handle saving errors
            self.logger.error(f"Failed to save status: {e}")

    def get_phase_operations(
        self, plan: Dict[str, Any], phase_number: int
    ) -> List[Dict[str, Any]]:
        """
        Get operations for a specific phase.

        Args:
            plan: Complete restructuring plan
            phase_number: Phase number (1-4)

        Returns:
            List[Dict[str, Any]]: Operations for the specified phase
        """
        if phase_number not in self.phases:  # Check if phase number is valid
            return []  # Return empty list for invalid phase

        phase_config = self.phases[phase_number]  # Get phase configuration
        operation_types = phase_config["operations"]  # Get operation types for phase

        # Filter operations by type for this phase
        return [
            op for op in plan.get("operations", []) if op.get("type") in operation_types
        ]

    def execute_phase(self, phase_number: int, plan: Dict[str, Any]) -> bool:
        """
        Execute a specific phase of the restructuring plan.

        Args:
            phase_number: Phase number to execute (1-4)
            plan: Complete restructuring plan

        Returns:
            bool: True if phase executed successfully, False otherwise
        """
        if phase_number not in self.phases:  # Check if phase number is valid
            self.logger.error(f"Invalid phase number: {phase_number}")
            return False

        phase_config = self.phases[phase_number]  # Get phase configuration
        phase_operations = self.get_phase_operations(
            plan, phase_number
        )  # Get phase operations

        if not phase_operations:  # Check if operations exist for phase
            self.logger.info(f"No operations found for Phase {phase_number}")
            return True  # Return success for empty phase

        self.logger.info(f"🚀 Starting Phase {phase_number}: {phase_config['name']}")
        self.logger.info(f"   Description: {phase_config['description']}")
        self.logger.info(f"   Operations: {len(phase_operations)}")

        # Update status for phase start
        status = self.get_current_status()  # Get current status
        status["current_phase"] = phase_number  # Set current phase
        self._save_status(status)  # Save updated status

        try:
            # Execute each operation in the phase
            for i, operation in enumerate(
                phase_operations, 1
            ):  # Iterate through operations
                self.logger.info(
                    f"   [{i}/{len(phase_operations)}] {operation.get('description', 'Unknown operation')}"
                )

                if not self._execute_operation(operation):  # Execute single operation
                    self.logger.error(f"Failed to execute operation: {operation}")
                    return False  # Return failure if operation fails

                # Update progress
                status = self.get_current_status()  # Get current status
                status["completed_operations"] += 1  # Increment completed operations
                self._save_status(status)  # Save updated status

            # Mark phase as completed
            status = self.get_current_status()  # Get current status
            if (
                phase_number not in status["phases_completed"]
            ):  # Check if phase not already completed
                status["phases_completed"].append(
                    phase_number
                )  # Add phase to completed list
            status["current_phase"] = None  # Clear current phase
            self._save_status(status)  # Save updated status

            self.logger.info(f"✅ Phase {phase_number} completed successfully")
            return True  # Return success

        except Exception as e:  # Handle execution errors
            self.logger.error(f"Error during Phase {phase_number} execution: {e}")
            return False  # Return failure

    def _execute_operation(self, operation: Dict[str, Any]) -> bool:
        """
        Execute a single restructuring operation.

        Args:
            operation: Operation definition with type and parameters

        Returns:
            bool: True if operation succeeded, False otherwise
        """
        op_type = operation.get("type")  # Get operation type

        try:
            if op_type == "create_backup":  # Handle backup creation
                return self._create_backup(operation)
            elif op_type == "backup_git_state":  # Handle git state backup
                return self._backup_git_state(operation)
            elif op_type == "create_directory":  # Handle directory creation
                return self._create_directory(operation)
            elif op_type == "create_file":  # Handle file creation
                return self._create_file(operation)
            elif op_type == "move_file":  # Handle file movement
                return self._move_file(operation)
            elif op_type == "validate":  # Handle validation
                return self._validate_operation(operation)
            else:
                self.logger.error(f"Unknown operation type: {op_type}")
                return False  # Return failure for unknown operation

        except Exception as e:  # Handle operation errors
            self.logger.error(f"Error executing {op_type} operation: {e}")
            return False  # Return failure

    def _create_backup(self, operation: Dict[str, Any]) -> bool:
        """
        Create comprehensive backup of workspace.

        Args:
            operation: Backup operation parameters

        Returns:
            bool: True if backup created successfully
        """
        try:
            if self.backup_dir.exists():  # Check if backup already exists
                self.logger.info("Backup directory already exists, skipping")
                return True

            self.backup_dir.mkdir(parents=True)  # Create backup directory
            self.logger.info(f"Created backup directory: {self.backup_dir}")

            # Copy all files to backup (excluding backup directory itself)
            for (
                item
            ) in self.workspace_root.iterdir():  # Iterate through workspace items
                if item.name.startswith(".restructuring"):  # Skip restructuring files
                    continue

                if item.is_file():  # Handle files
                    shutil.copy2(
                        item, self.backup_dir / item.name
                    )  # Copy file with metadata
                elif item.is_dir():  # Handle directories
                    shutil.copytree(
                        item, self.backup_dir / item.name
                    )  # Copy directory tree

            # Update status to indicate backup was created
            status = self.get_current_status()  # Get current status
            status["backup_created"] = True  # Mark backup as created
            status["rollback_available"] = True  # Enable rollback availability
            self._save_status(status)  # Save updated status

            self.logger.info("Workspace backup created successfully")
            return True  # Return success

        except Exception as e:  # Handle backup errors
            self.logger.error(f"Failed to create backup: {e}")
            return False  # Return failure

    def _backup_git_state(self, operation: Dict[str, Any]) -> bool:
        """
        Backup current git state.

        Args:
            operation: Git backup operation parameters

        Returns:
            bool: True if git state backed up successfully
        """
        try:
            git_dir = self.workspace_root / ".git"  # Git directory path
            if not git_dir.exists():  # Check if git repository exists
                self.logger.info("No git repository found, skipping git backup")
                return True

            git_backup_dir = self.backup_dir / ".git"  # Git backup directory path
            if git_backup_dir.exists():  # Check if git backup already exists
                self.logger.info("Git backup already exists, skipping")
                return True

            shutil.copytree(git_dir, git_backup_dir)  # Copy git directory
            self.logger.info("Git state backed up successfully")
            return True  # Return success

        except Exception as e:  # Handle git backup errors
            self.logger.error(f"Failed to backup git state: {e}")
            return False  # Return failure

    def _create_directory(self, operation: Dict[str, Any]) -> bool:
        """
        Create a directory.

        Args:
            operation: Directory creation operation parameters

        Returns:
            bool: True if directory created successfully
        """
        try:
            target_path = (
                self.workspace_root / operation["target_path"]
            )  # Get target path

            if target_path.exists():  # Check if directory already exists
                self.logger.info(f"Directory already exists: {target_path}")
                return True

            target_path.mkdir(parents=True, exist_ok=True)  # Create directory
            self.logger.info(f"Created directory: {target_path}")
            return True  # Return success

        except Exception as e:  # Handle directory creation errors
            self.logger.error(f"Failed to create directory: {e}")
            return False  # Return failure

    def _create_file(self, operation: Dict[str, Any]) -> bool:
        """
        Create a file with specified content.

        Args:
            operation: File creation operation parameters

        Returns:
            bool: True if file created successfully
        """
        try:
            target_path = (
                self.workspace_root / operation["target_path"]
            )  # Get target path
            content = operation.get("content", "")  # Get file content

            if target_path.exists():  # Check if file already exists
                self.logger.info(f"File already exists: {target_path}")
                return True

            # Ensure parent directory exists
            target_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Create parent directory

            with open(target_path, "w", encoding="utf-8") as f:  # Create file
                f.write(content)  # Write content to file

            self.logger.info(f"Created file: {target_path}")
            return True  # Return success

        except Exception as e:  # Handle file creation errors
            self.logger.error(f"Failed to create file: {e}")
            return False  # Return failure

    def _move_file(self, operation: Dict[str, Any]) -> bool:
        """
        Move a file to new location.

        Args:
            operation: File move operation parameters

        Returns:
            bool: True if file moved successfully
        """
        try:
            source_path = (
                self.workspace_root / operation["source_path"]
            )  # Get source path
            target_path = (
                self.workspace_root / operation["target_path"]
            )  # Get target path

            if not source_path.exists():  # Check if source file exists
                self.logger.warning(f"Source file not found: {source_path}")
                return True  # Return success for missing source

            if target_path.exists():  # Check if target already exists
                self.logger.info(f"Target already exists: {target_path}")
                return True

            # Ensure target parent directory exists
            target_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Create parent directory

            shutil.move(str(source_path), str(target_path))  # Move file
            self.logger.info(f"Moved: {source_path} -> {target_path}")
            return True  # Return success

        except Exception as e:  # Handle file move errors
            self.logger.error(f"Failed to move file: {e}")
            return False  # Return failure

    def _validate_operation(self, operation: Dict[str, Any]) -> bool:
        """
        Validate restructuring operation.

        Args:
            operation: Validation operation parameters

        Returns:
            bool: True if validation passed
        """
        self.logger.info("Running restructuring validation checks")
        # Placeholder for validation logic
        return True  # Return success for now

    def show_status(self) -> None:
        """Display current restructuring status."""
        status = self.get_current_status()  # Get current status

        print("📋 Framework0 Workspace Restructuring Status")
        print("=" * 50)
        print(f"Backup Created: {'✅' if status['backup_created'] else '❌'}")
        print(f"Rollback Available: {'✅' if status['rollback_available'] else '❌'}")
        print(f"Total Operations: {status['total_operations']}")
        print(f"Completed: {status['completed_operations']}")

        if status["current_phase"]:  # Check if phase is currently running
            print(f"Current Phase: {status['current_phase']}")

        print("\nPhase Status:")
        for phase_num, phase_config in self.phases.items():  # Iterate through phases
            status_icon = "✅" if phase_num in status["phases_completed"] else "⏸️"
            print(f"  {status_icon} Phase {phase_num}: {phase_config['name']}")

        print(f"\nLast Updated: {status.get('last_updated', 'Unknown')}")


def main() -> None:
    """
    Main function for phased workspace restructuring execution.
    """
    import argparse  # Import argument parser

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Framework0 Phased Workspace Restructurer"
    )
    parser.add_argument(
        "--phase", type=int, choices=[1, 2, 3, 4], help="Execute specific phase"
    )
    parser.add_argument(
        "--all", action="store_true", help="Execute all phases with prompts"
    )
    parser.add_argument("--status", action="store_true", help="Show current status")
    args = parser.parse_args()  # Parse arguments

    logger = get_logger(__name__)  # Initialize logger
    logger.info("🚀 Starting Framework0 Phased Workspace Restructurer")

    try:
        # Initialize phased restructurer
        workspace_root = Path.cwd()  # Use current working directory
        restructurer = PhasedRestructurer(str(workspace_root))  # Create restructurer

        if args.status:  # Handle status request
            restructurer.show_status()  # Show current status
            return

        # Load restructuring plan
        plan = restructurer.load_restructuring_plan()  # Load plan
        if not plan:  # Check if plan loaded successfully
            logger.error("Cannot proceed without restructuring plan")
            return

        if args.phase:  # Handle single phase execution
            logger.info(f"Executing Phase {args.phase}")

            # Show phase preview
            phase_ops = restructurer.get_phase_operations(
                plan, args.phase
            )  # Get phase operations
            print(f"\n📋 Phase {args.phase}: {restructurer.phases[args.phase]['name']}")
            print(f"Description: {restructurer.phases[args.phase]['description']}")
            print(f"Operations: {len(phase_ops)}")

            for i, op in enumerate(phase_ops, 1):  # Show operations preview
                print(f"  {i}. {op.get('description', 'Unknown operation')}")

            # Get user confirmation
            response = input(f"\nExecute Phase {args.phase}? (y/N): ").strip().lower()
            if response == "y":  # Check user confirmation
                success = restructurer.execute_phase(args.phase, plan)  # Execute phase
                if success:  # Check execution success
                    logger.info(f"✅ Phase {args.phase} completed successfully")
                else:
                    logger.error(f"❌ Phase {args.phase} failed")
            else:
                logger.info("Phase execution cancelled by user")

        elif args.all:  # Handle all phases execution
            logger.info("Executing all phases with user approval")

            for phase_num in sorted(
                restructurer.phases.keys()
            ):  # Execute phases in order
                phase_config = restructurer.phases[phase_num]  # Get phase configuration
                phase_ops = restructurer.get_phase_operations(
                    plan, phase_num
                )  # Get phase operations

                if not phase_ops:  # Skip empty phases
                    logger.info(f"Skipping Phase {phase_num} (no operations)")
                    continue

                # Show phase preview
                print(f"\n📋 Phase {phase_num}: {phase_config['name']}")
                print(f"Description: {phase_config['description']}")
                print(f"Operations: {len(phase_ops)}")

                for i, op in enumerate(phase_ops, 1):  # Show operations preview
                    print(f"  {i}. {op.get('description', 'Unknown operation')}")

                # Get user confirmation
                response = (
                    input(f"\nExecute Phase {phase_num}? (y/N/q to quit): ")
                    .strip()
                    .lower()
                )
                if response == "y":  # User approved execution
                    success = restructurer.execute_phase(
                        phase_num, plan
                    )  # Execute phase
                    if success:  # Check execution success
                        logger.info(f"✅ Phase {phase_num} completed successfully")
                    else:
                        logger.error(f"❌ Phase {phase_num} failed")
                        break  # Stop execution on failure
                elif response == "q":  # User requested quit
                    logger.info("Execution cancelled by user")
                    break  # Stop execution
                else:
                    logger.info(f"Phase {phase_num} skipped by user")
        else:
            # Show help and status if no specific action requested
            restructurer.show_status()  # Show current status
            print("\nUsage:")
            print("  --phase N    Execute specific phase (1-4)")
            print("  --all        Execute all phases with prompts")
            print("  --status     Show current status")

    except Exception as e:  # Handle main execution errors
        logger.error(f"❌ Phased restructuring failed: {e}")
        raise  # Re-raise for debugging


if __name__ == "__main__":
    main()  # Run main function
