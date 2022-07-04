from .base import BaseList
from .shortcuts import ShortCutMixin
from ..exceptions import *
from ..api import *
from ..utils import reduce_args, reduce_kwargs, pluralize_params



class Listorm(ShortCutMixin, BaseList):

        
    def filter(self, where:callable):
        records = [
            row for row in self if reduce_where(row, where)
        ]
        return Listorm(
            records,
            uniques=self.uniques, fill_missed=False
        )

    @reduce_args('columns')
    def select(self, columns:list, *, excludes:list=None, where:callable=None):
        return Listorm(
            select(self, columns, excludes=excludes, where=where), 
            fill_missed=False
        )

    @reduce_args('columns')
    def drop_column(self, columns:list):
        return self.select(excludes=columns)
    
    @reduce_kwargs('keymap')
    def add_column(self, keymap:dict):
        return Listorm(
            extend(self, keymap=keymap),
            **self.as_kwargs(fill_missed=False)
        )

    @reduce_kwargs('renamemap')
    def rename(self, renamemap:dict):
        return Listorm(rename(self, renamemap=renamemap), fill_missed=False)

    @reduce_kwargs('updatemap')
    def update(self, updatemap:dict, *, where:callable):
        return Listorm(
            update(self, updatemap=updatemap, where=where),
            fill_missed=False
        )
    
    @reduce_args('columns')
    def values(self, columns:list, *, flat_one=True):
        return values(self, columns, flat_one=flat_one)

    @reduce_args('columns')
    def distinct(self, columns:list, *, keep_first:bool=True, singles:bool=False):
        return Listorm(distinct(self, columns, keep_first=keep_first, singles=singles), fill_missed=False)

    @reduce_args('sortkeys')
    def orderby(self, sortkeys:list):
        return Listorm(sort(self, sortkeys), **self.as_kwargs(fill_missed=False))

    @reduce_args('columns')
    @reduce_kwargs('aggset')
    def groupby(self, columns:list, *, aggset:dict, renames:dict=None, groupset_name:str=None):
        return Listorm(
            groupby(self, columns, aggset=aggset, renames=renames, groupset_name=groupset_name)
        )

    @pluralize_params('on', 'right_on')
    def join(self, other, on:None, right_on=None, how:str='inner'):
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

    



    