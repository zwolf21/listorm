from ..api import read_excel as _read_execel
from .orm import Listorm



def read_excel(file=None, fields_contains:list=None, uniques=None, sheet_name=None, start_rows=0, start_cols=0):
    records = _read_execel(file, fields_contains, sheet_name, start_rows, start_cols)
    return Listorm(
        records, fill_missed=False, uniques=uniques
    )
