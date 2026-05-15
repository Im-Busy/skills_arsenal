#!/usr/bin/env python3
"""
Toggle autonomous Jupyter execution mode on/off.

Usage:
    uv run scripts/toggle_autonomous.py --enable
    uv run scripts/toggle_autonomous.py --disable
    uv run scripts/toggle_autonomous.py --status
"""

import argparse
import json
import sys
from pathlib import Path


def get_config_path():
    """Get config.json path from skill directory."""
    script_dir = Path(__file__).parent.parent
    config_path = script_dir / "config.json"
    return config_path


def load_config():
    """Load config.json."""
    config_path = get_config_path()
    if not config_path.exists():
        # Create default config
        default_config = {
            "enabled": False,
            "auto_execute_on_error": True,
            "max_retry_iterations": 5,
            "timeout_per_execution": 600,
            "allowed_notebook_patterns": ["**/*.ipynb"],
            "excluded_notebook_patterns": ["**/archive/*.ipynb", "**/temp/*.ipynb"],
            "auto_fix_patterns": {
                "ModuleNotFoundError": "install_package",
                "NameError": "check_definition",
                "SyntaxError": "fix_syntax",
                "FileNotFoundError": "check_path",
            },
            "reporting": {
                "log_all_executions": True,
                "save_error_reports": True,
                "output_directory": ".jupyter-execution-logs",
            },
            "safety": {
                "require_confirmation_for_package_install": True,
                "max_concurrent_executions": 1,
                "block_network_access": True,
            },
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        return default_config

    with open(config_path, "r") as f:
        return json.load(f)


def save_config(config):
    """Save config.json."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def enable():
    """Enable autonomous mode."""
    config = load_config()
    config["enabled"] = True
    save_config(config)
    print("✓ Autonomous execution ENABLED")
    print_status(config)


def disable():
    """Disable autonomous mode."""
    config = load_config()
    config["enabled"] = False
    save_config(config)
    print("✓ Autonomous execution DISABLED")
    print_status(config)


def print_status(config=None):
    """Print current status."""
    if config is None:
        config = load_config()

    mode = "ENABLED" if config.get("enabled", False) else "DISABLED"
    auto_fix = "ON" if config.get("auto_execute_on_error", True) else "OFF"
    max_retries = config.get("max_retry_iterations", 5)
    timeout = config.get("timeout_per_execution", 600)
    log_dir = config.get("reporting", {}).get("output_directory", ".jupyter-execution-logs")

    border = "═" * 58
    print(f"\n╔{border}╗")
    print(f"║  Jupyter Autonomous Execution - Status        ║")
    print(f"╠{border}╣")
    print(f"║  Mode:           {mode:30} ║")
    print(f"║  Auto-fix:       {auto_fix:30} ║")
    print(f"║  Max retries:    {max_retries:30} ║")
    print(f"║  Timeout:        {timeout}s{'':<27} ║")
    print(f"║  Log dir:        {log_dir[:30]:30} ║")
    print(f"╚{border}╝\n")


def is_enabled():
    """Check if autonomous mode is enabled."""
    config = load_config()
    return config.get("enabled", False)


def main():
    parser = argparse.ArgumentParser(description="Toggle autonomous Jupyter execution mode")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--enable", "-e", action="store_true", help="Enable autonomous mode")
    group.add_argument("--disable", "-d", action="store_true", help="Disable autonomous mode")
    group.add_argument("--status", "-s", action="store_true", help="Show current status")
    group.add_argument(
        "--check", "-c", action="store_true", help="Check if enabled (exit code 0 if enabled)"
    )

    args = parser.parse_args()

    if args.enable:
        enable()
    elif args.disable:
        disable()
    elif args.status:
        print_status()
    elif args.check:
        sys.exit(0 if is_enabled() else 1)


if __name__ == "__main__":
    main()
