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

from typing import Set, Dict
from collections import Counter

class TransactionDatabase():
    """
    a transaction database is a multi-set of transactions. each transaction
    is a set of items. one example for a transaction is a shopping basket
    with the articles in the basket as items.
    """

    def __init__(self, transactions = None):
        self.__transactions = transactions

    def __iter__(self):
        return iter(self.__transactions)

    def save_to_fic_file(self, path: str):
        """
        saves the transaction database to a file in so-called FIC format.
        See the README of Mexican in the thirdparty folder for more information

        Parameters
        ----------
        path : str
            the path of the fic file.
        Returns
        -------
        dict
            a dictionary that maps item id's back to items
        """
        item_count_dict = self.count_item_occurence()
        item_to_id_dict = {
            item: i for i,item in enumerate(item_count_dict.keys())
        }
        with open(path, 'w') as fic_file:
            fic_file.write('fic-1.5\n')
            fic_file.write('mi: nR=%d nT=%d nI=%d aS=%d sS=212624.77319 mL=%d\n' %(
                len(self), self.get_nr_of_unique_transactions(),
                self.get_nr_of_items_in_transactions(),
                len(item_to_id_dict),
                self.get_maximum_transaction_length()))
            fic_file.write('ab: ' + ' '.join(
                str(i) for i in sorted(item_to_id_dict.values())) + '\n')
            fic_file.write('ac: ' + ' '.join(
                str(item_count_dict[item]) for item,i
                in sorted(item_to_id_dict.items(), key=lambda v: -v[1])) + '\n')
            fic_file.write('it: ' + ' '.join(
                str(i) for i in sorted(item_to_id_dict.values())) + '\n')
            for transaction in self.__transactions:
                fic_file.write('%d: %s\n' % (
                    len(transaction), ' '.join(
                        str(item_to_id_dict[item])
                        for item in transaction)))
        return {v:k for k,v in item_to_id_dict.items()}

    def save_to_dat_file(self, path: str, offset: int = 0):
        """
        saves the transaction database to a file in so-called DAT format.
        each column is an item and each line is an integer encoded transaction

        Parameters
        ----------
        path : str
            the path of the dat file.
        Returns
        -------
        dict
            a dictionary that maps item id's back to items
        """
        item_to_int = {
            item: i+offset for i, item in enumerate(sorted(self.get_itemset()))
        }
        with open(path, 'w') as dat_file:
            for transaction in self.__transactions:
                dat_file.write(' '.join(map(str, map(item_to_int.get, transaction))))
                dat_file.write('\n')
        return {v:k for k,v in item_to_int.items()}

    def __len__(self) -> int:
        """
        returns the number of transactions in this database
        """
        return len(self.__transactions)

    def get_nr_of_unique_transactions(self) -> int:
        """
        returns the number of unique transactions (unique item sets) in this
        database
        """
        return len(set(self.__transactions))

    def get_nr_of_items_in_transactions(self) -> int:
        """
        returns the total number of items in all transactions
        """
        nr_of_items = 0
        for transaction in self.__transactions:
            nr_of_items += len(transaction)
        return nr_of_items

    def get_nr_of_different_items(self) -> int:
        """
        returns how many different items are in this database
        """
        return len(self.get_itemset())

    def get_itemset(self) -> Set[str]:
        """
        returns the unique items in this database
        """
        item_set = set()
        for transaction in self.__transactions:
            item_set.update(transaction)
        return item_set

    def count_item_occurence(self) -> Dict[str,int]:
        """
        counts how often each item occurs in this database

        Returns
        -------
        Dict[str,int]
            a dictionary that sotres the number of occurences per item.
        """
        counter = Counter()
        for transaction in self.__transactions:
            for item in transaction:
                counter[item] += 1
        return counter

    def get_maximum_transaction_length(self) -> int:
        """
        returns the maximum number of items in a transaction
        """
        return max(len(transaction) for transaction in self.__transactions)
