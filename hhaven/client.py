"""Main client module."""

import logging, aiohttp, typing, json, aiocache

from . import exceptions, utility, models
from .decorators import requires_build, requires_token, cached


class Client:
    """Hentai Haven client."""
    
    
    BASE_API_URL = "https://api.hentaihaven.app/v1/"
    
    logger: logging.Logger = logging.getLogger(__name__)
    
    _default_headers: typing.Mapping[str, str] = {
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "user-agent": "HH_xxx_APP",
        "warden": ""
    }
    
    _default_warden_body: typing.Mapping[str, typing.Any] = {
        "sdkInt": 33,
        "board": "goldfish_x86_64",
        "brand": "google",
        "display": "sdk_gphone_x86_64-userdebug 13 TE1A.220922.028 10190541 dev-keys",
        "fingerprint": "google/sdk_gphone_x86_64/emu64xa:13/TE1A.220922.028/10190541:userdebug/dev-keys",
        "manufacturer": "Google",
        "model": "sdk_gphone_x86_64"
    }
    
    def __init__(
        self, 
        token: str = None,
        *,
        cache: aiocache.Cache = None,
        cache_ttl: int = 1800,
        debug: bool = False,
        warden_body: typing.Mapping[str, typing.Any] = _default_warden_body
    ) -> None:
        """
        Initialize Hentai Heaven Client with the given parameters.

        Args:
            token (str, optional): Cloudflare token used to access Hentai Haven API.
            cache (aiocache.Cache, optional): Cache object to cache functions results.
            cache_ttl (int, optional): Time to live for the cache.
            debug (bool, optional): Whether the debug logs are being shown in stdout.
            warden_body (typing.Mapping[str, typing.Any], optional): Custom warden body with your device info.
            
        Note that in order to completely initialize client you 
        need to call `client.build()` function.
        """
        self.token = token
        self.cache = cache
        self.debug = debug
        self.cache_ttl = cache_ttl
        self._default_warden_body = warden_body
        
        self.built = False
        
        if token:
            self._default_headers["warden"] = token
            
            
    @property
    def token(self) -> str:
        """Cloudflare token used to access Hentai Haven API."""
        return self._default_headers["warden"]

    @token.setter
    def token(self, token: str) -> None:
        self._default_headers["warden"] = token
        
    
    @property
    def debug(self) -> bool:
        """Whether the debug logs are being shown in stdout."""
        return logging.getLogger("hhaven").level == logging.DEBUG
        
    
    @debug.setter
    def debug(self, debug: bool) -> None:
        logging.basicConfig()
        level = logging.DEBUG if debug else logging.NOTSET
        logging.getLogger("hhaven").setLevel(level)
    
    
    async def build(
        self, 
        token: str = None,
        *,
        validate_token: bool = True
    ) -> "Client":
        """
        Use this function to build a client.
        
        Args:
            token (str, optional): Token used to access Hentai Heaven API.
            validate_token (bool, optional): Validate token with test request to the API.
        Returns:
            Built client.
        """
        if token:
            self.token = token
            self._default_headers["warden"] = token
        
        if not self.token:
            await self.get_new_token(True)
        
        if validate_token:
            # Validate token
            await self._request("GET", "hentai/home", disable_logging = True)
        
        self.built = True
            
        return self
    

    async def _request(
        self,
        method: typing.Literal["GET", "POST"],
        path: str,
        headers: typing.Mapping[str, str] = _default_headers,
        data: typing.Mapping[str, typing.Any] = {},
        disable_logging: bool = False
    ) -> typing.Mapping[str, typing.Any]:
        async with aiohttp.ClientSession(headers = headers) as session:
            async with session.request(
                method = method,
                url = self.BASE_API_URL + path,
                data = data
            ) as r:
                response = await r.json()
                status = utility._get_status_from_response(response) or r.status
                
                if not disable_logging:
                    self.logger.debug("%s %s\n%s\n%s", method, r.url, json.dumps(data, separators=(",", ":")), response)
                
                if not str(status).startswith("2"):
                    return utility._raise_for_status(status)
                
                return response
        
    
    @requires_build
    @requires_token
    @cached
    async def home(self):
        """
        Get home page info.
        
        Returns:
            `models.HomePage` - [Docs](https://github.com)
        """
        data = await self._request("GET", "hentai/home")
        
        return models.HomePage(client = self, **data["data"])
    
    
    @requires_build
    @requires_token
    @cached
    async def search(self, query: str) -> list[models.PartialHentai]:
        """
        Search for hentai.
        
        Args:
            query (str): Query to search for.
        Returns:
            `list[models.PartialHentai]` - [Docs](https://github.com)
        """
        data = await self._request("GET", f"search?q={query}")
        
        # Nothing found
        if type(data["data"]) == str:
            return []
        
        return [models.PartialHentai(client = self, **post) for post in data["data"]]
    
    
    @requires_build
    @requires_token
    @cached
    async def get_hentai(self, id: int) -> models.Hentai:
        """
        Get full hentai info using it's ID. Raises `exceptions.HentaiEpisodeNotFound` if hentai was not found.
        
        Args:
            id (int): ID of the hentai.
        Returns:
            `models.Hentai` - [Docs](https://github.com)
        """
        data = await self._request("GET", f"hentai/{id}")
        
        # Not found
        if type(data["data"]) == str:
            raise exceptions.HentaiNotFound()
        
        return models.Hentai(client = self, **data["data"])
    
    
    @requires_build
    @requires_token
    @cached
    async def get_episode(self, id: int, hentai_id: int) -> models.HentaiEpisode:
        """
        Get full hentai episode info. Raises `exceptions.HentaiEpisodeNotFound` if episode was not found.
        
        Args:
            id (int): ID of the episode.
            hentai_id (int): ID of the hentai this episode belongs to.
        Returns:
            `models.HentaiEpisode` - [Docs](https://github.com)
        """
        data = await self._request("GET", f"hentai/{hentai_id}/episode/{id}")
        
        # Not found
        if type(data["data"]) == str:
            raise exceptions.HentaiEpisodeNotFound()
        
        return models.HentaiEpisode(**data["data"])
    
    
    @requires_build
    @requires_token
    @cached
    async def get_all_genres(self) -> models.HentaiGenre:
        """
        Get all hentai genres.
        
        Returns:
            `list[models.HentaiGenre]` - [Docs](https://github.com)
        """
        data = await self._request("GET", f"genre/all")
        
        return [models.HentaiGenre(client = self, **genre) for genre in data["data"]]

    
    @requires_build
    @requires_token
    @cached
    async def get_genre_page(self, id: int, page: int = 1) -> models.GenrePage:
        """
        Get page with list of hentai of the requested genre. Raises `exceptions.GenrePageNotFound` if page was not found.
        
        Args:
            id (int): ID of the genre you want to get page for.
            page (int, optional): Index of the page you want to get.
        Returns:
            `models.GenrePage` - [Docs](https://github.com)
        """
        data = await self._request("GET", f"genre/{id}?p={page}")
        
        # Not found
        if type(data["data"]) == str:
            raise exceptions.GenrePageNotFound()
        
        return models.GenrePage(client = self, **data["data"])
    
    
    @requires_build
    @requires_token
    @cached
    async def get_all_hentai(self, page: int = 1) -> models.HentaiPage:
        """
        Get page of all available hentai on the website. Raises `exceptions.HentaiPageNotFound` if page was not found.
        
        Args:
            page (int, optional): Index of the page you want to get.
        Returns:
            `models.HentaiPage` - [Docs](https://github.com)
        """
        data = await self._request("GET", f"hentai/all?p={page}")
        
        # Not found
        if type(data["data"]) == str:
            raise exceptions.HentaiPageNotFound()
        
        return models.HentaiPage(client = self, **data["data"])
    
    
    async def get_new_token(
        self, 
        apply: bool = True,
        *,
        body: typing.Mapping[str, typing.Any] = _default_warden_body,
        headers: typing.Mapping[str, str] = _default_headers
    ) -> str:
        """
        Obtain new Cloudflare token. 
        
        Args:
            apply (bool, optional): Apply received token to this client.
        
        Returns:
            Obtained token.
        """
        response = await self._request("POST", "warden", headers, body)
        token = response["data"]["token"]
        
        if apply: 
            self.token = token
            self._default_headers["warden"] = token
            
        return token
