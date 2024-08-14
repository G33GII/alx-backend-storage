#!/usr/bin/env python3
"""Cache module for storing data using Redis"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called

    Args:
        method: The method to be decorated

    Returns:
        Callable: The wrapped method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """Cache class for storing data using Redis"""

    def __init__(self):
        """Initialize the Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key

        Args:
            data: The data to be stored (can be str, bytes, int, or float)

        Returns:
            str: The randomly generated key used to store the data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Get data from Redis by key and optionally convert it using the provided function

        Args:
            key: The key to retrieve data from Redis
            fn: Optional callable to convert the data

        Returns:
            The data from Redis, optionally converted by fn, or None if the key doesn't exist
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Get a string from Redis by key

        Args:
            key: The key to retrieve data from Redis

        Returns:
            The string data from Redis, or None if the key doesn't exist
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Get an integer from Redis by key

        Args:
            key: The key to retrieve data from Redis

        Returns:
            The integer data from Redis, or None if the key doesn't exist
        """
        return self.get(key, fn=int)

