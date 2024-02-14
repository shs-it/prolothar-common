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
"""
contains various definitions of patterns in a log file
"""
from typing import List
import prolothar_common.math_utils as math_utils
from prolothar_common.models.suffix_tree import SuffixTree
from functools import reduce
from prolothar_common.collections import list_utils

Sequence = List[str]
ListOfSequences = List[Sequence]

#Finding Maximal Repetitions in a Word in Linear Time
#http://monge.univ-mlv.fr/~koutcher/PAPERS/KolpakovKucherovFOCS99.pdf

def is_tandem_array(trace: Sequence, start_index: int, repeat_type: Sequence,
                    return_k=False, max_k=None):
    """checks whether a given subsequence at a given position is a so-called
    tandem_array of the given trace.
    See "Abstractions in Process Mining: A Taxonony of Patterns" for the
    definition.

    Args:
        trace: a sequence of activities (strings)
        start_index: start index of the repeat_type in the trace
        repeat_type: subsequence of trace starting at position start_index
        return_k: defaults to False. If True a tuple (bool,k:int) is returned

    Returns:
        if return_k is True (is_tandem_array,k) else is_tandem_array
    """
    k = 0

    while (start_index + len(repeat_type) <= len(trace) and
           trace[start_index:start_index+len(repeat_type)] == repeat_type and
           (max_k == None or k < max_k)):
        k += 1
        start_index += len(repeat_type)

    if return_k:
        return k >= 2, k
    else:
        return k >= 2

def is_maximal_pair(sequence: Sequence, subsequence_a, subsequence_b):
    """checks whether two given subsequences are a so-called maximal pair of
    a given sequence.
    See "Abstractions in Process Mining: A Taxonony of Patterns" for the
    definition.

    Args:
        sequence: a sequence strings
        subsequence_a: pair of (start_index, end_index)
        subsequence_b: pair of (start_index, end_index)

    Returns:
        True iff
        - subsequence_a[0] != subsequence_b[0] and
        - sequence[subsequence_a] == sequence[subsequence_b] and
        - left sides and right sides of subsequences are different
    """
    return (subsequence_a[0] != subsequence_b[0] and
            sequence[subsequence_a] == sequence[subsequence_b] and
            sequence[max(0,subsequence_a[0]-1)] != sequence[max(0,subsequence_b[0]-1)] and
            sequence[min(len(sequence),subsequence_a[1]+1)] != sequence[min(len(sequence),subsequence_b[1]+1)])

def find_maximal_repeats(sequence: Sequence, min_length=1):
    """returns all subsequences of the given sequence that occure in a
    maximal pair => see the "is_maximal_pair" function
    """
    # Create the Suffix Tree.
    suff = SuffixTree(sequence)

    # Store all multiple repeats of a minimal length in a dictionary keyed on number of appearances.
    repeat_dict = {}

    for node in suff.nodes[1:]:
        if suff.total_descendants(node) >= 2 and len(suff.node_word(node)) >= min_length:
            if suff.total_descendants(node) not in repeat_dict:
                repeat_dict[suff.total_descendants(node)] = [suff.node_word(node)]
            else:
                repeat_dict[suff.total_descendants(node)].append(suff.node_word(node))

    # Filter out non-maximal repeats.
    repeats = []
    for values in repeat_dict.values():
        if len(values) == 1:
            repeats += values
        else:
            repeats += filter(lambda v: reduce(lambda a, b: a*b, [v not in word for word in values if word != v]), values)
    return repeats

def find_super_maximal_repeats(sequence: Sequence, min_length=1):
    """returns all maximal repeats (see the find_maximal_repeats function) that
    do not occur as a subsequence of other maximal repeats
    """
    maximal_repeats = find_maximal_repeats(sequence, min_length=min_length)
    return filter_super_maximal_repeats(maximal_repeats)

def filter_super_maximal_repeats(maximal_repeats):
    maximal_repeats.sort(key = lambda repeat: len(repeat))

    super_maximal_repeats = []

    for i,maximal_repeat in enumerate(maximal_repeats):
        is_super_maximal_repeat = True
        char_table = list_utils.make_boyer_moore_char_table(maximal_repeat)
        offset_table = list_utils.make_boyer_moore_offset_table(maximal_repeat)
        for other_maximal_repeat in maximal_repeats[i+1:]:
            if list_utils.is_sublist_bm(other_maximal_repeat, maximal_repeat,
                                        char_table=char_table,
                                        offset_table=offset_table):
                is_super_maximal_repeat = False
                break
        if is_super_maximal_repeat:
            super_maximal_repeats.append(maximal_repeat)

    return super_maximal_repeats

def find_near_super_maximal_repeats(sequence: Sequence, min_length=1,
                                    return_super_maximal_repeats=False):
    """returns all maximal repeats (see the find_maximal_repeats function) that
    occur as a subsequence in the original sequence at a position where no
    super maximal repeat overlaps
    """
    maximal_repeats = list(map(tuple, find_maximal_repeats(sequence, min_length=min_length)))

    super_maximal_repeats = set(filter_super_maximal_repeats(maximal_repeats))

    super_maximal_sequence_mask = _build_super_maximal_sequence_mask(
            sequence, super_maximal_repeats)

    near_super_maximal_repeats = []
    for maximal_repeat in maximal_repeats:
        if (maximal_repeat not in super_maximal_repeats and
            _does_not_overlap_super_maximal_repeat_at_least_once(
                    sequence, maximal_repeat, super_maximal_sequence_mask)):
                near_super_maximal_repeats.append(maximal_repeat)
    # all super maximal repeats are also near super maximal repeats
    near_super_maximal_repeats.extend(super_maximal_repeats)

    near_super_maximal_repeats = list(map(list, near_super_maximal_repeats))
    if return_super_maximal_repeats:
        return near_super_maximal_repeats, super_maximal_repeats
    else:
        return near_super_maximal_repeats

def _build_super_maximal_sequence_mask(sequence, super_maximal_repeats):
    """marks all indices in sequence that are part of a super maximal repeat
    """
    super_maximal_sequence_mask = [False] * len(sequence)
    for super_maximal_repeat in super_maximal_repeats:
        for occurence in list_utils.search_sublist_all_occurences(
                        sequence, super_maximal_repeat):
            for i in range(occurence,occurence + len(super_maximal_repeat)):
                super_maximal_sequence_mask[i] = True
    return super_maximal_sequence_mask

def _no_super_maximal_sequence_in_range(start_index, end_index,
                                        super_maximal_sequence_mask):
    result = True
    for super_maximal_sequence_present in super_maximal_sequence_mask[
            start_index:end_index]:
        if super_maximal_sequence_present:
            return False
    return result

def _does_not_overlap_super_maximal_repeat_at_least_once(
        sequence, maximal_repeat, super_maximal_sequence_mask):
    occurences = list_utils.search_sublist_all_occurences(sequence,
                                                          maximal_repeat)
    for occurence in occurences:
        if _no_super_maximal_sequence_in_range(
                occurence, occurence + len(maximal_repeat),
                super_maximal_sequence_mask):
            return True
    return False

def find_primitive_tandem_repeats(sequence, min_word_length=1, max_word_length=None):
    """returns all primitive tandem repeats (tandem repeat types), i.e. only
    the unique tandem repeats without location and nr of repeitions is returned.
    implementation inspired by "Python for Bioinformatics by Jason Kinser"

    Example:
        find_primitive_tandem_repeats([0,0,4,0,0,1,2,3,1,2,3])
        [[0,0],[1,2,3]]
    """
    if max_word_length is None:
        max_word_length = len(sequence) // 2
    tandem_repeats = []
    for word_length in range(min_word_length, max_word_length + 1):
        for word in extract_words(sequence, word_length):
            if is_primitive_tandem_repeat_type(word):
                _add_word_as_tandem_repeat_if_it_repeats(sequence, word,
                                                        tandem_repeats)
    return tandem_repeats

def _add_word_as_tandem_repeat_if_it_repeats(sequence: Sequence, word: Sequence,
                                         tandem_repeats: ListOfSequences):
    occurences = list_utils.search_sublist_all_occurences(sequence, word)
    for index_b, index_a in zip(occurences, occurences[1:]):
        if abs(index_b - index_a) == len(word):
            tandem_repeats.append(word)
            break

def is_primitive_tandem_repeat_type(repeat_type: Sequence):
    """returns True iff the repeat type is not a tandem array
    """
    #only subsequences that have maximal length should be considered
    #example: if there is a repeating subsequence of length 2, then
    # there is also a subsequence of length 4,6,8,...
    #after some thinking one can come to the conclusion that we only
    #need to check subsequences with the following length:
    #for each primefactor decrease the exponent by 1 and multiply with
    #all other primefactors. in other words: take the number and
    #devide by each unique primefactor

    #get list of prime_factors, e.g. [2,2,2,3] for 2^3*3^1=24
    prime_factors = [1] + math_utils.prime_factors(len(repeat_type))

    checked_prime_factors = set()

    L = len(repeat_type)
    for prime_factor in prime_factors:
        if prime_factor not in checked_prime_factors:
            checked_prime_factors.add(prime_factor)
            subsequence_L = L//prime_factor
            b,k = is_tandem_array(repeat_type, 0,
                                  repeat_type[0:subsequence_L],
                                  return_k=True)
            if b and k == L / subsequence_L:
                return False

    return True

def extract_words(sequence: Sequence, word_size: int):
    """see Python for Bioinformatics by Jason Kinser
    """
    words = []
    L = len(sequence)
    for i in range(L-word_size+1):
        words.append(sequence[i:i+word_size])
    return list(map(list, set(map(tuple, words))))


def create_tandem_arrays_from_repeat_types(
        repeat_types, sequence: Sequence):
    """uses a list of repeat_types and creates for each repeating
    occurence of a repeat type a triple

    Args:
        repeat_types: a list of lists of strings
        sequence: the sequence in which the repeat types are expected to occur

    Returns:
        a list of triples = tandem arrays with k >= 1. This definition
        deviates from the usual requirement of k >= 2 !!!
        the triples are sorted asc by the start index and the length of the
        repeat type
    """
    tandem_arrays = []

    for repeat_type in repeat_types:
        for tandem_array in create_tandem_arrays_from_repeat_type(
                repeat_type, sequence):
            tandem_arrays.append(tandem_array)

    tandem_arrays.sort(key = lambda tandem_array: (
            tandem_array[0], len(tandem_array[1])))
    return tandem_arrays

def create_tandem_arrays_from_repeat_type(
        repeat_type: Sequence, sequence: Sequence):
    """uses a repeat_type and creates for each repeating
    occurence of the repeat type a triple. the triples are sorted by the
    first component. A triple consists of (start_index,repeat_type,nr_of_repeats).

    Args:
        repeat_type: a list of strings, which denotes a repeating subsequence
            of the given sequence
        sequence: the sequence in which the repeat type is expected to occur

    Returns:
        a list of triples = tandem arrays with k >= 1. This definition
        deviates from the usual requirement of k >= 2 !!!
    """
    tandem_arrays = []

    occurences_of_repeat_type = list_utils.search_sublist_all_occurences(
            sequence, repeat_type)

    length_of_repeat_type = len(repeat_type)

    if occurences_of_repeat_type:
        new_tandem_array = [occurences_of_repeat_type[0], repeat_type, 1]
        last_processed_occurence = occurences_of_repeat_type[0]
        for occurence in occurences_of_repeat_type[1:]:
            if abs(last_processed_occurence - occurence) == length_of_repeat_type:
                new_tandem_array[2] += 1
            else:
                tandem_arrays.append(tuple(new_tandem_array))
                new_tandem_array = [occurence, repeat_type, 1]
            last_processed_occurence = occurence
        tandem_arrays.append(tuple(new_tandem_array))

    return tandem_arrays

def get_maximal_repeats_over_log(log: ListOfSequences, trace_separator='|',
                                 min_length=2):
    concatenated_log = list(reduce(lambda a,b: a + [trace_separator] + b, log))
    #Extract all maximal repeats over the concatened log
    #Split repeats with '|' in it because '|' separates different traces
    #The maximum repeat length should be the half of length of the longest trace
    maximal_repeats = set()
    for maximal_repeat in find_super_maximal_repeats(
            concatenated_log, min_length=min_length):
        trace_separator_occurences = list_utils.search_sublist_all_occurences(
                maximal_repeat, trace_separator)
        i = 0
        for j in trace_separator_occurences:
            maximal_repeats.add(tuple(maximal_repeat[i:j]))
            i = j + 1
        maximal_repeats.add(tuple(maximal_repeat[i:]))

    return [repeat for repeat in maximal_repeats if len(repeat) >= min_length]

class TandemArray():
    def __init__(self, trace: Sequence, start_index: int,
                 repeat_type: Sequence, nr_of_repeats: int):
        if not is_tandem_array(trace, start_index, repeat_type,
                               max_k=nr_of_repeats):
            raise ValueError('%r^%r is not a tandem array of %r at position %r' % (
                    repeat_type, nr_of_repeats, trace, start_index))
        self.trace = trace
        self.start_index = start_index
        self.repeat_type = repeat_type
        self.nr_of_repeats = nr_of_repeats

    def is_maximal(self):
        """returns True iff there is no match for the repeat type before
        and after the tandem array
        """
        return (self.trace[max(0, self.start_index - len(self.repeat_type)):
                           self.start_index] != self.repeat_type and
                self.trace[min(len(self.trace),
                               self.start_index
                               + len(self.repeat_type) * self.nr_of_repeats):
                           min(len(self.trace),
                               self.start_index + len(self.repeat_type)
                               + len(self.repeat_type) * self.nr_of_repeats)]
                           != self.repeat_type)

    def has_primitive_tandem_repeat_type(self):
        """returns True iff the repeat type of this tandem array is not a
        tandem array itself.
        """
        return is_primitive_tandem_repeat_type(self.repeat_type)

    def __eq__(self, other):
        return (self.trace == other.trace and
                self.start_index == other.start_index and
                self.repeat_type == other.repeat_type and
                self.nr_of_repeats == other.nr_of_repeats)
