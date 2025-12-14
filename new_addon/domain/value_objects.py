"""
Domain Layer - Value Objects

Immutable value objects representing domain concepts.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthToken:
    """Authentication token value object"""
    access_token: str
    refresh_token: str
    expires_in: int  # seconds
    token_type: str = "Bearer"
    
    def is_valid(self) -> bool:
        """Check if token is present"""
        return bool(self.access_token and self.refresh_token)


@dataclass(frozen=True)
class DeviceCode:
    """OAuth device code value object"""
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int = 5


@dataclass(frozen=True)
class Pagination:
    """Pagination information"""
    current_page: int
    total_pages: int
    items_per_page: int
    total_items: int
    
    @property
    def has_next(self) -> bool:
        return self.current_page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        return self.current_page > 1


@dataclass(frozen=True)
class RouteParams:
    """Route parameters value object"""
    path: str
    query_params: dict
    
    def get(self, key: str, default=None):
        """Get query parameter"""
        return self.query_params.get(key, default)
