import hhaven


async def test_home(client: hhaven.Client):
    """Test home page method."""
    home = await client.home()
    
    assert len(home.last) > 0
    assert len(home.ecchi) > 0
    assert len(home.last) > 0
