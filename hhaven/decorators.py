"""Library decorators."""

from . import exceptions


def requires_build(func):
    def wrapper(self, *args, **kwargs):
        if not self.built:
            raise exceptions.HHavenException("Hentai Haven client was not fully initialized. Remember to use client.build() to complete client initialization.", 0)
        return func(self, *args, **kwargs)
    return wrapper


def requires_token(func):
    def wrapper(self, *args, **kwargs):
        if not self.token:
            raise exceptions.TokenException("Hentai Haven token is missing. Use client.get_new_token() to obtain it.", 0)
        return func(self, *args, **kwargs)
    return wrapper


def cached(func):
    """Cache async function."""
    async def wrapper(self, *args, **kwargs):
        if self.cache:
            key = f"{func.__name__}_{args}_{kwargs}"
            cached = await self.cache.get(key)
            if cached is not None:
                return cached

        result = await func(self, *args, **kwargs)

        if self.cache:
            await self.cache.set(key, result, ttl=self.cache_ttl)

        return result

    return wrapper
