from collections import UserList

from ..api.list import *
from ..api.extensions import *
from ..utils import tuplize
from ..exceptions import UniqueConstraintError
from .row import Row




class BaseList(UserList):

    def __init__(self, records:list, uniques:tuple=None, fill_missed=True,  fill_value=None):
        self.uniques = tuplize(uniques)
        self.fill_value = fill_value
        self.fill_missed = fill_missed
        if self.uniques:
            records = self.check_for_uniques(records)
        if self.fill_missed:
            records = self.normalize_records(records, fill_value)
        super().__init__(map(Row, records))

    def as_kwargs(self, **updates):
        default = asselect(self.__dict__, ['uniques', 'fill_value', 'fill_missed'])
        default.update(updates)
        return default

    def check_for_uniques(self, records):
        uniqueset = set(self.uniques)
        seen = {}
        for row in records:
            missing = uniqueset - row.keys()
            if missing:
                missing = ', '.join(missing)
                raise UniqueConstraintError(
                    "The key(s) of {} does not exist in the {} for unique constraint validation".format(missing, row)
                )
            values = asvalues(row, self.uniques)
            exists = seen.get(values)
            if exists:
                raise UniqueConstraintError(
                    "\nUnique Constraint Failed in.\n{}\n{}\non:{}".format(exists, row, self.uniques)
                )
            seen[values] = row
            yield row

    def normalize_records(self, records, value):
        return fillmissed(records, value)
    
    @classmethod
    def from_csv(cls, file, uniques=None, encoding='utf-8'):
        return cls(read_csv(file, encoding=encoding), uniques)
    
    def print(self, nrow=25, **print_kwargs):
        for i, row in enumerate(self):
            if i == nrow:
                break
            print(row, **print_kwargs)