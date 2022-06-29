from ..utils import reduce_kwargs, reduce_args, number_format
from ..api import values_count, write_excel




class ShortCutMixin:

    @property
    def exists(self):
        return len(self) != 0

    @property
    def first(self):
        if self: return self[0]
    
    @property
    def count(self):
        return len(self)

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
    def values_count(self, *columns:str):
        return values_count(self, columns)
    
    def to_excel(self, filename=None, sheet_name=None):
        return write_excel(self, filename, sheet_name=sheet_name, fill_miss=False)
