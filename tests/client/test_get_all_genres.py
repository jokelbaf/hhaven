import hhaven


async def test_get_all_genres(client: hhaven.Client):
    """Test get all genres method."""
    genres = await client.get_all_genres()

    assert len(genres) > 0
