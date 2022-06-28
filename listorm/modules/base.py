from ..api.list import *
from ..api.extensions import *
from ..utils import tuplize
from ..exceptions import UniqueConstraintError



class ListBase(list):

    
    def __init__(self, records:list, uniques=None, normalize=True, fill_miss=None):
        self.uniques = tuplize(uniques)
        self.normalize = normalize
        self.fill_miss = fill_miss
        self._check_for_uniques(records)
        records = self._normalize_records(records, fill_miss)
        super().__init__(records)

    def _check_for_uniques(self, records):
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

    def _normalize_records(self, records, value):
        if not self.normalize:
            return records
        columns = get_allkeys(records)
        self.fields = columns
        return fillmissed(records, value)
    

    @classmethod
    def from_csv(cls, file, uniques=None, encoding='utf-8'):
        return cls(read_csv(file, encoding=encoding), uniques)