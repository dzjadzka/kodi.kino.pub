"""
Application Layer - Use Cases

Business logic use cases orchestrating domain and infrastructure.
"""

from typing import List, Tuple, Optional
from abc import ABC, abstractmethod

from ..domain import (
    Item, Movie, TVShow, Episode, AuthToken, DeviceCode,
    Pagination, WatchState, Bookmark, Collection, VideoQuality
)
from ..infrastructure import IAPIClient, IAuthService, ISettings, ICache


class AuthenticateUserUseCase:
    """
    Use case: Authenticate user with OAuth device flow.
    
    Steps:
    1. Initiate device flow
    2. Display user code
    3. Poll for token
    4. Store token
    5. Register device
    """
    
    def __init__(
        self,
        auth_service: IAuthService,
        settings: ISettings
    ):
        self.auth_service = auth_service
        self.settings = settings
    
    def execute(self) -> AuthToken:
        """Execute authentication flow"""
        # TODO: Implement OAuth device flow
        raise NotImplementedError("Stub: AuthenticateUserUseCase not implemented")


class BrowseItemsUseCase:
    """
    Use case: Browse items by content type with pagination.
    """
    
    def __init__(
        self,
        api_client: IAPIClient,
        settings: ISettings
    ):
        self.api_client = api_client
        self.settings = settings
    
    def execute(
        self,
        content_type: str,
        page: int = 1,
        sort: Optional[str] = None
    ) -> Tuple[List[Item], Pagination]:
        """Browse items"""
        # TODO: Implement
        raise NotImplementedError("Stub: BrowseItemsUseCase not implemented")


class SearchItemsUseCase:
    """
    Use case: Search for items.
    """
    
    def __init__(
        self,
        api_client: IAPIClient,
        cache: ICache
    ):
        self.api_client = api_client
        self.cache = cache
    
    def execute(self, query: str, page: int = 1) -> Tuple[List[Item], Pagination]:
        """Search items"""
        # TODO: Implement with caching
        raise NotImplementedError("Stub: SearchItemsUseCase not implemented")


class PlayVideoUseCase:
    """
    Use case: Resolve and play video.
    
    Steps:
    1. Get item details
    2. Select quality (user preference or dialog)
    3. Resolve video URL
    4. Set InputStream Adaptive properties
    5. Return playable URL
    """
    
    def __init__(
        self,
        api_client: IAPIClient,
        settings: ISettings,
        cache: ICache
    ):
        self.api_client = api_client
        self.settings = settings
        self.cache = cache
    
    def execute(
        self,
        item_id: int,
        video_id: Optional[int] = None,
        quality: Optional[VideoQuality] = None
    ) -> str:
        """
        Resolve playable video URL.
        
        Returns: URL to play
        """
        # TODO: Implement quality selection and URL resolution
        raise NotImplementedError("Stub: PlayVideoUseCase not implemented")


class TrackPlaybackUseCase:
    """
    Use case: Track playback progress and update watch status.
    
    Called by player callbacks:
    - onPlayBackStarted: Set resume point to 0 if not resuming
    - onPlayBackStopped: Save resume point
    - onPlayBackEnded: Mark as watched
    """
    
    def __init__(
        self,
        api_client: IAPIClient,
        settings: ISettings
    ):
        self.api_client = api_client
        self.settings = settings
    
    def on_playback_started(self, item_id: int, video_id: int) -> None:
        """Handle playback started"""
        # TODO: Implement
        raise NotImplementedError("Stub: on_playback_started not implemented")
    
    def on_playback_stopped(
        self,
        item_id: int,
        video_id: int,
        time: int,
        duration: int
    ) -> None:
        """Handle playback stopped"""
        # TODO: Implement resume point saving
        raise NotImplementedError("Stub: on_playback_stopped not implemented")
    
    def on_playback_ended(self, item_id: int, video_id: int) -> None:
        """Handle playback ended"""
        # TODO: Implement mark as watched
        raise NotImplementedError("Stub: on_playback_ended not implemented")


class ManageBookmarksUseCase:
    """
    Use case: Manage bookmarks/favorites.
    """
    
    def __init__(self, api_client: IAPIClient):
        self.api_client = api_client
    
    def get_folders(self) -> List[Bookmark]:
        """Get bookmark folders"""
        # TODO: Implement
        raise NotImplementedError("Stub: get_folders not implemented")
    
    def get_folder_items(self, folder_id: int) -> List[Item]:
        """Get items in folder"""
        # TODO: Implement
        raise NotImplementedError("Stub: get_folder_items not implemented")
    
    def add_item(self, folder_id: int, item_id: int) -> None:
        """Add item to folder"""
        # TODO: Implement
        raise NotImplementedError("Stub: add_item not implemented")
    
    def remove_item(self, folder_id: int, item_id: int) -> None:
        """Remove item from folder"""
        # TODO: Implement
        raise NotImplementedError("Stub: remove_item not implemented")


class GetWatchingListUseCase:
    """
    Use case: Get continue watching list.
    """
    
    def __init__(self, api_client: IAPIClient):
        self.api_client = api_client
    
    def execute(self) -> List[Item]:
        """Get watching list"""
        # TODO: Implement
        raise NotImplementedError("Stub: GetWatchingListUseCase not implemented")
