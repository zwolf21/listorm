'''
Functional API for list as records
----------------------------------
'''

from itertools import tee
from collections import abc

from .asdict import *
from ..utils import reduce_args, reduce_kwargs, pluralize_params
from .helper import reduce_where



@reduce_args('keys')
def values(records:list[dict], keys:list, *, flat_one=True) -> list[tuple]:
    '''extract values list from records

    :param records: a list contains dict items
    :param keys: keys for extracting values
    :param flat_one: If True, when the return value is a single value, the value is returned without being included in the list, defaults to True
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

    :param records: a list contains dict items
    :param keys: keys for selecting item
    :param excludes: keys for excluded, defaults to None
    :param where: callback for filtering records
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

    :param records: a list contains dict items
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

        The following below examples will use the unpacked parameters, or if unpacked is not available, you will see it used in packed form.


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

    :param records: a list contains dict items
    :param keymap: the value or function mapping required for key to be added
    :return: extended records


    .. doctest::

        >>> # Create a new column using the other two columns
        >>> records = listorm.add_column(userTable, 
        ...     keymap={'gender/age': lambda gender, age: "{}/{}".format(gender, age)}
        ... )
        >>> for row in records: row
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'gender/age': 'M/18'}
        {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'gender/age': 'M/19'}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'gender/age': 'F/28'}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'gender/age': 'M/15'}
        {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'gender/age': 'M/29'}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'gender/age': 'M/17'}
        {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'gender/age': 'F/12'}

    .. note::
        As above, if a slash or space is included in the column name, unpacked paramater is not allowed


        .. code-block::

            # due to / is not allowed to using as parameter name, this cannot be valid code
            add_column(userTable, gender/age=lambda gender, age: "{}/{}".format(gender, age))
    
    '''

    return [
        addkeys(row, keymap=keymap) for row in records
    ]


@reduce_args('keys')
def drop(records:list[dict], keys:list) -> list:
    '''delete key from the items in records

    :param records: a list contains dict items
    :param keys: keys for to delete
    :return: list what contains deleted items as records


    .. doctest::

        >>> records = listorm.drop(userTable, 'age', 'gender')
        >>> for row in records: row
        {'name': 'Hong', 'location': 'Korea'}
        {'name': 'Charse', 'location': 'USA'}
        {'name': 'Lyn', 'location': 'China'}
        {'name': 'Xiaomi', 'location': 'China'}
        {'name': 'Park', 'location': 'Korea'}
        {'name': 'Smith', 'location': 'USA'}
        {'name': 'Lee', 'location': 'Korea'}

    .. note::

        using by select and excludes parameter, can retrive same results


        .. code-block::

            listorm.select(userTable, excludes=['age', 'gender'])

    '''
    return select(records, excludes=keys)


@reduce_kwargs('renamemap')
def rename(records:list[dict], renamemap:dict) -> dict:
    '''change key of items in records as to another name

    :param records: a list contains dict items
    :param renamemap: old: new key mapping dict
    :return: list what contains renamed items as records


    .. doctest::

        >>> records = listorm.rename(userTable, gender='sex', location='country')
        >>> for row in records: row
        {'name': 'Hong', 'sex': 'M', 'age': 18, 'country': 'Korea'}
        {'name': 'Charse', 'sex': 'M', 'age': 19, 'country': 'USA'}
        {'name': 'Lyn', 'sex': 'F', 'age': 28, 'country': 'China'}
        {'name': 'Xiaomi', 'sex': 'M', 'age': 15, 'country': 'China'}
        {'name': 'Park', 'sex': 'M', 'age': 29, 'country': 'Korea'}
        {'name': 'Smith', 'sex': 'M', 'age': 17, 'country': 'USA'}
        {'name': 'Lee', 'sex': 'F', 'age': 12, 'country': 'Korea'}

        >>> # if key name has to be containing spaces
        >>> records = listorm.rename(userTable, renamemap={'age': 'age of ultron' })
        >>> for row in records: row
        {'name': 'Hong', 'gender': 'M', 'age of ultron': 18, 'location': 'Korea'}
        {'name': 'Charse', 'gender': 'M', 'age of ultron': 19, 'location': 'USA'}
        {'name': 'Lyn', 'gender': 'F', 'age of ultron': 28, 'location': 'China'}
        {'name': 'Xiaomi', 'gender': 'M', 'age of ultron': 15, 'location': 'China'}
        {'name': 'Park', 'gender': 'M', 'age of ultron': 29, 'location': 'Korea'}
        {'name': 'Smith', 'gender': 'M', 'age of ultron': 17, 'location': 'USA'}
        {'name': 'Lee', 'gender': 'F', 'age of ultron': 12, 'location': 'Korea'}

        .. note::

            In newer versions of python, the order of key occurence in dict is valid

    '''
    return [
        asrename(row, renamemap=renamemap)
        for row in records   
    ]

def get_allkeys(records:list[dict]) -> list:
    '''extract the occurance keys

    :param records: a list contains dict items
    :return: a list of key occurance


    .. doctest::

        >>> arecords = [
        ...    {'name': 'Hong', 'gender': 'M'},
        ...    {'name': 'Xiaomi', 'location': 'China'}
        ... ]

        >>> listorm.get_allkeys(arecords)
        ['name', 'gender', 'location']
    

    '''
    keyset = {
        key:None
        for row in records
        for key in row
    }
    return list(keyset)


def fillmissed(records:list[dict], value=None):
    '''fill missing key as default value for normalizing records

    :param records: a list contains dict items
    :param value: default value if item has missing key, defaults to None
    :return: a records that filled with default values


    .. doctest::

        >>> userTable_with_missing_values = [
        ...     {'age': 18, 'location': 'Korea'},
        ...     {'name': 'Charse', 'gender': 'M', 'location': 'USA'},
        ...     {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
        ...     {'name': 'Xiaomi', },
        ...     {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
        ...     {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
        ...     {'location': 'Korea'},
        ... ]

        >>> # as default, missing values are filled with None
        >>> records = listorm.fillmissed(userTable_with_missing_values)
        >>> for row in records: row
        {'age': 18, 'location': 'Korea', 'name': None, 'gender': None}
        {'name': 'Charse', 'gender': 'M', 'location': 'USA', 'age': None}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
        {'name': 'Xiaomi', 'age': None, 'location': None, 'gender': None}
        {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
        {'location': 'Korea', 'age': None, 'name': None, 'gender': None}

        >>> # or filled with 'undefined'
        >>> records = listorm.fillmissed(userTable_with_missing_values, 'undefined')
        >>> for row in records: row
        {'age': 18, 'location': 'Korea', 'name': 'undefined', 'gender': 'undefined'}
        {'name': 'Charse', 'gender': 'M', 'location': 'USA', 'age': 'undefined'}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
        {'name': 'Xiaomi', 'age': 'undefined', 'location': 'undefined', 'gender': 'undefined'}
        {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
        {'location': 'Korea', 'age': 'undefined', 'name': 'undefined', 'gender': 'undefined'}

        >>> # rearrange key order as same as original userTable by using select
        >>> records = listorm.select(records, listorm.get_allkeys(userTable))
        >>> for row in records: row
        {'name': 'undefined', 'gender': 'undefined', 'age': 18, 'location': 'Korea'}
        {'name': 'Charse', 'gender': 'M', 'age': 'undefined', 'location': 'USA'}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
        {'name': 'Xiaomi', 'gender': 'undefined', 'age': 'undefined', 'location': 'undefined'}
        {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
        {'name': 'undefined', 'gender': 'undefined', 'age': 'undefined', 'location': 'Korea'}

    '''

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
def orderby(records:list[dict], sortkeys:list) -> list[dict]:
    '''sort items in records

    :param records: a list of dict items
    :param sortkeys: key for sorting
    :return: sorted records


    .. doctest::


    >>> # complex key sorting: location as ascending and by age decending
    >>> records = listorm.orderby(userTable, 'location', '-age')
    >>> for row in records: row
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'}
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'}
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'}
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'}
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}

    >>> # ordering by callback
    >>> # order by first digit of age
    >>> records = listorm.orderby(userTable, lambda age: str(age)[-1])
    >>> for row in records: row
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'}
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'}
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'}
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'}
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}


    .. note::

        If you are familiar with django it looks like it

    '''
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
            records.sort(key=lambda row: reduce_callback(row, app=keys))
    return records


@reduce_args('keys')
def distinct(records:list[dict], keys:list, *, keep_first:bool=True, singles:bool=False) -> list:
    '''remove duplicate item by values for keys 

    :param records: a list contains dict items
    :param keys: key, check for duplicated values
    :param keep_first: if True In case of duplicate occurrence select the first item that appears, else last
    :param singles: if True eliminate duplicated items. That is, only items that were unique are left. defaults to False
    :return: distincted records


    .. doctest::
    
        >>> buyTable = [
        ...     {'name': 'Xiaomi', 'product': 'battery', 'amount':7},
        ...     {'name': 'Hong', 'product': 'keyboard', 'amount':1},
        ...     {'name': 'Lyn', 'product': 'cleaner', 'amount':5},
        ...     {'name': 'Hong', 'product': 'monitor', 'amount':1},
        ...     {'name': 'Hong', 'product': 'mouse', 'amount':3},
        ...     {'name': 'Lyn', 'product': 'mouse', 'amount':1},
        ...     {'name': 'Unknown', 'product': 'keyboard', 'amount':1},
        ...     {'name': 'Lee', 'product': 'hardcase', 'amount':2},
        ...     {'name': 'Lee', 'product': 'keycover', 'amount':2},
        ...     {'name': 'Yuki', 'product': 'manual', 'amount':1},
        ...     {'name': 'Xiaomi', 'product': 'cable', 'amount':1},
        ...     {'name': 'anonymous', 'product': 'adopter', 'amount':2},
        ...     {'name': 'Park', 'product': 'battery', 'amount':2},
        ...     {'name': 'Hong', 'product': 'cleaner', 'amount':3},
        ...     {'name': 'Smith', 'product': 'mouse', 'amount':1},
        ... ]

        >>> # maintains the existing item order if keep_first is True
        >>> records = listorm.distinct(buyTable, 'name')
        >>> for row in records: row
        {'name': 'Xiaomi', 'product': 'battery', 'amount': 7}
        {'name': 'Hong', 'product': 'keyboard', 'amount': 1}
        {'name': 'Lyn', 'product': 'cleaner', 'amount': 5}
        {'name': 'Unknown', 'product': 'keyboard', 'amount': 1}
        {'name': 'Lee', 'product': 'hardcase', 'amount': 2}
        {'name': 'Yuki', 'product': 'manual', 'amount': 1}
        {'name': 'anonymous', 'product': 'adopter', 'amount': 2}
        {'name': 'Park', 'product': 'battery', 'amount': 2}
        {'name': 'Smith', 'product': 'mouse', 'amount': 1}

        # retrive duplicated items occured at last if keep_first is False
        >>> records = listorm.distinct(buyTable, 'name', keep_first=False)
        >>> for row in records: row
        {'name': 'Lyn', 'product': 'mouse', 'amount': 1}
        {'name': 'Unknown', 'product': 'keyboard', 'amount': 1}
        {'name': 'Lee', 'product': 'keycover', 'amount': 2}
        {'name': 'Yuki', 'product': 'manual', 'amount': 1}
        {'name': 'Xiaomi', 'product': 'cable', 'amount': 1}
        {'name': 'anonymous', 'product': 'adopter', 'amount': 2}
        {'name': 'Park', 'product': 'battery', 'amount': 2}
        {'name': 'Hong', 'product': 'cleaner', 'amount': 3}
        {'name': 'Smith', 'product': 'mouse', 'amount': 1}

        # distinct by unique together by name, amount
        >>> records = listorm.distinct(buyTable, 'name', 'amount')
        >>> for row in records: row
        {'name': 'Xiaomi', 'product': 'battery', 'amount': 7}
        {'name': 'Hong', 'product': 'keyboard', 'amount': 1}
        {'name': 'Lyn', 'product': 'cleaner', 'amount': 5}
        {'name': 'Hong', 'product': 'mouse', 'amount': 3}
        {'name': 'Lyn', 'product': 'mouse', 'amount': 1}
        {'name': 'Unknown', 'product': 'keyboard', 'amount': 1}
        {'name': 'Lee', 'product': 'hardcase', 'amount': 2}
        {'name': 'Yuki', 'product': 'manual', 'amount': 1}
        {'name': 'Xiaomi', 'product': 'cable', 'amount': 1}
        {'name': 'anonymous', 'product': 'adopter', 'amount': 2}
        {'name': 'Park', 'product': 'battery', 'amount': 2}
        {'name': 'Smith', 'product': 'mouse', 'amount': 1}

        >>> # if singles is True, retrive the item only the name exist once
        >>> records = listorm.distinct(buyTable, 'name', singles=True)
        >>> for row in records: row
        {'name': 'Unknown', 'product': 'keyboard', 'amount': 1}
        {'name': 'Yuki', 'product': 'manual', 'amount': 1}
        {'name': 'anonymous', 'product': 'adopter', 'amount': 2}
        {'name': 'Park', 'product': 'battery', 'amount': 2}
        {'name': 'Smith', 'product': 'mouse', 'amount': 1}


    .. note::

        * distinct applies not only to records but also to lists with general values
        * Also removes duplicates while preserving order


        .. doctest::

            >>> dup_numbers = [1,1,2,3,3,4,4,5,5,5,6,7,7,7,8,9]
            >>> listorm.distinct(dup_numbers)
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> listorm.distinct(dup_numbers, singles=True)
            [2, 6, 8, 9]

            >>> fruitbasket = [
            ...   'apple', 'apple', 'banana', 'cherry', 'cherry', 'cherry', 'mango', 'orange', 'orange', 'grape', 'kiwi', 'kiwi'
            ... ]
            >>> listorm.distinct(fruitbasket)
            ['apple', 'banana', 'cherry', 'mango', 'orange', 'grape', 'kiwi']
            >>> listorm.distinct(fruitbasket, singles=True)
            ['banana', 'mango', 'grape']


    '''
    if not keep_first:
        records = list(reversed(records))
    duplicates = {}
    for row in records:
        if isinstance(row, abc.Mapping):
            values = asvalues(row, keys)
        else:
            values = row
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
    '''grouping by keys and aggregate values

    :param records: a list of dict items
    :param keys: keys for grouping
    :param aggset: aggregate key: function map
    :param renames: the name of aggregated key, if None, as original keyname, default None
    :param groupset_name: if specified, grouped items are dangling, default None
    :return: newly aggregated records


    .. doctest::

        >>> # get gender numbers by location
        >>> grouped = listorm.groupby(userTable,
        ...     'location', 'gender', #1. grouping
        ...      gender=len,  #2 caclulating
        ...      renames={'gender': 'gender_count'} #3 retriving as other keyname
        ... )
        >>> for row in grouped: row
        {'location': 'Korea', 'gender': 'M', 'gender_count': 2}
        {'location': 'USA', 'gender': 'M', 'gender_count': 2}
        {'location': 'China', 'gender': 'F', 'gender_count': 1}
        {'location': 'China', 'gender': 'M', 'gender_count': 1}
        {'location': 'Korea', 'gender': 'F', 'gender_count': 1}

        >>> # get average of age by gender
        >>> def calc_average_age(values):
        ...     return sum(values) / len(values)
        >>> grouped = listorm.groupby(userTable,
        ...   'gender',
        ...   age=calc_average_age,
        ...   renames={'age': 'age_avg'}
        ... )
        >>> grouped
        [{'gender': 'M', 'age_avg': 19.6}, {'gender': 'F', 'age_avg': 20.0}]

        >>> # simplify to values
        >>> listorm.values(grouped)
        [('M', 19.6), ('F', 20.0)]


        .. note::
            
            Although groupby's parameterizing is rather complicated, tt is largely divided into three parts.
            * keys
            * aggregation
            * renaming for retrieve aggregation

    '''
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
    '''merge two records

    :param left: a records
    :param right: another records
    :param on: when the field name of the key to join is the same, specify on, defaluts to None
    :param left_on: keys for join on left side records
    :param right_on: keys for join on right side records
    :param how: 'innder', 'left', 'right', 'outer', defaults to 'inner'
    :return: new merged records


    .. doctest::

        >>> # inner join by name
        >>> records = listorm.join(userTable, buyTable, on='name')
        >>> for row in records: row
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'cleaner', 'amount': 3}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'battery', 'amount': 7}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'cable', 'amount': 1}
        {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'product': 'battery', 'amount': 2}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'product': 'mouse', 'amount': 1}
        {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'hardcase', 'amount': 2}
        {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'keycover', 'amount': 2}

        >>> # left join, Charse has no buy item
        >>> records = listorm.join(userTable, buyTable, on='name', how='left')
        >>> for row in records: row
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'cleaner', 'amount': 3}
        {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'battery', 'amount': 7}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'cable', 'amount': 1}
        {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'product': 'battery', 'amount': 2}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'product': 'mouse', 'amount': 1}
        {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'hardcase', 'amount': 2}
        {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'keycover', 'amount': 2}

        >>> # merged records has missing values so filled missing as None
        >>> for row in listorm.fillmissed(records): row
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3}
        {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'cleaner', 'amount': 3}
        {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'product': None, 'amount': None}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5}
        {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'battery', 'amount': 7}
        {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'cable', 'amount': 1}
        {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'product': 'battery', 'amount': 2}
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'product': 'mouse', 'amount': 1}
        {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'hardcase', 'amount': 2}
        {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'keycover', 'amount': 2}


    '''
    if on:
        left_on = right_on = on
    elif not all([left_on, right_on]):
        raise ValueError('left_on and rignt_on must be specified')

    left_group = asgroup(left, left_on)
    right_group = asgroup(right, right_on)

    leftset = left_group.keys()
    rightset = right_group.keys()
    intersection = leftset & rightset

    leftkeys = [key for key in left_group if key in leftset]
    rightkeys = [key for key in right_group if key in rightset]
    unionkeys = distinct(leftkeys+rightkeys)

    if how == 'left':
        joinkeys = leftkeys
    elif how == 'right':
        joinkeys = rightkeys
    elif how == 'inner':
        joinkeys = [key for key in unionkeys if key in intersection]
    elif how == 'outer':
        joinkeys = unionkeys
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
    '''get values count by keys

    :param records: a list contains dict items
    :param keys: key for counted values
    :return: dict has values count


    .. doctest::

        >>> listorm.values_count(buyTable, 'product')
        {'battery': 2, 'keyboard': 2, 'cleaner': 2, 'monitor': 1, 'mouse': 3, 'hardcase': 1, 'keycover': 1, 'manual': 1, 'cable': 1, 'adopter': 1}

    '''

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
