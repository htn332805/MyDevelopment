#!/usr/bin/env python3
"""
CLI Demo: Tmux Session Manager with JSON Layout

This script demonstrates how to create tmux sessions from JSON layout files
using the TmuxSessionManagerV2 class.

Usage Examples:
    python tmux_cli_demo.py --help                          # Show help
    python tmux_cli_demo.py --list                         # List existing sessions
    python tmux_cli_demo.py --layout demo/layout1.json     # Create from layout file
    python tmux_cli_demo.py --layout demo/layout1.json --debug  # Debug mode
    python tmux_cli_demo.py --kill GESetup                 # Kill specific session
    python tmux_cli_demo.py --create-sample                # Create sample layout

Requirements:
    - tmux installed on system
    - Python virtual environment activated
    - Framework0 project structure
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Import tmux session manager
from tmux_predefined_layout import create_tmux_session_manager


def create_framework0_sample_layout(output_path: Path) -> None:
    """
    Create a Framework0-compatible sample layout file.

    Args:
        output_path: Path where to save the sample layout
    """
    sample_layout: Dict[str, Any] = {
        "session_name": "Framework0_Dev",
        "base_directory": "/home/tester/Projects/MyDevelopment",
        "windows": [
            {
                "name": "main",
                "layout": "even-horizontal",
                "panes": [
                    {
                        "command": "source .venv/bin/activate && echo 'Framework0 Environment Ready'",
                        "working_directory": "/home/tester/Projects/MyDevelopment",
                    },
                    {
                        "command": "htop",
                        "split_direction": "horizontal",
                        "size_percentage": 40,
                    },
                ],
            },
            {
                "name": "logs",
                "layout": "even-vertical",
                "panes": [
                    {
                        "command": "mkdir -p logs && tail -f logs/app.log || echo 'Creating logs...' && touch logs/app.log && tail -f logs/app.log",
                        "working_directory": "/home/tester/Projects/MyDevelopment",
                    },
                    {
                        "command": "watch -n 5 'find . -name \"*.py\" | wc -l'",
                        "split_direction": "horizontal",
                    },
                ],
            },
            {
                "name": "development",
                "layout": "main-vertical",
                "panes": [
                    {
                        "command": 'source .venv/bin/activate && python -c \'import sys; print(f"Python {sys.version}"); print("Ready for development!")\'',
                        "working_directory": "/home/tester/Projects/MyDevelopment",
                    }
                ],
            },
        ],
    }

    # Create directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write layout file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sample_layout, f, indent=2)

    print(f"✅ Created sample layout: {output_path}")


def display_layout_info(layout_path: Path) -> None:
    """
    Display information about a layout file.

    Args:
        layout_path: Path to the layout JSON file
    """
    try:
        with open(layout_path, "r", encoding="utf-8") as f:
            layout_data = json.load(f)

        print(f"\n📋 Layout File Information: {layout_path}")
        print("-" * 60)
        print(f"  Session Name: {layout_data.get('session_name', 'Unknown')}")
        print(
            f"  Base Directory: {layout_data.get('base_directory', 'Current directory')}"
        )

        windows = layout_data.get("windows", [])
        print(f"  Windows: {len(windows)}")

        for i, window in enumerate(windows):
            panes = window.get("panes", [])
            layout = window.get("layout", "default")
            print(
                f"    {i+1}. '{window.get('name', 'Unnamed')}' - {layout} layout, {len(panes)} panes"
            )

            # Show first few pane commands
            for j, pane in enumerate(panes[:3]):  # Show first 3 panes
                cmd = pane.get("command", "No command")[:50]  # Truncate long commands
                if len(pane.get("command", "")) > 50:
                    cmd += "..."
                print(f"       Pane {j+1}: {cmd}")

            if len(panes) > 3:
                print(f"       ... and {len(panes) - 3} more panes")

    except Exception as e:
        print(f"❌ Error reading layout file: {e}")


def main():
    """Main CLI interface for tmux session management."""

    # Configure argument parser
    parser = argparse.ArgumentParser(
        description="Framework0 Tmux Session Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                                    # List active sessions
  %(prog)s --layout demo/layout1.json               # Create from existing layout
  %(prog)s --layout my_layout.json --debug          # Create with debug logging
  %(prog)s --kill MySession                         # Kill specific session
  %(prog)s --create-sample --output my_layout.json  # Create sample layout
  %(prog)s --info demo/layout1.json                 # Show layout information
        """,
    )

    # Add command line arguments
    parser.add_argument(
        "--layout", "-l", type=str, help="Path to JSON layout file for session creation"
    )

    parser.add_argument(
        "--list", action="store_true", help="List all existing tmux sessions"
    )

    parser.add_argument(
        "--kill", "-k", type=str, help="Kill specified tmux session by name"
    )

    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug logging for detailed traces",
    )

    parser.add_argument(
        "--detach",
        action="store_true",
        default=True,
        help="Create session in detached mode (default: True)",
    )

    parser.add_argument(
        "--attach",
        "-a",
        action="store_true",
        help="Attach to session after creation (overrides --detach)",
    )

    parser.add_argument(
        "--create-sample",
        action="store_true",
        help="Create a sample Framework0 layout file",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="framework0_sample.json",
        help="Output path for sample layout file (default: framework0_sample.json)",
    )

    parser.add_argument(
        "--info",
        "-i",
        type=str,
        help="Show information about a layout file without creating session",
    )

    args = parser.parse_args()

    # Display header
    print("\n" + "=" * 70)
    print("🖥️  Framework0 Tmux Session Manager CLI")
    print("   JSON Layout-Based Session Management")
    print("=" * 70)

    try:
        # Handle sample creation
        if args.create_sample:
            output_path = Path(args.output)
            create_framework0_sample_layout(output_path)
            return

        # Handle layout info display
        if args.info:
            layout_path = Path(args.info)
            if not layout_path.exists():
                print(f"❌ Layout file not found: {layout_path}")
                return
            display_layout_info(layout_path)
            return

        # Create tmux session manager
        print(f"\n🔧 Initializing Tmux Session Manager")
        print(f"   Debug Mode: {'Enabled' if args.debug else 'Disabled'}")

        tmux_manager = create_tmux_session_manager(debug=args.debug)
        print("✅ Tmux Session Manager ready")

        # Handle session listing
        if args.list:
            print(f"\n📋 Current Tmux Sessions")
            print("-" * 40)

            sessions = tmux_manager.list_sessions()
            if sessions:
                for session in sessions:
                    status = "📍 Attached" if session["attached"] else "💤 Detached"
                    print(
                        f"  • {session['name']} - {session['windows']} windows - {status}"
                    )
            else:
                print("  No tmux sessions found")
            return

        # Handle session killing
        if args.kill:
            print(f"\n🗑️  Killing Session: {args.kill}")
            print("-" * 40)

            result = tmux_manager.kill_session(args.kill)
            if result:
                print(f"✅ Successfully killed session: {args.kill}")
            else:
                print(f"❌ Failed to kill session: {args.kill} (may not exist)")
            return

        # Handle layout-based session creation
        if args.layout:
            layout_path = Path(args.layout)

            if not layout_path.exists():
                print(f"❌ Layout file not found: {layout_path}")
                return

            print(f"\n🚀 Creating Session from Layout")
            print("-" * 40)
            print(f"  Layout File: {layout_path}")

            # Show layout info first
            display_layout_info(layout_path)

            # Determine detach mode
            detach_mode = not args.attach if args.attach else args.detach

            print(f"\n  Creating session (detached: {detach_mode})...")

            # Create session from layout
            success = tmux_manager.create_session_from_layout(
                layout_path=layout_path, detach=detach_mode
            )

            if success:
                print("✅ Session created successfully!")

                # Load session info to get name
                with open(layout_path, "r") as f:
                    layout_data = json.load(f)
                session_name = layout_data.get("session_name", "Unknown")

                print(f"\n📡 Connection Commands:")
                print(f"  tmux attach-session -t {session_name}   # Attach to session")
                print(f"  tmux list-sessions                      # List all sessions")
                print(f"  tmux kill-session -t {session_name}     # Kill this session")

            else:
                print("❌ Failed to create session")
                print("   Session may already exist or tmux commands failed")

            return

        # No specific action - show help
        parser.print_help()

    except KeyboardInterrupt:
        print(f"\n⚠️  Operation cancelled by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Check virtual environment
    if not os.environ.get("VIRTUAL_ENV"):
        print("⚠️  Warning: No Python virtual environment detected")
        print("   Recommended: source .venv/bin/activate")
        print()

    main()
