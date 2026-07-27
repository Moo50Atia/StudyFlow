"""
KOS Security Permission Engine (RBAC/ABAC)
==========================================
Executes Role-Based and Attribute-Based Access Control checks.
"""

from typing import List, Set, Dict, Any


class PermissionEngine:
    """Manages role-permission mappings and evaluates action authorization."""

    def __init__(self):
        self._role_permissions: Dict[str, Set[str]] = {
            "admin": {"read", "write", "delete", "publish", "admin"},
            "professor": {"read", "write", "publish", "edit_assets"},
            "student": {"read", "query_kie", "view_materials"},
        }

    def has_permission(self, role: str, required_permission: str) -> bool:
        permissions = self._role_permissions.get(role.lower(), set())
        return required_permission in permissions or "admin" in permissions

    def authorize(self, role: str, required_permission: str) -> None:
        if not self.has_permission(role, required_permission):
            raise PermissionError(f"Role '{role}' lacks required permission '{required_permission}'.")
