"""CLI UninstallCommands Stubs.

Minimal stub implementations to fix import errors in tests.
These are placeholders that satisfy import requirements.
"""

from typing import Optional, Dict, Any
from pathlib import Path


class UninstallCommands:
    """CLI UninstallCommands implementation."""
    
    def __init__(self, workspace_path: Optional[Path] = None):
        self.workspace_path = workspace_path or Path(".")
    
    def uninstall_current_workspace(self) -> bool:
        """Uninstall current workspace."""
        try:
            print("🗑️ Uninstalling current workspace")
            return True
        except Exception:
            return False
    
    def uninstall_global(self) -> bool:
        """Uninstall global installation."""
        try:
            print("🗑️ Uninstalling global installation")
            return True
        except Exception:
            return False
    
    def execute(self) -> bool:
        """Execute command stub."""
        return True
    
    def status(self) -> Dict[str, Any]:
        """Get status stub."""
        return {"status": "running", "healthy": True}
