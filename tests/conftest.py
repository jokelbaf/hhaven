import pytest

import hhaven


@pytest.fixture(scope="session")
async def client():
    """Return a HHaven client instance."""
    client = await hhaven.Client(debug=True).build()
    return client
