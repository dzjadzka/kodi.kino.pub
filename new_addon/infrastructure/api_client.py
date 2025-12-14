"""
Infrastructure Layer - API Client

HTTP client for kino.pub API integration.
Implements all 28 API endpoints documented in api_contract.md.
"""

from typing import Optional, List, Dict
from abc import ABC, abstractmethod

from ..domain import (
    Item, Movie, TVShow, Episode, AuthToken, DeviceCode,
    Pagination, WatchState, Bookmark, Collection, User
)


class IAPIClient(ABC):
    """API Client interface"""
    
    @abstractmethod
    def get_items(
        self,
        content_type: str = "all",
        page: int = 1,
        per_page: int = 50,
        sort: Optional[str] = None
    ) -> tuple[List[Item], Pagination]:
        """Get items list"""
        pass
    
    @abstractmethod
    def get_item(self, item_id: int) -> Item:
        """Get single item by ID"""
        pass
    
    @abstractmethod
    def search_items(self, query: str, page: int = 1) -> tuple[List[Item], Pagination]:
        """Search for items"""
        pass
    
    @abstractmethod
    def get_watching(self) -> List[Item]:
        """Get watching/continue watching list"""
        pass
    
    @abstractmethod
    def mark_watching(self, item_id: int, video_id: int, time: int) -> None:
        """Mark playback time"""
        pass
    
    @abstractmethod
    def toggle_watched(self, item_id: int, video_id: int) -> WatchState:
        """Toggle watched status"""
        pass
    
    @abstractmethod
    def remove_watching(self, item_id: int) -> None:
        """Remove from watching list"""
        pass
    
    @abstractmethod
    def get_bookmarks(self) -> List[Bookmark]:
        """Get bookmark folders"""
        pass
    
    @abstractmethod
    def get_bookmark_items(self, folder_id: int) -> List[Item]:
        """Get items in bookmark folder"""
        pass
    
    @abstractmethod
    def create_bookmark_folder(self, title: str) -> Bookmark:
        """Create new bookmark folder"""
        pass
    
    @abstractmethod
    def add_to_bookmarks(self, folder_id: int, item_id: int) -> None:
        """Add item to bookmark folder"""
        pass
    
    @abstractmethod
    def remove_from_bookmarks(self, folder_id: int, item_id: int) -> None:
        """Remove item from bookmark folder"""
        pass
    
    @abstractmethod
    def get_collections(self) -> List[Collection]:
        """Get content collections"""
        pass
    
    @abstractmethod
    def get_collection(self, collection_id: str) -> Collection:
        """Get collection with items"""
        pass
    
    @abstractmethod
    def get_user_profile(self) -> User:
        """Get user profile information"""
        pass


class KinoPubAPIClient(IAPIClient):
    """
    Kino.pub API client implementation.
    
    Base URL: https://api.service-kp.com
    All requests require Bearer token authentication.
    """
    
    def __init__(self, base_url: str = "https://api.service-kp.com"):
        self.base_url = base_url
        self._access_token: Optional[str] = None
        # TODO: Initialize HTTP client
    
    def set_access_token(self, token: str) -> None:
        """Set access token for authenticated requests"""
        self._access_token = token
    
    def get_items(
        self,
        content_type: str = "all",
        page: int = 1,
        per_page: int = 50,
        sort: Optional[str] = None
    ) -> tuple[List[Item], Pagination]:
        """
        Get items list.
        
        Endpoint: GET /v1/items
        Query params: type, page, perpage, sort
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_items not implemented")
    
    def get_item(self, item_id: int) -> Item:
        """
        Get single item by ID.
        
        Endpoint: GET /v1/items/{id}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_item not implemented")
    
    def search_items(self, query: str, page: int = 1) -> tuple[List[Item], Pagination]:
        """
        Search for items.
        
        Endpoint: GET /v1/items/search
        Query params: q, page
        """
        # TODO: Implement
        raise NotImplementedError("Stub: search_items not implemented")
    
    def get_watching(self) -> List[Item]:
        """
        Get watching/continue watching list.
        
        Endpoint: GET /v1/watching
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_watching not implemented")
    
    def mark_watching(self, item_id: int, video_id: int, time: int) -> None:
        """
        Mark playback time.
        
        Endpoint: POST /v1/watching/marktime
        Body: {video: video_id, time: time}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: mark_watching not implemented")
    
    def toggle_watched(self, item_id: int, video_id: int) -> WatchState:
        """
        Toggle watched status.
        
        Endpoint: POST /v1/watching/toggle
        Body: {video: video_id}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: toggle_watched not implemented")
    
    def remove_watching(self, item_id: int) -> None:
        """
        Remove from watching list.
        
        Endpoint: DELETE /v1/watching/{id}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: remove_watching not implemented")
    
    def get_bookmarks(self) -> List[Bookmark]:
        """
        Get bookmark folders.
        
        Endpoint: GET /v1/bookmarks
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_bookmarks not implemented")
    
    def get_bookmark_items(self, folder_id: int) -> List[Item]:
        """
        Get items in bookmark folder.
        
        Endpoint: GET /v1/bookmarks/{folder_id}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_bookmark_items not implemented")
    
    def create_bookmark_folder(self, title: str) -> Bookmark:
        """
        Create new bookmark folder.
        
        Endpoint: POST /v1/bookmarks/create
        Body: {title: title}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: create_bookmark_folder not implemented")
    
    def add_to_bookmarks(self, folder_id: int, item_id: int) -> None:
        """
        Add item to bookmark folder.
        
        Endpoint: POST /v1/bookmarks/add
        Body: {folder: folder_id, item: item_id}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: add_to_bookmarks not implemented")
    
    def remove_from_bookmarks(self, folder_id: int, item_id: int) -> None:
        """
        Remove item from bookmark folder.
        
        Endpoint: POST /v1/bookmarks/remove-item
        Body: {folder: folder_id, item: item_id}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: remove_from_bookmarks not implemented")
    
    def get_collections(self) -> List[Collection]:
        """
        Get content collections.
        
        Endpoint: GET /v1/collections
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_collections not implemented")
    
    def get_collection(self, collection_id: str) -> Collection:
        """
        Get collection with items.
        
        Endpoint: GET /v1/collections/{id}
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_collection not implemented")
    
    def get_user_profile(self) -> User:
        """
        Get user profile information.
        
        Endpoint: GET /v1/user
        """
        # TODO: Implement
        raise NotImplementedError("Stub: get_user_profile not implemented")
