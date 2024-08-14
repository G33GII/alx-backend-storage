#!/usr/bin/env python3
"""Cache module for storing data using Redis"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))

        return output
    return wrapper

class Cache:
    """Cache class for storing data using Redis"""

    def __init__(self):
        """Initialize the Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a random key and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """Get data from Redis by key and optionally convert it using the provided function"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Get a string from Redis by key"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Get an integer from Redis by key"""
        return self.get(key, fn=int)

def replay(method: Callable):
    """Display the history of calls of a particular function"""
    redis_instance = method.__self__._redis
    method_name = method.__qualname__
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    # Get the number of calls
    calls_count = redis_instance.get(method_name)
    calls_count = int(calls_count.decode('utf-8')) if calls_count else 0

    print(f"{method_name} was called {calls_count} times:")

    # Get inputs and outputs
    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    # Display each call
    for input_args, output in zip(inputs, outputs):
        input_str = input_args.decode('utf-8')
        output_str = output.decode('utf-8')
        print(f"{method_name}{input_str} -> {output_str}")
