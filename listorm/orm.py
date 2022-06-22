from collections import UserList
from typing import Union

from .row import Row
from .exceptions  import *


def extract_fields(records:list[dict]) -> list:
    fields = set()
    for row in records:
        for key in row:
            fields.add(key)
    return list(fields)

def check_unique_constraint(records:list[dict], uniques:tuple) -> tuple:
    visited = set()
    for row in records:
        values = itemgetter(*uniques)(row)



class Listorm(UserList):

    def __init__(self, records:Union[list, UserList], uniques:Union[tuple, str]=None, fields:Union[list, tuple]=None):
        self.uniques = (uniques,) if isinstance(uniques, str) else uniques
        self.fields = fields
        if isinstance(records, (list, UserList)):
            self.fields = self.fields or extract_fields(records)
        elif isinstance(records, Listorm):
            self.fields = self.fields or records.fields
            self.uniques = self.uniques or records.uniques
        else:
            raise TypeError('records type Error')

        rows = [Row(row, fields=self.fields) for row in records]
        super().__init__(rows)
    
    def _check_uniques(self):
        visited = set()
        for row in self.data:
            values = row.values(*self)
            if values in visited:
                raise UniqueConstraintError
            visited.add(values)
    




        
