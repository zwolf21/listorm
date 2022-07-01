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


def diffkeys(dict1:dict, dict2:dict) -> list:
    return [
        key1
        for key1, value1 in dict1.items()
        for key2, value2 in dict2.items()
        if key1 == key2 and value1 != value2
    ]
    
