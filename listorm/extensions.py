from heapq import nlargest, nsmallest

from .utils import reduce_kwargs, reduce_args, number_format
from .api import set_index, top_or_bottom, values_count




class ExtensionMixin:

    @property
    def exists(self):
        return len(self) != 0

    @property
    def first(self):
        if self: return self[0]

    @property
    def last(self):
        if self: return self[-1]

    def max(self, column:str):
        values = filter(None, self.values(column))
        return max(values)

    def min(self, column:str):
        values = filter(None, self.values(column))
        return min(values)
    
    @reduce_kwargs
    def set_number_type(self, *formats:dict, **formats_kwargs):
        '''set_number_format(A=0.0, B=0, C='0'), change number type to default value(if failed, example values are applied to default)
            A: '123' => 123.0, B: 123.2 => 123, C: 123.1 => '123.1' 
        '''
        kwargs = {
            column:lambda v: number_format(v, fmt) 
            for column, fmt in formats_kwargs.items()
        }
        return self.update(kwargs, pass_undefined=False)
    
    @reduce_args
    def top(self, *columns:str, n:int=1):
        return top_or_bottom(self, columns, n, top=True)

    @reduce_args
    def bottom(self, *columns:str, n:int=1):
        return top_or_bottom(self, columns, n, top=False)

    @reduce_args
    def values_count(self, *columns:str):
        return values_count(self, columns)