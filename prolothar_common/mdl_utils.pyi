def L_N(n: int) -> float: ...
def log2binom(n: int, k: int) -> float: ...
def log2multinom(n: int, ks: list[int]|tuple[int]|set[int]) -> float: ...
def L_U(m: int, n: int) -> float: ...
def prequential_coding_length(counts: dict[object,int], epsilon: float = 0.5) -> float: ...
def cached_lgamma(x: float) -> float: ...
def L_R(real_number: float, precision: int = 5) -> float: ...