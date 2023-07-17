# Usage

All requests to the API must be made through the Client class. Every request requires special Cloudflare token which can be obtained using `get_new_token()` function. You only need to set the token once during client initialization.

## Initializing Client
In order to properly initialize client, `build()` function must be called:

```python
token = "..."

# You can pass token to Client class:
client = await Client(token).build()

# Or to build function:
client = await Client().build(token)
```
If no token was provided during initialization, new token will be automatically obtained via API:

```python
client = await Client().build()

# Will print obtained token
print(client.token)
```

## Debugging
You may want to see all incoming and outgoing traffic the library send and receive. In order to enable debugging, use `debug` argument of the Client class:

```python
client = await Client(debug = True).build()
```

After this you will see logs on every request on console:
```yaml
DEBUG:hhaven.client:GET https://api.hentaihaven.app/v1/search?q=Maid+Kyouiku # Request info
{} # Request body
{'success': True, 'data': [{'post_ID': 87109, 'post_title': 'Maid Kyouiku. Botsuraku Kizoku Rurikawa Tsubaki The Animation', 'post_name': 'maid-kyouiku-botsuraku-kizoku-rurikawa-tsubaki-the-animation', 'post_thumbnail': 'https://hh-imgs.cyou/images/hh/w/f/s_Maid-Kyouiku.-Botsuraku-Kizoku-Rurikawa-Tsubaki-The-Animation-Episode-1.jpg'}]} # Response
```

## Caching
HHaven has built-in caching functionality which uses [aiocache](https://github.com/aio-libs/aiocache) library. This means you have two ways to set up caching:

### Using memory cache
Installation:
```console
pip install aiocache[memcached]
```

Usage:
```python
from aiocache import Cache
from hhaven import Client
import asyncio, time

async def main():
    cache = Cache(Cache.MEMORY)
    client = await Client(cache = cache).build()

    for i in ["First", "Second", "Third"]:
        start = time.time()
        await client.search("Maid Kyouiku")

        print(f"{i} call took {time.time() - start} seconds.")
        
if __name__ == "__main__":
    asyncio.run(main())
```

Result:
```
First call took 0.2489948272705078 seconds.
Second call took 0.0 seconds.
Third call took 0.0 seconds.
```

### Using redis
Installation:
```console
pip install aiocache[redis]
```

Usage:
```python
from aiocache import Cache
from hhaven import Client
import asyncio, time

async def main():
    cache = Cache(Cache.REDIS, endpoint = "127.0.0.1", port = 6379, namespace = "main")
    client = await Client(cache = cache).build()

    for i in ["First", "Second", "Third"]:
        start = time.time()
        await client.search("Maid Kyouiku")

        print(f"{i} call took {time.time() - start} seconds.")
        
if __name__ == "__main__":
    asyncio.run(main())
```

Result:
```
First call took 0.2899123413241 seconds.
Second call took 0.0 seconds.
Third call took 0.0 seconds.
```

## Token validation
Every time you initialize client with your own token, it is validated by requesting home page:
```python title="hhaven/client.py"
...
if validate_token:
    # Validate token
    await self._request("GET", "hentai/home", disable_logging = True)
```

You can disable this behavior by setting `validate_token` to `False` during client initialization:
```python
await Client().build(validate_token = False)
``` 

## Exceptions handling
Some methods can raise custom exceptions. All library exceptions can be imported from `hhaven.exceptions` and used in try/except block:
```python
from hhaven.exceptions import HentaiNotFound

...

try:
    hentai = await client.get_hentai(123)
except HentaiNotFound:
    print("Can not find hentai with this ID.")
```

There are some exceptions that can be applied to multiple methods. For example, `HHavenNotFound` is a parent exception for both `HentaiEpisodeNotFound` and `HentaiNotFound`:
```python
from hhaven.exceptions import HHavenNotFound

try:
    hentai = await client.get_hentai(123)
    episode = await client.get_episode(123, 123)
except HHavenNotFound:
    print("Either hentai or episode was not found.")
```
