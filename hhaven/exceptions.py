"""All HHaven exceptions."""
import typing

__all__ = [
    "HHavenException",
    "HHavenRateLimited",
    "HHavenNotFound",
    "TokenException",
    "HentaiNotFound",
    "GenrePageNotFound",
    "HentaiPageNotFound",
    "HentaiEpisodeNotFound"
]

class HHavenException(Exception):
    """Base Hentai Haven exception."""
    
    status: int = 0
    message: str = ""
    
    def __init__(
        self,
        message: str | None = None,
        status: int = status
    ) -> None:
        self.status = status
        self.message = message or self.message
        
        if self.status:
            self.message = f"[{self.status}] {self.message}"
        
        super().__init__(self.message)
    
    @property
    def response(self) -> typing.Mapping[str, typing.Any]:
        return {"status": self.status, "message": self.message, "data": None}

class HHavenRateLimited(HHavenException):
    """You were rate limited. Please try again later."""
    
    status = 429
    message = "You were rate limited. Please try again later."
    
    
class HHavenNotFound(HHavenException):
    """Requested resource does not exist."""
    
    status = 404
    message = "Requested resource does not exist."

class TokenException(HHavenException):
    """Invalid Hentai Haven token."""
    
    status = 502
    message = "Invalid Hentai Haven token."

class HentaiNotFound(HHavenNotFound):
    """Unable to find hentai with the ID you provided."""
    
    status = 404
    message = "Unable to find hentai with the ID you provided."

class GenrePageNotFound(HHavenNotFound):
    """Unable to find genre page with the ID and index you provided."""
    
    status = 404
    message = "Unable to find genre page with the ID and index you provided."

class HentaiPageNotFound(HHavenNotFound):
    """Unable to find hentai page with this index."""
    
    status = 404
    message = "Unable to find hentai page with this index."

class HentaiEpisodeNotFound(HHavenNotFound):
    """Unable to find hentai episode with the IDs you provided."""
    
    status = 404
    message = "Unable to find hentai episode with the IDs you provided."
