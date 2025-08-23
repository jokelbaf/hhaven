import os

import aiohttp
import dotenv
import pytest

import hhaven


@pytest.fixture(scope="session")
async def client():
    """Return a HHaven client instance."""
    proxy, proxy_auth = get_proxy_config()
    client = await hhaven.Client(debug=True, proxy=proxy, proxy_auth=proxy_auth).build()
    return client

def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest."""
    dotenv.load_dotenv()

def get_proxy_config() -> tuple[str | None, aiohttp.BasicAuth | None]:
    """Get proxy configuration from environment variables."""
    proxy = os.getenv("PROXY_URL")
    username = os.getenv("PROXY_USERNAME")
    password = os.getenv("PROXY_PASSWORD")

    proxy_auth = aiohttp.BasicAuth(
        login=username,
        password=password,
    ) if username and password else None

    return proxy, proxy_auth
