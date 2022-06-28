from ..api.list import *
from ..api.extensions import *
from ..utils import tuplize
from ..exceptions import UniqueConstraintError
from .row import Row




class BaseList(list):

    def __init__(self, records:list, uniques:tuple=None, normalize=True,  fill_missed=None):
        self.uniques = tuplize(uniques)
        self.fill_missed = fill_missed
        self.normalize = normalize
        self.check_for_uniques(records)
        if self.normalize:
            records = self.normalize_records(records, fill_missed)
        super().__init__(map(Row, records))

    def check_for_uniques(self, records):
        if not self.uniques:
            return
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

    def normalize_records(self, records, value):
        return fillmissed(records, value)
    
    @classmethod
    def from_csv(cls, file, uniques=None, encoding='utf-8'):
        return cls(read_csv(file, encoding=encoding), uniques)