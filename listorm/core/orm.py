from .base import BaseList
from .shortcuts import ShortCutMixin
from ..exceptions import *
from ..api import sort, distinct, groupby, join, reduce_where
from ..utils import reduce_args, reduce_kwargs, tuplize



class Listorm(ShortCutMixin, BaseList):

        
    def filter(self, where:callable):
        where = reduce_where(where)
        return Listorm(
            filter(where, self),
            uniques=self.uniques, fill_missed=False
        )

    @reduce_args
    def select(self, *columns:str, excludes:list=None, where:callable=None):
        app = lambda row: row.select(columns, excludes)
        return Listorm(
            map(app, self.filter(where)), fill_missed=False
        )

    @reduce_args
    def drop_column(self, *columns:str):
        return self.select(excludes=columns)
    
    @reduce_kwargs
    def add_column(self, *column_mapset:dict, **column_map_kwargs):
        app = lambda row: row.addkeys(column_map_kwargs)
        return Listorm(
            map(app, self), **self.as_kwargs(fill_missed=False)
        )

    @reduce_kwargs
    def rename(self, *renamemap:dict, **rename_kwargs):
        app = lambda row: row.rename(rename_kwargs)
        return Listorm(map(app, self), fill_missed=False)

    @reduce_kwargs
    def update(self, *applymap:dict, where:callable=None, **apply_kwargs):
        where = reduce_where(where)
        app = lambda row: row.map(apply_kwargs) if where(row) else row      
        return Listorm(map(app, self), fill_missed=False)
    
    @reduce_args
    def values(self, *columns:str, flat_one=True):
        app = lambda row: row.values(columns, flat=flat_one)
        return list(map(app, self))

    @reduce_args
    def distinct(self, *columns:str, keep_first:bool=True, singles:bool=False):
        return Listorm(distinct(self, columns, keep_first=keep_first, singles=singles), fill_missed=False)

    @reduce_args
    def orderby(self, *sortkeys:list):
        return Listorm(sort(self, sortkeys), **self.as_kwargs(fill_missed=False))

    @reduce_args
    @reduce_kwargs
    def groupby(self, *columns:str, aggset:dict=None, renames:dict=None, groupset_name:str=None, **aggset_kwargs):
        aggset_kwargs.update(aggset or {})
        return Listorm(
            groupby(self, columns, aggset=aggset_kwargs, renames=renames, groupset_name=groupset_name)
        )

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
        return Listorm(
                join(self, other, None, on, right_on, how=how),
                fill_value=self.fill_value
            )

    



    