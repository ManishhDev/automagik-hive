#!/usr/bin/env python3
"""
CLI utilities for Automagik Hive authentication management.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from lib.auth.init_service import AuthInitService


def show_current_key():
    """Display the current API key."""
    init_service = AuthInitService()
    key = init_service.get_current_key()
    
    if key:
        print(f"Current API Key: {key}")
        print(f"\nUsage example:")
        print(f'curl -H "x-api-key: {key}" http://localhost:9888/playground/status')
    else:
        print("No API key found. Run the server once to generate a key automatically.")


def regenerate_key():
    """Generate a new API key."""
    init_service = AuthInitService()
    new_key = init_service.regenerate_key()
    print(f"✅ New API key generated: {new_key}")
    

def show_auth_status():
    """Show authentication configuration status."""
    auth_disabled = os.getenv("HIVE_AUTH_DISABLED", "false").lower() == "true"
    
    print("🔐 Automagik Hive Authentication Status")
    print("=" * 40)
    print(f"Authentication: {'DISABLED' if auth_disabled else 'ENABLED'}")
    
    if auth_disabled:
        print("⚠️  Running in development mode - no authentication required")
    else:
        show_current_key()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Automagik Hive Authentication Management")
    parser.add_argument(
        "action", 
        choices=["show", "regenerate", "status"],
        help="Action to perform"
    )
    
    args = parser.parse_args()
    
    if args.action == "show":
        show_current_key()
    elif args.action == "regenerate":
        regenerate_key()
    elif args.action == "status":
        show_auth_status()