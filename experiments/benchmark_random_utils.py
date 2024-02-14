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

from numpy.random import default_rng

from prolothar_common.experiments.stopwatch import Stopwatch
from prolothar_common.random_utils import BufferingChoice

seed = 42
number_of_choices = 1_000_000
options = list(range(5))
probabilities = [0.1, 0.2, 0.15, 0.45, 0.1]

stopwatch = Stopwatch()

random_generator = default_rng(seed)
stopwatch.start()
for _ in range(number_of_choices):
    random_generator.choice(options, p=probabilities)
print(f'without buffering: {stopwatch.get_elapsed_time()}')

random_generator = BufferingChoice(options, probabilities, buffer_size=1000, seed=seed)
stopwatch.start()
for _ in range(number_of_choices):
    random_generator.next_sample()
print(f'with buffer size 1000: {stopwatch.get_elapsed_time()}')

random_generator = BufferingChoice(options, probabilities, buffer_size=10000,  seed=seed)
stopwatch.start()
for _ in range(number_of_choices):
    random_generator.next_sample()
print(f'with buffer size 10000: {stopwatch.get_elapsed_time()}')