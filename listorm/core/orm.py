'''
Class Based API as wrapper class
--------------------------------
'''


from .base import BaseList
from .shortcuts import ShortCutMixin
from ..exceptions import *
from ..api import *
from ..utils import reduce_args, reduce_kwargs, pluralize_params



class Listorm(ShortCutMixin, BaseList):
    '''Wrapper class for list api

    :param ShortCutMixin: test
    :param BaseList: test
    '''

        
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
        '''Retrieves the item of the specified item

        :param columns: keys for selecting columns
        :param excludes: keys for excluding columns, defaults to None
        :param where: callback for filtering records, defaults to None
        :return: selected and filtered records as Listorm objects

        
        .. doctest::

            >>> from listorm import Listorm
            >>> userTable = [
            ...    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
            ...    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
            ...    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
            ...    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
            ...    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
            ...    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
            ...    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
            ... ]

            ls = Listorm(userTable)
            ls.select('name', 'age', 'location', where=lambda age: age > 20).print()
            {'name': 'Lyn', 'age': 28, 'location': 'China'}
            {'name': 'Park', 'age': 29, 'location': 'Korea'}


        '''
        return Listorm(
            select(self, columns, excludes=excludes, where=where), 
            fill_missed=False
        )

    @reduce_args('columns')
    def drop_column(self, columns:list):
        '''delete columns

        :param columns: column name for delete
        :return: Listorm object
        '''
        return self.select(excludes=columns)
    
    @reduce_kwargs('keymap')
    def add_column(self, keymap:dict):
        '''extend row as new columns

        :param keymap: new column: function mapping
        :return: Listorm

        
        .. doctest::
            >>> ls = Listorm(userTable)
            >>> ls.add_column(
            ...    summary=lambda name, gender, age: f"{name}/{gender}/{age}"
            ... ).print()
            {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'summary': 'Hong/M/18'}
            {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'summary': 'Charse/M/19'}
            {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'summary': 'Lyn/F/28'}
            {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'summary': 'Xiaomi/M/15'}
            {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'summary': 'Park/M/29'}
            {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'summary': 'Smith/M/17'}
            {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'summary': 'Lee/F/12'}

        '''
        return Listorm(
            add_column(self, keymap=keymap),
            **self.as_kwargs(fill_missed=False)
        )

    @reduce_kwargs('renamemap')
    def rename(self, renamemap:dict):
        return Listorm(rename(self, renamemap=renamemap), fill_missed=False)

    @reduce_kwargs('updatemap')
    def update(self, updatemap:dict, *, where:callable=None):
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
        return Listorm(orderby(self, sortkeys), **self.as_kwargs(fill_missed=False))

    @reduce_args('columns')
    @reduce_kwargs('aggset')
    def groupby(self, columns:list, *, aggset:dict, renames:dict=None, groupset_name:str=None):
        return Listorm(
            groupby(self, columns, aggset=aggset, renames=renames, groupset_name=groupset_name)
        )

    @pluralize_params('left_on', 'right_on')
    def join(self, other, left_on:None, right_on=None, how:str='inner'):
        left_on = left_on or self.uniques        
        
        if not right_on:
            if isinstance(other, Listorm):
                right_on = other.uniques or left_on
            else:
                right_on = left_on
        if not all((left_on, right_on)):
            raise JoinKeyDoesNotExists('on:{}, right_on:{} must be specified'.format(left_on, right_on))
        return Listorm(
                join(self, other, None, left_on, right_on, how=how),
                fill_value=self.fill_value
            )

    



    