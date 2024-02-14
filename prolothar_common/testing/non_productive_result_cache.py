from typing import Callable
import os
from pickle import dump
from pickle import load

def non_productive_result_cache(cache_dir: str, key: Callable[[tuple, dict],str] = None):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    def decorator(function):
        def wrapper(*args, **kwargs):
            if key is not None:
                result_cache_file = os.path.join(cache_dir, f'{function.__name__}{key(*args,**kwargs)}')
            else:
                result_cache_file = os.path.join(cache_dir, function.__name__)
            if os.path.exists(result_cache_file):
                with open(result_cache_file, 'rb') as f:
                    return load(f)
            else:
                result = function(*args, **kwargs)
                with open(result_cache_file, 'wb') as f:
                    dump(result, f)
                return result
        return wrapper
    return decorator