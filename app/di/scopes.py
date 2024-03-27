from typing import Callable, TypeVar
from functools import wraps


T = TypeVar("T", bound=Callable)


def singleton_factory(is_async: bool = False) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        instances = {}

        @wraps(func)
        def get_instance(*args, **kwargs):
            if func not in instances:
                instances[func] = func(*args, **kwargs)
            return instances[func]

        @wraps(func)
        async def get_instance_async(*args, **kwargs):
            if func not in instances:
                instances[func] = await func(*args, **kwargs)

            return instances[func]

        if is_async:
            return get_instance_async

        return get_instance

    return decorator