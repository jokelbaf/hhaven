import pytest

import hhaven


async def test_get_hentai(client: hhaven.Client):
    """Test get hentai method."""
    TEST_HENTAI_ID = 2131
    TEST_HENTAI_TITLE = "Overflow"
    TEST_HENTAI_NAME = "overflow"

    hentai = await client.get_hentai(TEST_HENTAI_ID)

    assert hentai.id == TEST_HENTAI_ID
    assert hentai.title == TEST_HENTAI_TITLE
    assert hentai.name == TEST_HENTAI_NAME

async def test_get_hentai_invalid_id(client: hhaven.Client):
    """Test get hentai method with invalid ID."""
    INVALID_HENTAI_ID = 99999

    with pytest.raises(hhaven.exceptions.HentaiNotFound):
        await client.get_hentai(INVALID_HENTAI_ID)
