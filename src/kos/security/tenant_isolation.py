"""
KOS Security Tenant Isolation Engine
====================================
Enforces strict multi-tenant and material-level storage boundaries.
"""

from typing import Dict, Any, Optional


class TenantIsolationError(PermissionError):
    """Raised when a cross-tenant data access violation is detected."""
    pass


class TenantIsolationEngine:
    """Validates material and tenant context boundaries for all storage operations."""

    @staticmethod
    def validate_access(request_tenant_id: str, resource_tenant_id: str, resource_id: str) -> bool:
        if request_tenant_id != resource_tenant_id:
            raise TenantIsolationError(
                f"Security Violation: Tenant '{request_tenant_id}' attempted unauthorized access "
                f"to resource '{resource_id}' owned by tenant '{resource_tenant_id}'."
            )
        return True

    @staticmethod
    def resolve_storage_path(material_id: str, base_path: str = "Generating/Materials") -> str:
        """Resolves isolated file storage path per material."""
        # Sanitize material_id to prevent directory traversal
        sanitized_id = os.path.basename(material_id)
        return f"{base_path}/{sanitized_id}"


import os
