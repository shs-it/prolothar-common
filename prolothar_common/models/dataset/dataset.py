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

from itertools import chain
from typing import Iterable, Iterator, Tuple, List, Dict
from random import Random
import csv
import pandas as pd

from prolothar_common.models.dataset.instance import Instance
from prolothar_common.models.dataset.attributes import Attribute
from prolothar_common.models.dataset.attributes import CategoricalAttribute
from prolothar_common.models.dataset.attributes import NumericalAttribute

class Dataset():
    """a dataset with instances with categorical and numerical attributes"""

    def __init__(self, categorical_attribute_names: Iterable[str],
                 numerical_attribute_names: Iterable[str]):
        """creates an empty dataset"""
        self.__instances = set()
        self.__attributes = {}
        self.__categorical_attribute_names = []
        for attribute_name in categorical_attribute_names:
            self.add_categorical_attribute(attribute_name, [])
        self.__numerical_attribute_names = list(numerical_attribute_names)
        for attribute_name in numerical_attribute_names:
            self.__attributes[attribute_name] = NumericalAttribute(
                    attribute_name, set())

    def add_instance(self, instance: Instance):
        """adds a new instance to this dataset. if there already is an instance
        with the same id in the dataset, it will be replaced.
        """
        instance_feature_names = set(instance.get_feature_names())
        if instance_feature_names != self.__attributes.keys():
            raise ValueError('inconsistent feature names '
                             'between dataset and instance:'
                             '%r != %r' % (instance_feature_names,
                                           self.__attributes.keys()))
        if instance in self.__instances:
            raise ValueError('instance with id %r already in dataset' %
                             instance.get_id())
        self.__instances.add(instance)
        for attribute_name, attribute in self.__attributes.items():
            attribute.add_value(instance[attribute_name])

    def __contains__(self, instance):
        return instance in self.__instances

    def remove_attribute(self, attribute_name: str):
        """
        removes the given attribute from this dataset and from all instances
        in the dataset
        """
        attribute = self.__attributes.pop(attribute_name)
        if attribute.is_categorical():
            self.__categorical_attribute_names.remove(attribute_name)
        if attribute.is_numerical():
            self.__numerical_attribute_names.remove(attribute_name)
        for instance in self:
            instance.remove_feature(attribute_name)

    def add_categorical_attribute(self, attribute_name: str, values: List):
        if len(self) != len(values):
            raise ValueError('len(values) = %d but should be %d' % (
                len(values), len(self)))
        self.__attributes[attribute_name] = CategoricalAttribute(
                    attribute_name, set(values))
        self.__categorical_attribute_names.append(attribute_name)
        for value,instance in zip(values, self):
            instance[attribute_name] = value

    def add_numerical_attribute(self, attribute_name: str, values: List):
        if len(self) != len(values):
            raise ValueError('len(values) = %d but should be %d' % (
                len(values), len(self)))
        self.__attributes[attribute_name] = NumericalAttribute(
                    attribute_name, set(values))
        self.__numerical_attribute_names.append(attribute_name)
        for value,instance in zip(values, self):
            instance[attribute_name] = value

    def get_attribute_by_name(self, name: str) -> Attribute:
        return self.__attributes[name]

    def get_nr_of_attributes(self) -> int:
        return len(self.__attributes)

    def get_attributes(self) -> Iterable[Attribute]:
        return self.__attributes.values()

    def get_categorical_attribute_names(self) -> str:
        return self.__categorical_attribute_names

    def get_numerical_attribute_names(self) -> str:
        return self.__numerical_attribute_names

    def get_subdataset(self, instances: Iterable[Instance]):
        subdataset = type(self)(
                categorical_attribute_names=self.__categorical_attribute_names,
                numerical_attribute_names=self.__numerical_attribute_names)
        for instance in instances:
            subdataset.add_instance(instance)
        return subdataset

    def export_to_arff(
            self, relation_name: str = 'Nameless Dataset',
            **kwargs) -> str:
        """
        exports the dataset to the Attribute-Relation File Format (ARFF)
        https://www.cs.waikato.ac.nz/~ml/weka/arff.html

        Parameters
        ----------
        relation_name : str, optional
            name of the relation (@RELATION). The default is 'Nameless Dataset'.

        Returns
        -------
        str
            dataset in ARFF.
        """
        arff = '@RELATION "%s"\n' % relation_name

        arff = self._add_attributes_definition_to_arff(arff, **kwargs)

        arff += '\n\n@DATA'
        for instance in self:
            arff = self._add_instance_to_arff(arff, instance, **kwargs)

        return arff

    def _add_attributes_definition_to_arff(self, arff: str, **kwargs) -> str:
        for attribute_name in self.__categorical_attribute_names:
            arff += '\n@ATTRIBUTE "%s" {%s}' % (attribute_name, ','.join(
                '"%s"' % attribute_value for attribute_value in
                sorted(self.get_attribute_by_name(
                    attribute_name).get_unique_values())))

        for attribute_name in self.__numerical_attribute_names:
            arff += '\n@ATTRIBUTE "%s" NUMERIC' % attribute_name

        return arff

    def _add_instance_to_arff(self, arff: str, instance: Instance, **kwargs) -> str:
        arff += '\n'
        features = instance.get_features_dict()
        arff += ','.join(
            '"' + str(features[attribute_name]) + '"'
            for attribute_name in self.__categorical_attribute_names)
        if self.__categorical_attribute_names and self.__numerical_attribute_names:
            arff += ','
        arff += ','.join(
            str(features[attribute_name])
            for attribute_name in self.__numerical_attribute_names)
        return arff

    def to_dataframe(self) -> pd.DataFrame:
        """
        converts this dataset to a pandas dataframe

        Returns
        -------
        pd.DataFrame
            dataframe where each row corresponds to one instance in the dataset
        """
        attribute_names = (
            self.get_categorical_attribute_names() +
            self.get_numerical_attribute_names())
        return pd.DataFrame(
                [
                    [instance[attribute] for attribute in attribute_names]
                    for instance in self
                ],
                columns=attribute_names,
                index=[instance.get_id() for instance in self])

    def copy(self) -> 'Dataset':
        """
        returns a copy of this dataset. for this a new dataset is created
        and a copy of each instance is added to the new dataset
        """
        copy = Dataset(self.__categorical_attribute_names,
                       self.__numerical_attribute_names)
        for instance in self:
            copy.add_instance(instance.copy())
        return copy

    def split(self, testset_proportion: float,
              random_seed: int = None) -> Tuple['Dataset', 'Dataset']:
        """
        splits the dataset into trainset and testset

        Parameters
        ----------
        testset_proportion : float
            must be between 0 and 1 both exclusively. this determines the
            minimal size of the testset in percent of the complete dataset
        random_seed : int, optional
            can be set to a fixed integer to get stable results.
            The default is None.

        Returns
        -------
        a tuple of two datasets (trainset and testset).
        testset can never be empty if the dataset is non-empty, but the
        trainset can be empty if testset_proportion is large enough
        """
        if not (0 < testset_proportion < 1):
            raise ValueError(
                'testset_proportion must be (0,1) but was %f' % testset_proportion)

        trainset = type(self)(self.__categorical_attribute_names,
                              self.__numerical_attribute_names)
        testset = type(self)(self.__categorical_attribute_names,
                             self.__numerical_attribute_names)

        instances = list(iter(self))
        Random(random_seed).shuffle(instances)
        split_index = int(len(self) - len(self) * testset_proportion)

        for instance in instances[:split_index]:
            trainset.add_instance(instance)
        for instance in instances[split_index:]:
            testset.add_instance(instance)

        return trainset, testset

    def random_subset(self, size_of_subset: int, random_seed: int = None) -> 'Dataset':
        """
        randomly selects a subset of this dataset

        Parameters
        ----------
        size_of_subset : int
            size of subset. must not be < 0 or > len(dataset)
        random_seed : int, optional
            can be set to an integer to fix random genreator and get stable
            results. The default is None.

        Raises
        ------
        ValueError
            if size_of_subset is < 0 or > len(dataset).

        Returns
        -------
        subset : Dataset
            a random subset of this dataset of size "size_of_subset".
        """
        if size_of_subset < 0 or size_of_subset > len(self):
            raise ValueError('invalid size_of_subset %d for dataset of length %d' % (
                size_of_subset, len(self)))
        instances = list(iter(self))
        Random(random_seed).shuffle(instances)
        subset = type(self)(self.__categorical_attribute_names,
                            self.__numerical_attribute_names)
        for instance in instances[:size_of_subset]:
            subset.add_instance(instance)
        return subset

    def group_by_categorical_attribute(self, attribute_name: str) -> Dict[str, 'Dataset']:
        """
        splits this dataset into groups based on the categories of a categorical attribute.
        returns a list a dictionary with one entry per category. the keys are the
        categories (group names) and the value are the corresponding subdatasets.
        """
        grouped_datasets = {
            category: type(self)(
                self.__categorical_attribute_names,
                self.__numerical_attribute_names)
            for category in
            self.get_attribute_by_name(attribute_name).get_unique_values()
        }
        for instance in self:
            grouped_datasets[instance[attribute_name]].add_instance(instance)
        return grouped_datasets

    def __iter__(self) -> Iterator[Instance]:
        return iter(self.__instances)

    def __len__(self) -> int:
        """returns the number of instances in this dataset"""
        return len(self.__instances)

    def __repr__(self) -> str:
        return self.export_to_arff()

    def __eq__(self, other) -> bool:
        return other.export_to_arff() == self.export_to_arff()

    @staticmethod
    def create_from_arff(arff: str) -> 'Dataset':
        """
        creates a Dataset from the given ARFF string
        """
        all_attribute_names = []
        categorical_attribute_names = []
        numerical_attribute_names = []
        data_section_started = False
        instances = []

        for line in arff.splitlines(keepends=False):
            if data_section_started and line:
                instances.append(Dataset.__parse_arff_instance(line, all_attribute_names))
            elif line.lower().startswith('@attribute'):
                _, attribute_name, attribute_type = line.split(' ')
                attribute_name = attribute_name.strip('"')
                all_attribute_names.append(attribute_name)
                if attribute_type.startswith('{'):
                    categorical_attribute_names.append(attribute_name)
                elif attribute_type.lower() == 'numeric':
                    numerical_attribute_names.append(attribute_name)
                else:
                    raise NotImplementedError(f'unsupported attribute type "{attribute_type}"')
            elif line.lower().startswith('@data'):
                data_section_started = True

        dataset = Dataset(
            categorical_attribute_names=categorical_attribute_names,
            numerical_attribute_names = numerical_attribute_names
        )

        for i,instance in enumerate(instances):
            dataset.add_instance(Instance(i, instance))

        return dataset

    @staticmethod
    def __parse_arff_instance(line: str, all_attribute_names: List[str]) -> dict:
        if line.startswith('{'):
            line = line.strip('{}')
            instance = {attribute_name: 0 for attribute_name in all_attribute_names}
            for sparse_attribute_value in list(csv.reader([line], delimiter=','))[0]:
                attribute_index, attribute_value = sparse_attribute_value.split(' ')
                instance[all_attribute_names[int(attribute_index)]] = int(attribute_value)
            return instance
        else:
            return {
                all_attribute_names[attribute_index]: attribute_value
                for attribute_index, attribute_value
                in enumerate(list(csv.reader([line], delimiter=','))[0])
            }

    @staticmethod
    def create_from_pandas(
        df: pd.DataFrame, categorical_attributes: list[str],
        numerical_attributes: list[str]) -> 'Dataset':
        """
        creates a dataset from a pandas dataframe. it is your responsibility
        that the numerical attributes have the right datatype (float or int).

        Parameters
        ----------
        df : pd.DataFrame
            dataframe containing the data
        categorical_attributes : list[str]
            defines which columns in the dataframe correspond to categorical attributes
        numerical_attributes : list[str]
            defines which columns in the dataframe correspond to numerical attributes

        Returns
        -------
        Dataset
            a dataset corresponding to the dataframe (id=index and only the
            given columns for categorical and numerical attributes)
        """
        dataset = Dataset(categorical_attributes, numerical_attributes)
        for index,row in df.iterrows():
            dataset.add_instance(Instance(index, {
                a: row[a] for a in chain(categorical_attributes, numerical_attributes)
            }))
        return dataset