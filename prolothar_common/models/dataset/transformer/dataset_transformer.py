# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from prolothar_common.models.dataset import Dataset

class DatasetTransformer(ABC):
    """
    abstract template for any class that transforms a Dataset, e.g. for
    data normalization
    """

    def transform(self, dataset: Dataset, inplace: bool = False) -> Dataset:
        """
        transforms the given dataset

        Parameters
        ----------
        dataset : Dataset
            dataset that will be transformed. the dataset will be copied
            if the inplace parameter is False, which is standard.
        inplace : bool, OPTIONAL
            if False (Default) the given dataset will remain unchanged

        Returns
        -------
        Dataset
            the given dataset with applied transformation. if inplace is True,
            this is the same instance than the given dataet
        """
        if not inplace:
            dataset = dataset.copy()
        self.inplace_transform(dataset)
        return dataset

    @abstractmethod
    def inplace_transform(self, dataset: Dataset) -> Dataset:
        """
        transforms the given dataset inplace

        Parameters
        ----------
        dataset : Dataset
            dataset that will be transformed. the dataset will be copied
            if the inplace parameter is False, which is standard.

        Returns
        -------
        Dataset
            a copy of the given dataset with applied transformation.
        """
        pass