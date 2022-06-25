from collections import namedtuple

from .base import BaseList
from .exceptions import *
from .api import sort, distinct, groupby, join, extend, asgroup, diffkeys
from .utils import reduce_args, reduce_kwargs, tuplize
from .shortcuts import ShortCutMixin




class Listorm(ShortCutMixin, BaseList):

    
    def _reduce_where(self, where):
        return where or (lambda row: True)
        
    def filter(self, where:callable):
        where = self._reduce_where(where)
        return Listorm(filter(where, self), uniques=self.uniques, defaults=self.defaults)

    @reduce_args
    def select(self, *columns:str, excludes:list=None, where:callable=None):
        app = lambda row: row.select(columns, excludes)
        return Listorm(map(app, self.filter(where)))
    
    @reduce_args
    def drop_column(self, *columns:str):
        return self.select(excludes=columns)
    
    @reduce_kwargs
    def add_column(self, *column_mapset:dict, **column_map_kwargs):
        return Listorm(extend(self, column_map_kwargs), uniques=self.uniques, defaults=self.defaults)

    @reduce_kwargs
    def rename(self, *renamemap:dict, **rename_kwargs):
        app = lambda row: row.rename(rename_kwargs)
        return Listorm(map(app, self))

    @reduce_kwargs
    def update(self, *applymap:dict, where:callable=None, pass_undefined:bool=True, **apply_kwargs):
        where = self._reduce_where(where)
        app = lambda row: row.map(apply_kwargs, pass_undefined) if where(row) else row
        return Listorm(map(app, self))
    
    @reduce_args
    def values(self, *columns:str):
        app = lambda row: row.values(columns)
        return list(map(app, self))

    @reduce_args
    def distinct(self, *columns:str, first:bool=True, singles:bool=False):
        return Listorm(distinct(self, columns, first, singles))

    @reduce_args
    def orderby(self, *sortkeys:list):
        return Listorm(sort(self, sortkeys))

    @reduce_args
    @reduce_kwargs
    def groupby(self, *columns:str, aggset:dict=None, aliases:dict=None, groupset_name:str=None, **aggset_kwargs):
        aggset_kwargs.update(aggset or {})
        return Listorm(groupby(self, columns, aggset=aggset_kwargs, aliases=aliases, groupset_name=groupset_name))

    def join(self, other, on:None, right_on=None, how:str='inner'):
        on, right_on = tuplize(on), tuplize(right_on)
        
        if not on:
            on = self.uniques
        if not right_on:
            if isinstance(other, Listorm):
                right_on = other.uniques or on
            else:
                right_on = on
        if not all((on, right_on)):
            raise JoinKeyDoesNotExists('on:{}, right_on:{} must be specified'.format(on, right_on))
        return Listorm(join(self, other, on, right_on, how=how))

    def get_changes(self, other):
        if not all([self.uniques, other.uniques]):
            raise ValueError("Both of list has unique keys")
        elif self.uniques != other.uniques:
            raise ValueError("Both unique key fields({}, {}) must be same".format(self.uniques, other.uniques))
        elif not isinstance(other, Listorm):
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
                diff = diffkeys(before, after)
                if diff:
                    updated.append(Updated(key, before, after, diff))
        
        return Changes(added, deleted, updated)
            

    