from collections import UserDict
from operator import itemgetter

from .utils import reduce_kwargs, reduce_args, Undefined, get_argcounts
from .exceptions import *


class Row(UserDict):

    def __init__(self, *args, fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fields:
            self.arrange(fields)

    def _items(self):
        yield from self.data.items()

    def arrange(self, fields:list[str]):
        self.data = {
           f:self.data[f] if f in self.data else Undefined()
           for f in fields 
        }
        return self

    @reduce_kwargs
    def rename(self, *args:dict, **kwargs):
        self.data = {
            kwargs.get(key, key): value
            for key, value in self._items()
        }
        return self
    
    @reduce_args
    def select(self, *columns:str, excludes:list=None):
        columns = columns or self.data.keys()
        excludes = excludes or []
        self.data = {
            col:self.data[col] for col in columns
            if col not in excludes
        }
        return self
    
    @reduce_args
    def drop(self, *columns):
        self.data = {
            key: value for key, value in self._items()
            if key not in columns
        }
        return self

    @reduce_kwargs
    def map(self, *args, **kwargs):
        applied = {}
        for key, app in kwargs.items():
            value = self.data[key]
            if isinstance(value, Undefined):
                continue
            if callable(app):
                if get_argcounts(app) == 1:
                    result = app(self.data[key])
                elif get_argcounts(app) == 2:
                    result = app(self.data[key], self.data)
                else:
                    raise ApplyFunctionArgumentCountError(app)
            else:
                result = app
            applied[key] = result
        self.data.update(applied)
        return self
    
    @reduce_args
    def values(self, *columns, **kwargs):
        return itemgetter(*columns)(self.data)
        
