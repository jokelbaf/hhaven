import pytest

import hhaven


async def test_get_episode(client: hhaven.Client):
    """Test get episode method."""
    TEST_EPISODE_ID = 624
    TEST_EPISODE_HENTAI_ID = 2131
    TEST_EPISODE_HENTAI_TITLE = "Overflow"
    TEST_EPISODE_HENTAI_NAME = "overflow"

    episode = await client.get_episode(TEST_EPISODE_ID, TEST_EPISODE_HENTAI_ID)

    assert episode.id == TEST_EPISODE_ID
    assert episode.hentai_id == TEST_EPISODE_HENTAI_ID
    assert episode.hentai_title == TEST_EPISODE_HENTAI_TITLE
    assert episode.hentai_name == TEST_EPISODE_HENTAI_NAME

async def test_get_episode_invalid_id(client: hhaven.Client):
    """Test get episode method with invalid ID."""
    INVALID_EPISODE_ID = 99999
    INVALID_EPISODE_HENTAI_ID = 99999

    with pytest.raises(hhaven.exceptions.HentaiEpisodeNotFound):
        await client.get_episode(INVALID_EPISODE_ID, INVALID_EPISODE_HENTAI_ID)
