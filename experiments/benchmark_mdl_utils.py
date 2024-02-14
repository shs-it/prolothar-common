from prolothar_common.experiments.stopwatch import Stopwatch
from prolothar_common import mdl_utils

stopwatch = Stopwatch()

stopwatch.start()
for n in range(1, 10_000_000):
    mdl_utils.L_N(n)
print(f'L_N: {stopwatch.get_elapsed_time()}')