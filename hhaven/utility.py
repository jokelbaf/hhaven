"""Some useful utility."""

import typing

from . import exceptions


__all__ = []


def _raise_for_status(status: int):
    """Raise exception for status."""
    
    if status == 502:
        raise exceptions.TokenException()
    elif status == 429:
        raise exceptions.HHavenRateLimited()
    elif status == 404:
        raise exceptions.HHavenNotFound()
    else:
        raise exceptions.HHavenException("Something went wrong.", status)
    

def _get_status_from_response(response: typing.Mapping[str, typing.Any]) -> int | None:
    """Determine status using response text."""
    
    data = response.get("data", None)
    if data and type(data) == str:
        if data[:3].isdigit(): 
            return int(data[:3])
        
    return None
