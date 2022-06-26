from .dict import *
from ..utils import reduce_args, reduce_kwargs, tuplize



@reduce_args
def values(records:list[dict], *keys:str) -> list:
    return [
        asvalues(row, keys) for row in records
    ]


@reduce_args
def select(records:list[dict], *keys:str, excludes:list=None, where:callable=None) -> list[dict]:
    where = where or (lambda row: True)
    return [
        asselect(row, keys, excludes) for row in records
        if where(row)
    ]


@reduce_kwargs
def extend(records:list[dict], keymapset:dict, **keymapset_kwargs):
    return [
        addkeys(row, keymapset_kwargs) for row in records
    ]


def get_allkeys(records:list[dict]) -> list:
    keyset = {
        key:None
        for row in records
        for key in row
    }
    return list(keyset)


@reduce_args
def sort(records:list[dict], *sortkeys) -> list[dict]:
    records = list(records)
    if not records:
        return records

    for keys in reversed(sortkeys):
        print(keys)
        reverse = False
        if isinstance(keys, str):
            if keys.startswith('-'):
               keys = keys[1:]
               reverse = True
            records.sort(key=lambda x: x[keys], reverse=reverse)
        elif callable(keys):
            records.sort(key=keys)
    return records


@reduce_args
def distinct(records:list[dict], *keys:str, fisrt:bool=True, singles:bool=False) -> list:
    if not fisrt:
        records = reversed(records)
    duplicates = {}
    for row in records:
        values = asvalues(row, keys)
        duplicates.setdefault(values, []).append(row)
    
    distincts = []
    for dct, rows in duplicates.items():
        if singles and len(rows) > 1:
            continue
        distincts.append(rows[0])
    
    if not fisrt:
        distincts = reversed(distincts)
    return distincts


@reduce_args
def asgroup(records:list[dict], *keys:list, with_pos:bool=False) -> tuple[list, dict[str, list]]:
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
            values = values(rows, [key])
            agg = apply(values)
            alias = aliases.get(key, key)
            agged[alias] = agg
        if groupset_name:
            agged[groupset_name] = rows
        aggregated.append(agged)
    return aggregated


@reduce_args
@reduce_kwargs
def groupby(records:list[dict], *keys:str, aggset:dict, aliases:dict=None, groupset_name:str=None, **aggset_kwargs) -> list[dict]:
    grouped = asgroup(records, keys)
    agged = aggregate(grouped, keys, aggset_kwargs, aliases, groupset_name)
    return agged


def product(records1:list[dict], records2:list[dict]):
    for row1 in records1:
        for row2 in records2:
            row = {}
            row.update(row1)
            row.update(row2)
            yield row


@reduce_args
def set_index(records:list[dict], *keys:str) -> list[tuple[tuple, dict]]:
    return [
        (asvalues(row, keys), row) for row in records
    ]


def join(left:list[dict], right:list[dict], left_on:tuple, right_on:tuple, how:str='inner') -> list[dict]:
    left_on, right_on = tuplize(left_on), tuplize(right_on)

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


@reduce_args
def values_count(records:list[dict], *keys:str):
    counter = {}
    for row in records:
        value = asvalues(row, keys)
        counter.setdefault(value, 0)
        counter[value] += 1   
    return counter