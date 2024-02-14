'''
    This file is part of Prolothar-Common (More Info: https://github.com/shs-it/prolothar-common).

    Prolothar-Common is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Prolothar-Common is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Prolothar-Common. If not, see <https://www.gnu.org/licenses/>.
'''

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