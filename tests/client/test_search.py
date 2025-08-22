import hhaven


async def test_search(client: hhaven.Client):
    """Test search method."""
    TEST_HENTAI_TITLE = "Overflow"
    TEST_HENTAI_NAME = "overflow"

    results = await client.search(TEST_HENTAI_TITLE)

    assert len(results) > 0
    assert TEST_HENTAI_TITLE in results[0].title
    assert TEST_HENTAI_NAME in results[0].name
