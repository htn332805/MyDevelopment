#!/usr/bin/env python3
"""
Framework0 Workspace Management Script
=====================================
Convenient wrapper for Framework0 workspace cleaning and baseline management.

This script provides easy access to Framework0 workspace cleaning functions
that preserve the baseline structure while enabling clean development cycles.

Usage Examples:
    # Clean development artifacts (keeps Framework0 baseline)
    python tools/framework0_manager.py clean

    # Reset workspace to fresh development state
    python tools/framework0_manager.py reset

    # Create backup before major changes
    python tools/framework0_manager.py backup

    # Test what would be cleaned (dry run)
    python tools/framework0_manager.py clean --dry-run

Author: Framework0 Team
Version: 1.0.0
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Main entry point - delegates to Framework0 workspace cleaner."""

    # Import the actual cleaner
    try:
        from tools.framework0_workspace_cleaner import main as cleaner_main

        # Show helpful message
        print("🚀 Framework0 Workspace Manager")
        print("=" * 35)
        print("Managing workspace with Framework0 baseline preservation...")
        print()

        # Delegate to the main cleaner
        cleaner_main()

    except ImportError as e:
        print(f"❌ Error: Cannot import Framework0 workspace cleaner: {e}")
        print("\nEnsure you're running from the Framework0 workspace root directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
