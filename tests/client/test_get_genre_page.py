import pytest

import hhaven


async def test_get_genre_page(client: hhaven.Client):
    """Test get genre page method."""
    TEST_GENRE_ID = 2594
    TEST_GENRE_NAME = "Ecchi"
    TEST_GENRE_SLUG = "ecchi"

    page = await client.get_genre_page(TEST_GENRE_ID)

    assert page.genre.id == TEST_GENRE_ID
    assert page.genre.name == TEST_GENRE_NAME
    assert page.genre.slug == TEST_GENRE_SLUG
    assert len(page.hentai) > 0
    assert page.total_results > 0
    assert page.total_pages > 0

async def test_get_genre_page_invalid_id(client: hhaven.Client):
    """Test get genre page method with invalid ID."""
    INVALID_GENRE_ID = 99999

    with pytest.raises(hhaven.exceptions.GenrePageNotFound):
        await client.get_genre_page(INVALID_GENRE_ID)
