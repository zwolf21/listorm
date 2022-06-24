from typing import Union
from collections import UserList

from .exceptions import *
from .api import asvalues, extract_keys_from_records
from .utils import tuplize
from .row import Row



class BaseList(UserList):


    def __init__(self, records:Union[list, UserList], uniques:Union[tuple, str]=None, defaults:dict[str, object]=None):
        super().__init__(map(Row, records))
        self.defaults = defaults
        self.uniques = tuplize(uniques)
        self.check_for_uniques()
        self.data = self.normalize_records()


    def check_for_uniques(self, uniques:tuple=None):
        uniques = uniques or self.uniques
        if not uniques:
            return
        uniqueset = set(uniques)
        seen = {}
        for row in self.data:
            missing = uniqueset - row.keys()
            if missing:
                missing = ', '.join(missing)
                raise UniqueConstraintError(
                    "The key(s) of {} does not exist in the {} for unique constraint validation".format(missing, row)
                )
            values = asvalues(row, uniques)
            exists = seen.get(values)
            if exists:
                raise UniqueConstraintError(
                    "\nUnique Constraint Failed in.\n{}\n{}\non:{}".format(exists, row, uniques)
                )
            seen[values] = row

    def normalize_records(self):
        columns = extract_keys_from_records(self.data)
        self.fields = columns
        return [row.normalize(columns, self.defaults) for row in self.data]