from .helper import reduce_callable, reduce_args_count
from ..utils import number_format, reduce_args, reduce_kwargs



def askeys(item:dict, excludes:list=None):
    """extract keys from item

    :param item: a dict object
    :param excludes: keys for excluded, defaults to None
    :return: a list contains keys of item


    .. doctest::

        >>> import listorm

        >>> item = {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}

        >>> listorm.askeys(item)
        ['name', 'gender', 'age', 'location']

        >>> listorm.askeys(item, excludes=['gender', 'age'])
        ['name', 'location']
    """
    excludes = excludes or []
    return [
        key for key in item if key not in excludes
    ]



@reduce_args
def asvalues(item:dict, *keys:str, exact:bool=True, flat=True):
    """extract values from item that matchs the order of keys

    :param item: a dict object
    :type item: dict
    :param keys: keys for retrive values
    :type keys: the arguments for keys or a list containing keys
    :param exact: if True, raise KeyError when key is not in item, defaults to True
    :type exact: bool, optional
    :param flat: When the return value is a single value, the value is returned without being included in the tuple, defaults to True
    :type flat: bool, optional
    :return: a tuple of contains values or a value
    :rtype: tuple, option


    .. doctest::

        >>> item = {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}

        >>> listorm.asvalues(item, 'name', 'gender')
        ('Smith', 'M')

        >>> listorm.asvalues(item, ['name', 'gender']) #  listify keys
        ('Smith', 'M')

        >>> listorm.asvalues(item, 'name') # unpacked when retriving single value
        'Smith'

        >>> listorm.asvalues(item, 'name', flat=False) # if flat=False, the sigle value is also packed as a tuple.
        ('Smith',)

    """
    keys = keys or askeys(item)
    result = tuple(
        item[key] for key in keys if exact or key in item
    )
    if flat and len(result) == 1:
        return result[0]
    return result

@reduce_args
def asselect(item:dict, *keys:str, excludes:list=None) -> dict:
    """select key, value pair from item

    :param item: a dict object
    :param keys: the arguments for keys or a list containing keys, if nothing, returns a new dict with the same key and value as the original item.
    :param excludes: keys for excluded, defaults to None
    :return: new dict item as selected


    .. doctest::


        >>> item = {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}

        >>> listorm.asselect(item, ['name', 'gender']) # keys arg as list
        {'name': 'Smith', 'gender': 'M'}

        >>> listorm.asselect(item, 'name', 'gender') # equal from above that keys as unpacked args
        {'name': 'Smith', 'gender': 'M'}

        >>> listorm.asselect(item) # pass a nothing of keys arg
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}

        >>> listorm.asselect(item, excludes=['gender']) # useful when need to drop item
        {'name': 'Smith', 'age': 17, 'location': 'USA'}

    """
    keys = keys or askeys(item)
    keys = [
        key for key in keys
        if key not in (excludes or [])
    ]
    return {
        key:item[key] for key in keys if key in item
    }
    
@reduce_args
def aslambda(callback, *keys, askwargs=False):
    """
    * reduce for callback and values in items as parameters
    * concise than using original lambda syntax
    * flexible implementation according to the parameters required by callback
    * It will be frequently used when using callback as an argument throughout this library.

    :param callback: Any callable function to apply at item
    :param keys: The key of the item value to pass as a callback args
    :param askwargs: If True, passing not only the value of the item but also the key value as kwargs , defaults to False
    :return: reduced as lambda function


    .. note::

        Examples of aslambda will appear in the examples of functions that take callbacks as arguments, which will be introduced belows

    """
    if askwargs:
        return lambda item: callback(**asselect(item, keys)) 
    return lambda item: callback(*asvalues(item, keys, flat=False))


@reduce_kwargs
def addkeys(item:dict, keymapset:dict=None, **keymapset__kwargs) -> dict:
    """extends item keys values via value or callback

    :param item: a dict object
    :param keymapset: key: value pair dict of items to be added
    :return: Expanded existing items


    .. doctest::


        >>> item = {'name': 'Smith', 'gender': 'M', 'age': 17}

        >>> listorm.addkeys(item, {'location': 'USA'})
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}

        >>> listorm.addkeys(item, location='USA') # also keymapset can converted into kwargs style
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
        
        # add key value via function
        >>> listorm.addkeys(item,
        ...    gender_age=lambda item: "{}/{}".format(item['gender'], item['age'])
        ... )
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'gender_age': 'M/17'}

        # Tricks with aslambda
        >>> from listorm import aslambda
        >>> listorm.addkeys(item,
        ...     gender_age=aslambda("{}/{}".format, 'gender', 'age')
        ... )
        {'name': 'Smith', 'gender': 'M', 'age': 17, 'gender_age': 'M/17'}

    """
    item = dict(item)
    for key, app in keymapset__kwargs.items():
        item[key] = reduce_callable(app, item)
    return item



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