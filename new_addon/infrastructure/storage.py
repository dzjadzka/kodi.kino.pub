"""
Infrastructure Layer - Storage

Settings and cache storage interfaces and implementations.
"""

from typing import Any, Optional
from abc import ABC, abstractmethod


class ISettings(ABC):
    """Settings storage interface"""
    
    @abstractmethod
    def get_string(self, key: str, default: str = "") -> str:
        """Get string setting"""
        pass
    
    @abstractmethod
    def set_string(self, key: str, value: str) -> None:
        """Set string setting"""
        pass
    
    @abstractmethod
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer setting"""
        pass
    
    @abstractmethod
    def set_int(self, key: str, value: int) -> None:
        """Set integer setting"""
        pass
    
    @abstractmethod
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean setting"""
        pass
    
    @abstractmethod
    def set_bool(self, key: str, value: bool) -> None:
        """Set boolean setting"""
        pass


class ICache(ABC):
    """Cache storage interface"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached value with optional TTL in seconds"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete cached value"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all cache"""
        pass


class ISearchHistory(ABC):
    """Search history storage interface"""
    
    @abstractmethod
    def add(self, query: str) -> None:
        """Add search query to history"""
        pass
    
    @abstractmethod
    def get_recent(self, limit: int = 10) -> list[str]:
        """Get recent search queries"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear search history"""
        pass


class KodiSettings(ISettings):
    """
    Kodi addon settings implementation.
    
    Uses xbmcaddon.Addon().getSetting() / setSetting()
    """
    
    def __init__(self, addon_id: str = "plugin.video.kino.pub"):
        self.addon_id = addon_id
        # TODO: Initialize xbmcaddon.Addon
    
    def get_string(self, key: str, default: str = "") -> str:
        """Get string setting"""
        # TODO: Implement with xbmcaddon
        raise NotImplementedError("Stub: get_string not implemented")
    
    def set_string(self, key: str, value: str) -> None:
        """Set string setting"""
        # TODO: Implement with xbmcaddon
        raise NotImplementedError("Stub: set_string not implemented")
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer setting"""
        # TODO: Implement with xbmcaddon
        raise NotImplementedError("Stub: get_int not implemented")
    
    def set_int(self, key: str, value: int) -> None:
        """Set integer setting"""
        # TODO: Implement with xbmcaddon
        raise NotImplementedError("Stub: set_int not implemented")
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean setting"""
        # TODO: Implement with xbmcaddon
        raise NotImplementedError("Stub: get_bool not implemented")
    
    def set_bool(self, key: str, value: bool) -> None:
        """Set boolean setting"""
        # TODO: Implement with xbmcaddon
        raise NotImplementedError("Stub: set_bool not implemented")


class WindowPropertyCache(ICache):
    """
    Cache using Kodi window properties.
    
    Uses xbmcgui.Window().setProperty() / getProperty()
    with pickle serialization for complex objects.
    """
    
    def __init__(self, window_id: int = 10000):
        self.window_id = window_id
        # TODO: Initialize xbmcgui.Window
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        # TODO: Implement with window properties + pickle
        raise NotImplementedError("Stub: get not implemented")
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached value"""
        # TODO: Implement with window properties + pickle
        raise NotImplementedError("Stub: set not implemented")
    
    def delete(self, key: str) -> None:
        """Delete cached value"""
        # TODO: Implement
        raise NotImplementedError("Stub: delete not implemented")
    
    def clear(self) -> None:
        """Clear all cache"""
        # TODO: Implement
        raise NotImplementedError("Stub: clear not implemented")


class SearchHistoryStorage(ISearchHistory):
    """
    Search history using window properties.
    
    Stores list of recent search queries.
    """
    
    HISTORY_KEY = "search_history"
    
    def __init__(self, cache: ICache):
        self.cache = cache
    
    def add(self, query: str) -> None:
        """Add search query to history"""
        # TODO: Implement
        raise NotImplementedError("Stub: add not implemented")
    
    def get_recent(self, limit: int = 10) -> list[str]:
        """Get recent search queries"""
        # TODO: Implement
        raise NotImplementedError("Stub: get_recent not implemented")
    
    def clear(self) -> None:
        """Clear search history"""
        # TODO: Implement
        raise NotImplementedError("Stub: clear not implemented")
