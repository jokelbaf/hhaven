"""All HHaven models."""

from datetime import datetime
import pydantic, typing


class HentaiRating(pydantic.BaseModel):
    """Information about hentai rating."""
    rating: float
    """Hentai rating."""
    votes: int
    """Number of people who voted when calculating the rating."""


class HentaiGenre(pydantic.BaseModel):
    """HentaiGenre object."""
    id: int
    """Genre ID."""
    name: str
    """
    Well formatted genre name.
    
    Examples: Yuri, Uncensored.
    """
    slug: str
    """
    Raw genre name.
    
    Examples: hentai-school, yuri.
    """
    count: int
    """Number of hentai of this genre."""
    thumbnail: typing.Optional[str] = None
    """
    Genre thumbnail url. Note that thumbnail is not present in `GenrePage.genre` object.
    
    Example: https://example.com/Yuri.jpg
    """
    client: typing.Any
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("term_", ""): v
            for k, v in data.items()
        }
        super().__init__(**processed)
        
    async def page(self, page: int = 1) -> "GenrePage":
        """
        Get page with hentai of this genre.
        
        Args:
            page (int, optional): Index of the page you want to get.
        Returns:
            `models.GenrePage` - [Docs](https://github.com)
        """
        return await self.client.get_genre_page(self.id, page)


class PartialHentaiGenre(pydantic.BaseModel):
    """Short HentaiGenre object."""
    id: int
    """Genre ID."""
    name: str
    """
    Genre name.
    
    Examples: Yuri, Uncensored.
    """
    client: typing.Any
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("term_", ""): v
            for k, v in data.items()
        }
        super().__init__(**processed)
        
    async def full(self) -> HentaiGenre:
        """
        Get full genre information.
        
        Returns:
            `models.HentaiGenre` - [Docs](https://github.com)
        """
        all_genres = await self.client.get_all_genres()
        return [genre for genre in all_genres if genre.id == self.id]
    
    async def page(self, page: int = 1) -> "GenrePage":
        """
        Get page with hentai of this genre.
        
        Args:
            page (int, optional): Index of the page you want to get.
        Returns:
            `models.GenrePage` - [Docs](https://github.com)
        """
        return await self.client.get_genre_page(self.id, page)
    
    
class GenrePage(pydantic.BaseModel):
    """Page with hentai of certain genre."""
    genre: HentaiGenre
    """Genre of the page."""
    hentai: list["PartialHentai"]
    """List of hentai on this page."""
    total_results: int
    """Total number of hentai on all pages of the genre."""
    index: int
    """Index of current page."""
    total_pages: int
    """Total pages available for this genre."""
    client: typing.Any
    
    def __init__(self, **data):
        data["genre"] = data.pop("term")
        data["hentai"] = data.pop("hentais")
        data["index"] = data.pop("current_page")
        
        for hentai in data["hentai"]:
            hentai["client"] = data.get("client")
        
        data["genre"]["client"] = data.get("client")
        
        super().__init__(**data)
        
    async def next(self) -> "GenrePage":
        """
        Get next page.
        
        Returns:
            `models.GenrePage` - [Docs](https://github.com)
        """
        return await self.client.get_genre_page(self.genre.id, self.index + 1)
    
    async def prev(self) -> "GenrePage":
        """
        Get previous page.
        
        Returns:
            `models.GenrePage` - [Docs](https://github.com)
        """
        return await self.client.get_genre_page(self.genre.id, self.index - 1)
        
        
class HentaiPage(pydantic.BaseModel):
    """Page with all hentai of the website."""
    hentai: list["PartialHentai"]
    """List of hentai on this page."""
    total_results: int
    """Total number of hentai on all pages."""
    index: int
    """Index of current page."""
    total_pages: int
    """Total pages available."""
    client: typing.Any
    
    def __init__(self, **data):
        data["hentai"] = data.pop("hentais")
        data["index"] = data.pop("current_page")
        
        for hentai in data["hentai"]:
            hentai["client"] = data.get("client")
        
        super().__init__(**data)
        
    async def next(self) -> "HentaiPage":
        """
        Get next page.
        
        Returns:
            `models.HentaiPage` - [Docs](https://github.com)
        """
        return await self.client.get_all_hentai(self.index + 1)
    
    async def prev(self) -> "HentaiPage":
        """
        Get previous page.
        
        Returns:
            `models.HentaiPage` - [Docs](https://github.com)
        """
        return await self.client.get_all_hentai(self.index - 1)
     
        
class HentaiTag(pydantic.BaseModel):
    """Hentai tag."""
    id: int
    """Tag ID."""
    name: str
    """
    Tag name.
    
    Examples: HD, Young
    """
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("term_", ""): v
            for k, v in data.items()
        }
        super().__init__(**processed)
        
        
class HentaiAuthor(pydantic.BaseModel):
    """Hentai author object."""
    id: int
    """Author ID."""
    name: str
    """Author's name."""
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("term_", ""): v
            for k, v in data.items()
        }
        super().__init__(**processed)
        
        
class HentaiRelease(pydantic.BaseModel):
    """Hentai release object."""
    id: int
    """Release ID."""
    name: str
    """
    Release name. In most cases it is the year when the hentai was released.
    
    Example: 2023
    """
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("term_", ""): v
            for k, v in data.items()
        }
        super().__init__(**processed)
        
        
class HentaiEpisode(pydantic.BaseModel):
    """Hentai episode."""
    id: int
    """Episode ID."""
    name: str
    """
    Well formatted episode title.
    
    Example: Episode 1
    """
    slug: str
    """
    Raw title.
    
    Example: episode-1
    """
    date: datetime
    """Datetime object representing episode upload date."""
    thumbnail: str
    """
    Episode thumbnail url.
    
    Example: https://example.com/episode_thumbnail.jpg
    """
    hentai_id: int
    """
    ID of the hentai this episode belongs to.
    """
    hentai_name: str
    """
    Raw name of the hentai this episode belongs to.
    
    Example: tsuma-shibori
    """
    hentai_title: str
    """
    Well formatted title of the hentai this episode belongs to.
    
    Example: Tsuma Shibori
    """
    hentai_views: int
    """Number of hentai views."""
    hentai_thumbnail: str
    """
    Hentai thumbnail url.
    
    Example: https://example.com/image.jpg
    """
    hentai_description: str
    """Full hentai description on English."""
    hentai_date: datetime
    """Datetime object representing hentai upload date."""
    hentai_rating: HentaiRating
    """Hentai rating object. Has `rating` and `votes` attributes."""
    hentai_tags: list[HentaiTag]
    """List of hentai tags."""
    hentai_title_alternative: str
    """
    Well formatted alternative title of the hentai this episode belongs to.
    
    Example: Nightmare×Deathscytheー前編...
    """
    hentai_genres: list[PartialHentaiGenre]
    """List of hentai genres."""
    hentai_authors: list[HentaiAuthor]
    """List of hentai authors."""
    hentai_releases: list[HentaiRelease]
    """List of hentai releases."""
    next_episode: typing.Optional["HentaiEpisode"] = None
    """Next hentai episode."""
    prev_episode: typing.Optional["HentaiEpisode"] = None
    """Previous hentai episode."""
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("post_", "hentai_").replace("chapter_", ""): v
            for k, v in data.items()
        }
        processed["hentai_description"] = processed.pop("hentai_content")
        processed["date"] = datetime.strptime(processed["date"], "%Y-%m-%d %H:%M:%S")
        processed["hentai_date"] = datetime.strptime(processed["hentai_date"], "%Y-%m-%d %H:%M:%S")
        
        if data["next_episode"] is not None:
            for key, value in data.items():
                if key not in ("id", "name", "thumbnail", "date", "slug"):
                    if key == "next_episode" or key == "prev_episode":
                        data["next_episode"][key] = None
                    else:
                        data["next_episode"][key] = value
                    
        if data["prev_episode"] is not None:
            for key, value in data.items():
                if key not in ("id", "name", "thumbnail", "date", "slug"):
                    if key == "next_episode" or key == "prev_episode":
                        data["next_episode"][key] = None
                    else:
                        data["next_episode"][key] = value
                        
        for genre in processed["hentai_genres"]:
            genre["client"] = data.get("client")
        
        super().__init__(**processed)
        
        
class PartialHentaiEpisode(pydantic.BaseModel):
    """Simplified HentaiEpisode object."""
    id: int
    """Episode ID."""
    name: str
    """
    Well formatted episode title.
    
    Example: Episode 1
    """
    slug: str
    """
    Raw title.
    
    Example: episode-1
    """
    date: datetime
    """Datetime object representing episode upload date."""
    thumbnail: str
    """
    Episode thumbnail url.
    
    Example: https://example.com/episode_thumbnail.jpg
    """
    hentai_id: int
    """
    ID of the hentai this episode belongs to.
    """
    hentai_name: str
    """
    Raw name of the hentai this episode belongs to.
    
    Example: tsuma-shibori
    """
    hentai_title: str
    """
    Well formatted title of the hentai this episode belongs to.
    
    Example: Tsuma Shibori
    """
    hentai_thumbnail: str
    """
    Hentai thumbnail url.
    
    Example: https://example.com/image.jpg
    """
    hentai_description: str
    """Full hentai description on English."""
    client: typing.Any
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("post_", "hentai_").replace("chapter_", ""): v
            for k, v in data.items()
        }
        processed["hentai_description"] = processed.pop("hentai_content")
        processed["date"] = datetime.strptime(processed["date"], "%Y-%m-%d %H:%M:%S")
        
        super().__init__(**processed)
        
    async def full(self) -> HentaiEpisode:
        """
        Get full episode object.
        
        Returns:
            `models.HentaiEpisode` - [Docs](https://github.com)
        """
        return await self.client.get_episode(self.id, self.hentai_id)

        
class Hentai(pydantic.BaseModel):
    """Hentai object."""
    id: int
    """ID of the hentai."""
    name: str
    """
    Raw hentai name.
    
    Example: tsuma-shibori
    """
    title: str
    """
    Well formatted title.
    
    Example: Tsuma Shibori
    """
    views: int
    """Number of views."""
    thumbnail: str
    """
    Hentai thumbnail url.
    
    Example: https://example.com/image.jpg
    """
    date: datetime
    """Datetime object representing hentai upload date."""
    description: str
    """Full description on English."""
    rating: HentaiRating
    """Hentai rating object. Has `rating` and `votes` attributes."""
    tags: list[HentaiTag]
    """List of hentai tags."""
    title_alternative: str
    """
    Well formatted alternative title.
    
    Example: Nightmare×Deathscytheー前編...
    """
    genres: list[PartialHentaiGenre]
    """List of hentai genres."""
    authors: list[HentaiAuthor]
    """List of hentai authors."""
    releases: list[HentaiRelease]
    """List of releases."""
    episodes: list[PartialHentaiEpisode]
    """List of episodes."""
    client: typing.Any
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("post_", ""): v
            for k, v in data.items()
        }
        processed["description"] = processed.pop("content")
        processed["date"] = datetime.strptime(processed["date"], "%Y-%m-%d %H:%M:%S")
        
        for episode in processed["episodes"]:
            episode["client"] = data.get("client")
            episode["hentai_id"] = processed.get("id")
            episode["hentai_name"] = processed.get("name")
            episode["hentai_title"] = processed.get("title")
            episode["hentai_thumbnail"] = processed.get("thumbnail")
            episode["hentai_content"] = processed.get("description")
                    
        for genre in processed["genres"]:
            genre["client"] = data.get("client")
        
        super().__init__(**processed)


class PartialHentai(pydantic.BaseModel):
    """Simplified Hentai object."""
    id: int
    """ID of the hentai."""
    name: str
    """
    Raw hentai name.
    
    Example: tsuma-shibori
    """
    title: str
    """
    Well formatted hentai title.
    
    Example: Tsuma Shibori
    """
    thumbnail: str
    """
    Hentai thumbnail url.
    
    Example: https://example.com/image.jpg
    """
    client: typing.Any
    
    def __init__(self, **data):
        processed = {
            k.lower().replace("post_", ""): v
            for k, v in data.items()
        }
        super().__init__(**processed)
        
    async def full(self) -> Hentai:
        """
        Get full hentai object.
        
        Returns:
            `models.Hentai` - [Docs](https://github.com)
        """
        return await self.client.get_hentai(self.id)


class HomePage(pydantic.BaseModel):
    """Home page information."""
    
    client: typing.Any
    last: list[PartialHentai]
    """Last released hentai."""
    yuri: list[PartialHentai]
    """List of popular yuri hentai."""
    ecchi: list[PartialHentai]
    """List of popular ecchi hentai."""
    incest: list[PartialHentai]
    """List of popular incest hentai."""
    tentacle: list[PartialHentai]
    """List of popular tentacle hentai."""
    uncensored: list[PartialHentai]
    """List of popular uncensored hentai."""
    trending_month: list[PartialHentai]
    """List of trending month hentai."""
    last_episodes: list[PartialHentaiEpisode]
    """Last released hentai episodes."""
    
    def __init__(self, **data):
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    item["client"] = data.get("client")
                    
        super().__init__(**data)
        