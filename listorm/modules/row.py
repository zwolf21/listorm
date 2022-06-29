from ..exceptions import *
from ..utils import get_argcounts
from ..api import asselect, renamekeys, setdefaults, asvalues, addkeys, asmap



class Row(dict):

    __getattr__ = dict.get

    def normalize(self, common_columns:list[str], defaults:dict=None):
        row = setdefaults(self, common_columns, defaults)
        return Row(row)

    def rename(self, renames:dict):
        row = renamekeys(self, renames)
        return Row(row)
    
    def select(self, columns:list=None, excludes:list=None):
        row = asselect(self, columns, excludes=excludes)
        return Row(row)
    
    def drop(self, columns:list):
        row = asselect(self, excludes=columns)
        return Row(row)

    def addkeys(self, keymapset:dict):
        row = addkeys(self, keymapset)
        return Row(row)

    def map(self, keymapset:dict):
        return asmap(self, keymapset)
    
    def values(self, columns:list, **kwargs):
        return asvalues(self, columns, **kwargs)