# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine

def add(a: int, b: int) -> int:
    return a + b

def add_throw_exception(a, b):
    raise ValueError()

def has_even_age(parameter, person):
    return person.age % 2 == 0

class Person():
    def __init__(self, age: int):
        self.age = age
    def __eq__(self, other) -> bool:
        return self.age == other.age
    def __repr__(self) -> str:
        return 'Person(%d)' % self.age
    def __hash__(self) -> int:
        return hash(self.age)

def add_persons(a: Person, b: Person) -> Person:
    return Person(a.age + b.age)
def add_persons_dict(person_dict, person: Person) -> Person:
    return Person(person_dict[person.age % 2 == 0].age + person.age)

class TestEngine(ABC):

    def setUp(self):
        self.engine = self.create_engine()

    @abstractmethod
    def create_engine(self) -> ComputationEngine:
        pass

    def test_map_keep_order_False(self):
        list_to_process = [1,2,3,4,5,6,7,8,9,10]
        global_parameter = 1

        partionable_list = self.engine.create_partitionable_list(list_to_process)
        self.assertNotEqual(partionable_list, None)

        mapped_list = partionable_list.map(global_parameter, add, keep_order=False)
        self.assertNotEqual(mapped_list, None)

        self.assertCountEqual([2,3,4,5,6,7,8,9,10,11], mapped_list)

    def test_map_basic_types_assert_correct_order(self):
        list_to_process = [1,2,3,4,5,6,7,8,9,10]
        global_parameter = 1

        partionable_list = self.engine.create_partitionable_list(list_to_process)
        self.assertNotEqual(partionable_list, None)

        mapped_list = partionable_list.map(global_parameter, add, keep_order=True)
        self.assertNotEqual(mapped_list, None)

        self.assertListEqual([2,3,4,5,6,7,8,9,10,11], mapped_list)

    def test_map_persons(self):
        list_to_process = [Person(i) for i in [1,2,3,4,5,6,7,8,9,10]]
        global_parameter = Person(1)

        partionable_list = self.engine.create_partitionable_list(list_to_process)
        self.assertNotEqual(partionable_list, None)

        mapped_list = partionable_list.map(global_parameter, add_persons)
        self.assertNotEqual(mapped_list, None)

        self.assertCountEqual([Person(i) for i in [2,3,4,5,6,7,8,9,10,11]],
                               mapped_list)

    def test_map_dict_parameter_and_large_list(self):
        list_to_process = [Person(i) for i in range(100000)]
        global_parameter = {
                True: Person(1),
                False: Person(2)
        }
        partionable_list = self.engine.create_partitionable_list(list_to_process)
        mapped_list = partionable_list.map(global_parameter, add_persons_dict)
        self.assertNotEqual(mapped_list, None)

    def test_map_exception(self):
        list_to_process = [Person(i) for i in range(100)]
        global_parameter = Person(1)
        partionable_list = self.engine.create_partitionable_list(list_to_process)
        try:
            partionable_list.map(global_parameter, add_throw_exception)
            self.fail('ValueError expected')
        except ValueError:
            pass

    def test_map_filter(self):
        list_to_process = [Person(i) for i in range(100)]
        global_parameter = Person(1)
        partionable_list = self.engine.create_partitionable_list(list_to_process)
        mapped_list = partionable_list.map_filter(global_parameter, add_persons,
                                                  has_even_age)
        self.assertEqual(50, len(mapped_list))

    def test_map_reduce(self):
        list_to_process = [1,2,3,4,5,6,7,8,9,10]
        global_parameter = 1
        partionable_list = self.engine.create_partitionable_list(list_to_process)
        mapped_list = partionable_list.map_reduce(global_parameter, add, add)
        self.assertNotEqual(mapped_list, None)

        self.assertEqual(sum([2,3,4,5,6,7,8,9,10,11]), mapped_list)
