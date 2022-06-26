from .helper import _route_callable




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
        row[key] = _route_callable(app, row)
    return row


def asselect(dict:dict, keys:list=None, excludes:list=None) -> dict:
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


def setdefaults(row:dict, defaults:dict) -> dict:
    row = dict(row)
    for defkey, defval in defaults.items():
        if defkey not in row:
            row[defkey] = _route_callable(defval, row)
    return row


def diffkeys(dict1:dict, dict2:dict) -> list:
    return [
        key1
        for key1, value1 in dict1.items()
        for key2, value2 in dict2.items()
        if key1 == key2 and value1 != value2
    ]