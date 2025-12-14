"""
Infrastructure Layer - Authentication Service

OAuth 2.0 Device Authorization Grant implementation for kino.pub API.
Follows RFC 8628 specification.
"""

from typing import Optional
from abc import ABC, abstractmethod

from ..domain import AuthToken, DeviceCode


class IAuthService(ABC):
    """Authentication service interface"""
    
    @abstractmethod
    def initiate_device_flow(self) -> DeviceCode:
        """Start OAuth device authorization flow"""
        pass
    
    @abstractmethod
    def poll_for_token(self, device_code: str) -> Optional[AuthToken]:
        """Poll for authorization token"""
        pass
    
    @abstractmethod
    def refresh_token(self, refresh_token: str) -> AuthToken:
        """Refresh access token"""
        pass
    
    @abstractmethod
    def register_device(self, token: AuthToken) -> None:
        """Register device after authentication"""
        pass


class KinoPubAuthService(IAuthService):
    """
    Kino.pub OAuth authentication service.
    
    OAuth endpoints:
    - Device code: POST /oauth/device
    - Token: POST /oauth/token
    - Device registration: POST /oauth/device
    
    Client credentials:
    - CLIENT_ID: xbmc
    - CLIENT_SECRET: cgg3gq04h04cc8k044ggg4kww0k0osgok4ocg0kw
    """
    
    CLIENT_ID = "xbmc"
    CLIENT_SECRET = "cgg3gq04h04cc8k044ggg4kww0k0osgok4ocg0kw"
    
    def __init__(self, base_url: str = "https://api.service-kp.com"):
        self.base_url = base_url
        # TODO: Initialize HTTP client
    
    def initiate_device_flow(self) -> DeviceCode:
        """
        Start OAuth device authorization flow.
        
        Endpoint: POST /oauth/device
        Body: {client_id: CLIENT_ID, client_secret: CLIENT_SECRET}
        
        Response:
        {
            "code": "device_code",
            "user_code": "XXXX-XXXX",
            "verification_uri": "https://kino.pub/device",
            "expires_in": 300,
            "interval": 5
        }
        """
        # TODO: Implement
        raise NotImplementedError("Stub: initiate_device_flow not implemented")
    
    def poll_for_token(self, device_code: str) -> Optional[AuthToken]:
        """
        Poll for authorization token.
        
        Endpoint: POST /oauth/token
        Body: {
            grant_type: "device_code",
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            code: device_code
        }
        
        Response on success:
        {
            "access_token": "...",
            "refresh_token": "...",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        
        Response on pending: HTTP 400 {"error": "authorization_pending"}
        Response on expired: HTTP 400 {"error": "expired_token"}
        
        Returns:
            AuthToken if authorized, None if still pending
        
        Raises:
            Exception if token expired or other error
        """
        # TODO: Implement
        raise NotImplementedError("Stub: poll_for_token not implemented")
    
    def refresh_token(self, refresh_token: str) -> AuthToken:
        """
        Refresh access token.
        
        Endpoint: POST /oauth/token
        Body: {
            grant_type: "refresh_token",
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            refresh_token: refresh_token
        }
        
        Response:
        {
            "access_token": "...",
            "refresh_token": "...",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        """
        # TODO: Implement
        raise NotImplementedError("Stub: refresh_token not implemented")
    
    def register_device(self, token: AuthToken) -> None:
        """
        Register device after authentication.
        
        Endpoint: POST /oauth/device
        Headers: {Authorization: "Bearer {access_token}"}
        Body: {
            title: "Kodi",
            hardware: "...",
            software: "..."
        }
        
        Note: Uses same endpoint as device code initiation,
        but with Bearer token for registration.
        """
        # TODO: Implement
        raise NotImplementedError("Stub: register_device not implemented")
