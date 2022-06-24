from heapq import nlargest, nsmallest
from collections import defaultdict, Counter


def asvalues(dict:dict, keys:list, exact:bool=True) -> object:
    result = tuple(
        dict[key] for key in keys if exact or key in dict
    )
    if len(result) == 1:
        return result[0]
    return result


def addkeys(dict:dict, keymapset:dict) -> dict:
    row = {k:v for k,v in dict.items()}
    for key, app in keymapset.items():
        if callable(app):
            row[key] = app(row)
        else:
            row[key] = app
    return row


def selectitem(dict:dict, keys:list=None, excludes:list=None) -> dict:
    keys = [
        key for key in (keys or dict.keys())
        if key not in (excludes or [])
    ]
    return {
        key:dict[key] for key in keys if key in dict
    }
    

def renamekeys(dict:dict, renames:dict) -> dict:
    return {
        renames.get(key, key): value
        for key, value in dict.items()
    }


def set_defaults(dict:dict, keys:list, defaults:dict, padding:object=None) -> dict:
    defaults = defaults or {}
    result = {}
    for key in keys:
        if key in dict:
            result[key] = dict[key]
        else:
            result[key] = defaults.get(key, padding)
    return result


def diffkeys(dict1:dict, dict2:dict):
    return [
        key1
        for key1, value1 in dict1.items()
        for key2, value2 in dict2.items()
        if key1 == key2 and value1 != value2
    ]
    

def values_list(records:list[dict], keys:list) -> list:
    return [
        asvalues(row, keys) for row in records
    ]


def select(records:list[dict], keys:list, excludes:list=None, where:callable=None) -> list[dict]:
    where = where or (lambda row: True)
    return [
        selectitem(row, keys, excludes) for row in records
        if where(row)
    ]

def extend(records:list[dict], keymapset:dict):
    return [
        addkeys(row, keymapset) for row in records
    ]


def extract_keys_from_records(records:list[dict]) -> list:
    collect = {
        key:None
        for row in records
        for key in row
    }
    return list(collect)


def sort(records:list[dict], sortkeys:list) -> list[dict]:
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


def distinct(records:list[dict], keys:list, fisrt:bool=True, singles:bool=False) -> list:
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


def asgroup(records:list[dict], keys:list, with_pos:bool=False) -> tuple[list, dict[str, list]]:
    grouped = {}
    for p, row in enumerate(records):
        values = asvalues(row, keys)    
        grouped.setdefault(values, []).append((p, row) if with_pos else row)
    return grouped


def aggregate(grouped:dict[str, list[dict]], keys:list, aggset:dict, aliases:dict=None, groupset_name:str=None) -> list[dict]:
    aliases = aliases or {}

    result = []
    for _, rows in grouped.items():
        agged = selectitem(rows[0], keys)
        for key, apply in aggset.items():
            values = values_list(rows, [key])
            agg = apply(values)
            alias = aliases.get(key, key)
            agged[alias] = agg
        if groupset_name:
            agged[groupset_name] = rows
        result.append(agged)
    return result
            

def groupby(records:list[dict], keys:list, aggset:dict, aliases:dict=None, groupset_name:str=None) -> list[dict]:
    grouped = asgroup(records, keys)
    agged = aggregate(grouped, keys, aggset, aliases, groupset_name)
    return agged


def product(records1:list[dict], records2:list[dict]):
    for row1 in records1:
        for row2 in records2:
            row = {}
            row.update(row1)
            row.update(row2)
            yield row


def set_index(records:list[dict], keys:list) -> list[tuple[tuple, dict]]:
    return [
        (asvalues(row, keys), row) for row in records
    ]


def join(left:list[dict], right:list[dict], left_on:tuple=None, right_on:tuple=None, how:str='inner') -> list[dict]:

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

    result = []
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
        result += rows
    return result


def top_or_bottom(records:list[dict], keys:list, n=1, top=True):
    if n < 1:
        index = round(len(records)*n)
    else:
        index = n
    rgest = nlargest if top else nsmallest
    result = list(rgest(index, records, key=lambda row: asvalues(row, keys)))
    if n == 1 and result:
        return result[0]
    return result


def values_count(records:list[dict], keys:list):
    return Counter(values_list(records, keys))    

