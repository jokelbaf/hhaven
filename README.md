<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/JokelBaf/hhaven/assets/60827680/977e3964-e2f5-443a-b1c5-57f7a3089f6e">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/JokelBaf/hhaven/assets/60827680/521c38e7-96d7-4781-9660-b2a61ee9fb17">
  <img alt="Logo" src="https://github.com/JokelBaf/hhaven/assets/60827680/521c38e7-96d7-4781-9660-b2a61ee9fb17">
</picture>


# HHaven
![GitHub release (with filter)](https://img.shields.io/github/v/release/jokelbaf/hhaven?style=for-the-badge&logo=github&label=Version&labelColor=%23c7423e) ![PyPI](https://img.shields.io/pypi/v/hhaven?style=for-the-badge&logo=pypi&logoColor=white) ![Code Climate coverage](https://img.shields.io/codeclimate/coverage/JokelBaf/hhaven?style=for-the-badge&logo=codeclimate&logoColor=white)

A well-documented and typed API wrapper for [**Hentai Haven**](https://hentaihaven.xxx/), providing efficient asynchronous requests, built-in cache support, and Pydantic Models for seamless autocompletion and linter support.

## Key Features
- **Efficient Asynchronous Structure:** Utilize a fully asynchronous structure that enhances request speed without affecting other processes in your code.
- **Built-in Cache Support:** Benefit from built-in cache support using the aiocache library, reducing unnecessary API requests and improving overall performance.
- **Pydantic Model Output:** Receive all data in the form of Pydantic Models, enabling comprehensive autocompletion and linter support.
- **Comprehensive Documentation:** Explore extensive and user-friendly documentation, covering all aspects of this library.

## Links
Documentation - https://jokelbaf.github.io/hhaven

API Reference - https://jokelbaf.github.io/hhaven-api-reference

## Requirements

- Python 3.8+
- pydantic
- aiohttp
- aiocache

## Installation
From PyPi:
```console
pip install hhaven
```
From GitHub:
```console
pip install git+https://github.com/JokelBaf/hhaven.git
```

## Examples
Search for hentai by it's name:
```python
from hhaven import Client
import asyncio

async def main():
    client = await Client().build()

    results = await client.search("Maid Kyouiku")
    hentai = await results[0].full()

    print(hentai)
        
if __name__ == "__main__":
    asyncio.run(main())
```
Get all episodes of the latest hentai:
```python
from hhaven import Client
import asyncio

async def main():
    client = await Client().build()
    
    home = await client.home()
    hentai = await home.last[0].full()
    
    for episode in hentai.episodes:
        print(episode.name)
        
if __name__ == "__main__":
    asyncio.run(main())
```
