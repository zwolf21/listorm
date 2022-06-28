from .base import *




class Listorm(ListBase):

    
    @reduce_args
    def select(self, *columns, where:callable=None):
        records = select(self, columns, where=where)
        if set(self.uniques) & set(columns):
            return Listorm(records)
        return Listorm(records, self.uniques)
    