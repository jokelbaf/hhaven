import pytest

import hhaven


async def test_get_all_hentai(client: hhaven.Client):
    """Test get all hentai method."""
    page = await client.get_all_hentai()

    assert len(page.hentai) > 0
    assert page.total_results > 0
    assert page.total_pages > 0

async def test_get_all_hentai_invalid_page(client: hhaven.Client):
    """Test get all hentai method with invalid page."""
    INVALID_PAGE = 99999

    with pytest.raises(hhaven.exceptions.HentaiPageNotFound):
        await client.get_all_hentai(INVALID_PAGE)
