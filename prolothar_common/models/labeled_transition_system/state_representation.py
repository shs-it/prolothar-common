from typing import List, Hashable, FrozenSet, Tuple

def set_abstraction(prefix: List[Hashable]) -> FrozenSet:
    return frozenset(prefix)

def list_abstraction(prefix: List[Hashable]) -> Tuple:
    return tuple(prefix)

def last_abstraction(prefix: List[Hashable]) -> Hashable:
    try:
        return prefix[-1]
    except IndexError:
        return None

def last_n_abstraction(n: int):
    def state_representation(prefix: List[Hashable]):
        return tuple(prefix[-n:])
    return state_representation
