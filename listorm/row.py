from collections import UserDict

from .exceptions import *
from .utils import  Undefined, get_argcounts
from .api import selectitem, renamekeys, set_defaults, asvalues, addkeys



class Row(UserDict):

    __getattr__ = UserDict.get

    def normalize(self, common_columns:list[str], defaults:dict=None):
        row = set_defaults(self, common_columns, defaults, Undefined())
        return Row(row)

    def rename(self, renames:dict):
        row = renamekeys(self, renames)
        return Row(row)
    
    def select(self, columns:list=None, excludes:list=None):
        row = selectitem(self, columns, excludes=excludes)
        return Row(row)
    
    def drop(self, columns:list):
        row = selectitem(self, excludes=columns)
        return Row(row)

    def addkeys(self, keymapset:dict):
        row = addkeys(self, keymapset)
        return Row(row)

    def map(self, keymapset:dict):
        applied = {}
        for key, app in keymapset.items():
            value = self[key]
            if isinstance(value, Undefined):
                continue
            if callable(app):
                if get_argcounts(app) == 1:
                    result = app(self[key])
                elif get_argcounts(app) == 2:
                    result = app(self[key], self)
                else:
                    raise ApplyFunctionArgumentCountError(app)
            else:
                result = app
            applied[key] = result
        row = selectitem(self)
        row.update(applied)
        return Row(row)
    
    def values(self, columns:list):
        return asvalues(self, columns)
        
