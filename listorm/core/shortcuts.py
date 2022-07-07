from collections import namedtuple

from ..utils import reduce_kwargs, reduce_args
from ..api import values_count, write_excel, write_csv, asgroup, asdiff, set_number_format



class ShortCutMixin:

    @property
    def exists(self):
        return len(self) != 0

    @property
    def first(self):
        if self: return self[0]
    
    @property
    def count(self):
        return len(self)

    @property
    def last(self):
        if self: return self[-1]

    def max(self, column:str):
        '''get max
        '''
        values = filter(None, self.values(column))
        return max(values)

    def min(self, column:str):
        values = filter(None, self.values(column))
        return min(values)
    
    @reduce_kwargs('formats')
    def set_number_type(self, formats:dict):
        records = set_number_format(self, formats=formats)
        return self.__class__(records)
        
    @reduce_args('columns')
    def values_count(self, columns:list):
        return values_count(self, columns)

    def to_excel(self, filename=None):
        return write_excel(self, filename, fill_miss=False)

    def to_csv(self, filename=None, fields=None, encoding='utf-8', **csv_kwargs):
        return write_csv(self, filename, fields=fields, encoding=encoding, **csv_kwargs)

    def get_changes(self, other):
        if not all([self.uniques, other.uniques]):
            raise ValueError("Both of list has unique keys")
        elif self.uniques != other.uniques:
            raise ValueError("Both unique key fields({}, {}) must be same".format(self.uniques, other.uniques))
        elif not isinstance(other, self.__class__):
            raise ValueError("{} must be Listorm instance, not {}".format(other, type(other)))
        elif not all([self.exists, other.exists]):
            raise ValueError("Empty list not allowed:")
        
        diff_keys = self.uniques or other.uniques

        beforeset = asgroup(self, diff_keys)
        afterset = asgroup(other, diff_keys)

        comparison_keys = beforeset.keys() | afterset.keys()
        
        Added = namedtuple('Added', 'pk rows')
        Deleted = namedtuple('Deleted', 'pk rows')
        Updated = namedtuple('Updated', 'pk before after where')
        Changes = namedtuple('Changes', 'added deleted updated')

        added = []
        deleted = []
        updated = []
        for key in comparison_keys:
            before = beforeset.get(key)
            after = afterset.get(key)
            if before and not after:
                deleted.append(Deleted(key, before[0]))
            elif after and not before:
                added.append(Added(key, after[0]))
            else:
                before, after = before[0], after[0]
                diff = asdiff(before, after)
                if diff:
                    updated.append(Updated(key, before, after, diff))
        return Changes(added, deleted, updated)