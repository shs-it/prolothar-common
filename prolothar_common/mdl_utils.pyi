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

def L_N(n: int) -> float: ...
def log2binom(n: int, k: int) -> float: ...
def log2multinom(n: int, ks: list[int]|tuple[int]|set[int]) -> float: ...
def L_U(m: int, n: int) -> float: ...
def prequential_coding_length(counts: dict[object,int], epsilon: float = 0.5) -> float: ...
def cached_lgamma(x: float) -> float: ...
def L_R(real_number: float, precision: int = 5) -> float: ...