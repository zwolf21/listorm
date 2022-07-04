from itertools import tee

from .asdict import *
from ..utils import reduce_args, reduce_kwargs, tuplize
from .helper import reduce_where



@reduce_args('keys')
def values(records:list[dict], keys:list, *, flat_one=True) -> list:
    return [
        asvalues(row, keys, flat=flat_one) for row in records
    ]


@reduce_args('keys')
def select(records:list[dict], keys:list, *, excludes:list=None, where:callable=None) -> list[dict]:
    return [
        asselect(row, keys, excludes=excludes) for row in records
        if reduce_where(row, where)
    ]


@reduce_kwargs('updatemap')
def update(records:list[dict], updatemap:dict=None, where:callable=None):
    return [
        asupdate(row, updatemap=updatemap) if reduce_where(row, where) else row
        for row in records
    ]


@reduce_kwargs('keymap')
def extend(records:list[dict], *, keymap:dict) -> list[dict]:
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


def join(left:list[dict], right:list[dict], on:tuple=None, left_on:tuple=None, right_on:tuple=None, how:str='inner') -> list[dict]:
    on, left_on, right_on = tuplize(on), tuplize(left_on), tuplize(right_on)

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
