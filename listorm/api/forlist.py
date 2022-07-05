'''
Functional API for manipulating list contains dict items
========================================================
'''

from itertools import tee

from .asdict import *
from ..utils import reduce_args, reduce_kwargs, pluralize_params
from .helper import reduce_where



@reduce_args('keys')
def values(records:list[dict], keys:list, *, flat_one=True) -> list[tuple]:
    '''extract values list from records

    :param records: list contains dicts
    :param keys: keys for extracting values
    :param flat_one: When the return value is a single value, the value is returned without being included in the list, defaults to True
    :return: list contains tuple values


    .. doctest::
        
        >>> import listorm

        >>> userTable = [
        ...    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
        ...    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
        ...    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
        ...    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
        ...    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
        ...    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
        ...    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
        ... ]

        >>> records = listorm.values(userTable, 'name', 'gender', 'location')
        >>> for row in records: print(row)
        ('Hong', 'M', 'Korea')
        ('Charse', 'M', 'USA')
        ('Lyn', 'F', 'China')
        ('Xiaomi', 'M', 'China')
        ('Park', 'M', 'Korea')
        ('Smith', 'M', 'USA')
        ('Lee', 'F', 'Korea')

        >>> # When there is only one column, a flatten single list is returned
        >>> listorm.values(userTable, 'name')
        ['Hong', 'Charse', 'Lyn', 'Xiaomi', 'Park', 'Smith', 'Lee']

        >>> # but, flat_one = False when consistency is required
        >>> listorm.values(userTable, 'name', flat_one=False)
        [('Hong',), ('Charse',), ('Lyn',), ('Xiaomi',), ('Park',), ('Smith',), ('Lee',)]

    '''
    return [
        asvalues(row, keys, flat=flat_one) for row in records
    ]


@reduce_args('keys')
def select(records:list[dict], keys:list, *, excludes:list=None, where:callable=None) -> list[dict]:
    '''Retrieves the item of the specified item

    :param records: list contains dicts
    :param keys: keys for retrieves item
    :param excludes: keys for excluded, defaults to None
    :param where: record filtering callback 
    :return: list of selected and filtered as records


    .. doctest::

        >>> # Names of people over 20 years of name, age, location
        >>> records = listorm.select(userTable, ['name', 'age', 'location'], where=lambda age: age > 20)
        >>> for row in records: row
        {'name': 'Lyn', 'age': 28, 'location': 'China'}
        {'name': 'Park', 'age': 29, 'location': 'Korea'}

    '''
    return [
        asselect(row, keys, excludes=excludes) for row in records
        if reduce_where(row, where)
    ]


@reduce_kwargs('updatemap')
def update(records:list[dict], updatemap:dict=None, where:callable=None):
    '''update item values

    :param records: a list contains dicts
    :param updatemap: key:value|callable mapping for update values
    :param where: filter specifying what to update, defaults to None
    :return: list of updated items as records


    .. doctest::

        >>> # Increase the age of people in Korea and China by one
        >>> records = listorm.update(
        ...     userTable,
        ...     age=lambda age: age +1,
        ...     # or updatemap={'age': lambda age: age +1} 
        ...     where=lambda location: location.lower() in ['korea', 'china']
        ... )
        >>> for row in records: print(row)
        {'name': 'Hong', 'gender': 'M', 'age': 19, 'location': 'Korea'}
        {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'}
        {'name': 'Lyn', 'gender': 'F', 'age': 29, 'location': 'China'}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 16, 'location': 'China'}
        {'name': 'Park', 'gender': 'M', 'age': 30, 'location': 'Korea'}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
        {'name': 'Lee', 'gender': 'F', 'age': 13, 'location': 'Korea'}
 
        # applying value modifing functions
        >>> records = listorm.update(userTable,
        ...     # age=float, location=str.upper
        ...     updatemap={'age': float, 'location': str.upper} 
        ... )

        >>> for row in records: row
        {'name': 'Hong', 'gender': 'M', 'age': 18.0, 'location': 'KOREA'}
        {'name': 'Charse', 'gender': 'M', 'age': 19.0, 'location': 'USA'}
        {'name': 'Lyn', 'gender': 'F', 'age': 28.0, 'location': 'CHINA'}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15.0, 'location': 'CHINA'}
        {'name': 'Park', 'gender': 'M', 'age': 29.0, 'location': 'KOREA'}
        {'name': 'Smith', 'gender': 'M', 'age': 17.0, 'location': 'USA'}
        {'name': 'Lee', 'gender': 'F', 'age': 12.0, 'location': 'KOREA'}


    .. note::

        *packed* vs *unpacked* the two way of parameterization supported

        list for columns args and dict for mapping args can be converted into variable args or kwargs parameters in this library

        The following below examples will use the unpacked parameters 


        .. code-block::
            # unpacked args vs packed to list
            listorm.select(userTable, 'name', 'gender') == listorm.select(userTable, ['name', 'gender'])
        
        .. code-block::
            # unpacked kwargs vs packed to dict
            listorm.update(userTable, name=str.upper) == listorm.update(userTable, updatemap={'name': str.upper})

    '''
    return [
        asupdate(row, updatemap=updatemap) if reduce_where(row, where) else row
        for row in records
    ]


@reduce_kwargs('keymap')
def add_column(records:list[dict], *, keymap:dict) -> list[dict]:
    '''add keys to item in records

    :param records: a list contains dicts
    :param keymap: the value or function mapping required for key to be added
    :return: extended records


    '''

    return [
        addkeys(row, keymap=keymap) for row in records
    ]


@reduce_args('keys')
def drop(records:list[dict], keys:list) -> list:
    return select(records, excludes=keys)


@reduce_kwargs('renamemap')
def rename(records:list[dict], renamemap:dict) -> dict:
    return [
        asrename(row, renamemap=renamemap)
        for row in records   
    ]

def get_allkeys(records:list[dict]) -> list:
    keyset = {
        key:None
        for row in records
        for key in row
    }
    return list(keyset)


def fillmissed(records:list[dict], value=None):
    tee1, tee2 = tee(records, 2)
    fields = get_allkeys(tee1)
    defaults = dict.fromkeys(fields, value)
    return [
        asdefault(row, defaultmap=defaults) for row in tee2
    ]


def guess_type(records:list[dict], key:str):
    values = values(records, key)
    head, *_ = filter(None, values)
    return type(head)


@reduce_args('sortkeys')
def sort(records:list[dict], sortkeys:list) -> list[dict]:
    records = list(records)
    if not records:
        return records

    for keys in reversed(sortkeys):
        reverse = False
        if isinstance(keys, str):
            if keys.startswith('-'):
               keys = keys[1:]
               reverse = True
            records.sort(key=lambda x: x[keys], reverse=reverse)
        elif callable(keys):
            records.sort(key=keys)
    return records


@reduce_args('keys')
def distinct(records:list[dict], keys:list, *, keep_first:bool=True, singles:bool=False) -> list:
    if not keep_first:
        records = list(reversed(records))
    duplicates = {}
    for row in records:
        values = asvalues(row, keys)
        duplicates.setdefault(values, []).append(row)
    
    distincts = []
    for dct, rows in duplicates.items():
        if singles and len(rows) > 1:
            continue
        distincts.append(rows[0])
    
    if not keep_first:
        distincts = list(reversed(distincts))
    return distincts


def asgroup(records:list[dict], keys:list, with_pos:bool=False) -> tuple[list, dict[str, list]]:
    grouped = {}
    for p, row in enumerate(records):
        values = asvalues(row, keys)    
        grouped.setdefault(values, []).append((p, row) if with_pos else row)
    return grouped


def aggregate(grouped:dict[str, list[dict]], keys:list, aggset:dict, aliases:dict=None, groupset_name:str=None) -> list[dict]:
    aliases = aliases or {}
    aggregated = []
    for _, rows in grouped.items():
        agged = asselect(rows[0], keys)
        for key, apply in aggset.items():
            values_list = values(rows, [key])
            agg = apply(values_list)
            alias = aliases.get(key, key)
            agged[alias] = agg
        if groupset_name:
            agged[groupset_name] = rows
        aggregated.append(agged)
    return aggregated


@reduce_args('keys')
@reduce_kwargs('aggset')
def groupby(records:list[dict], keys:list, *, aggset:dict, renames:dict=None, groupset_name:str=None) -> list[dict]:
    grouped = asgroup(records, keys)
    agged = aggregate(grouped, keys, aggset, renames, groupset_name)
    return agged


def product(records1:list[dict], records2:list[dict]):
    for row1 in records1:
        for row2 in records2:
            row = {}
            row.update(row1)
            row.update(row2)
            yield row


@reduce_args('keys')
def set_index(records:list[dict], keys:list) -> list[tuple[tuple, dict]]:
    return [
        (asvalues(row, keys), row) for row in records
    ]

@pluralize_params('on', 'left_on', 'right_on')
def join(left:list[dict], right:list[dict], on:tuple=None, left_on:tuple=None, right_on:tuple=None, how:str='inner') -> list[dict]:

    if on:
        left_on = right_on = on
    elif not all([left_on, right_on]):
        raise ValueError('left_on and rignt_on must be specified')

    left_group = asgroup(left, left_on)
    right_group = asgroup(right, right_on)

    if how == 'left':
        joinkeys = left_group.keys()
    elif how == 'right':
        joinkeys = right_group.keys()
    elif how == 'inner':
        joinkeys = left_group.keys() & right_group.keys()
    elif how == 'outer':
        joinkeys = left_group.keys() | right_group.keys()
    else:
        raise ValueError

    joined = []
    for jkey in joinkeys:
        lrows = left_group.get(jkey, [{}])
        rrows = right_group.get(jkey, [{}])
        products = (
            (lrow, rrow)
            for lrow in lrows
            for rrow in rrows
        )
        rows = []
        for lrow, rrow in products:
            row = {}
            row.update(lrow)
            row.update(rrow)
            rows.append(row)
        joined += rows
    return joined


@reduce_args('keys')
def values_count(records:list[dict], keys:list):
    counter = {}
    for row in records:
        value = asvalues(row, keys)
        counter.setdefault(value, 0)
        counter[value] += 1   
    return counter


@reduce_kwargs('formats')
def set_number_format(records:list[dict], *, formats:dict=None):
    return [
        asnumformat(row, formats) for row in records
    ]

@reduce_args('keys')
def is_unique(records:list[dict], keys:list):
    counter = values_count(records, keys)
    return max(counter.values(), default=1) < 2
