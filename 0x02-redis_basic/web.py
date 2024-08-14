#!/usr/bin/env python3
"""Web caching and tracking module"""

import redis
import requests
from functools import wraps
from typing import Callable

# Create a Redis client
redis_client = redis.Redis()


def url_access_count(func: Callable) -> Callable:
    """Decorator to track how many times a URL is accessed"""
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the access count for this URL
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        # Call the original function
        return func(url)
    return wrapper


def cache_result(expiration: int = 10) -> Callable:
    """Decorator to cache the result of a function"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the result is already in cache
            cache_key = f"cache:{url}"
            cached_result = redis_client.get(cache_key)

            if cached_result:
                return cached_result.decode('utf-8')

            # If not in cache, call the original function
            result = func(url)

            # Cache the result with expiration
            redis_client.setex(cache_key, expiration, result)

            return result
        return wrapper
    return decorator


@url_access_count
@cache_result(10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL

    Args:
        url (str): The URL to fetch

    Returns:
        str: The HTML content of the URL
    """
    response = requests.get(url)
    return response.text
