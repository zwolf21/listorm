from .helper import reduce_callable, reduce_args_count
from ..utils import number_format, reduce_args, reduce_kwargs



def askeys(dict:dict, excludes:list=None):
    excludes = excludes or []
    return [
        key for key in dict if key not in excludes
    ]


@reduce_args
def asvalues(dict:dict, *keys:str, exact:bool=True, flat=True) -> object:
    keys = keys or askeys(dict)
    result = tuple(
        dict[key] for key in keys if exact or key in dict
    )
    if flat and len(result) == 1:
        return result[0]
    return result


@reduce_kwargs
def addkeys(dict:dict, keymapset:dict, **keymapset__kwargs) -> dict:
    for key, app in keymapset__kwargs.items():
        dict[key] = reduce_callable(app, dict)
    return dict


@reduce_args
def asselect(dict:dict, *keys:str, excludes:list=None) -> dict:
    keys = [
        key for key in (keys or dict.keys())
        if key not in (excludes or [])
    ]
    return {
        key:dict[key] for key in keys if key in dict
    }
    

@reduce_kwargs
def asrename(dict:dict, renamemap:dict, **renamemap_kwargs) -> dict:
    return {
        renamemap_kwargs.get(key, key): value
        for key, value in dict.items()
    }

@reduce_kwargs
def setdefaults(row:dict, defaults:dict, **defaults_kwargs) -> dict:
    row = dict(row)
    for defkey, defval in defaults_kwargs.items():
        if defkey not in row:
            row[defkey] = reduce_callable(defval, row)
    return row


def diffkeys(dict1:dict, dict2:dict) -> list:
    return [
        key1
        for key1, value1 in dict1.items()
        for key2, value2 in dict2.items()
        if key1 == key2 and value1 != value2
    ]


def asnumformat(dict:dict, examples:dict):
    return {
        key: number_format(value, examples.get(key))
        for key, value in dict.items()
    }

@reduce_kwargs
def asmap(dict:dict, keymap:dict, **keymap_kwargs):
    applied = {} 
    for key, value in dict.items():
        app = keymap_kwargs.get(key)
        if not app:
            applied[key] = value
            continue
        app = keymap_kwargs[key]
        applied[key] = reduce_args_count(app, value, dict)
    return applied