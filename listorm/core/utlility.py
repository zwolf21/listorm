from ..api import extensions
from .orm import Listorm



def read_excel(
    file=None,
    fields_contains:list=None, uniques=None,
    sheet_name=None, start_rows=0, start_cols=0,
    prettify_column_names=True,
):
    records = extensions.read_excel(
        file, fields_contains, sheet_name, start_rows, start_cols,
        prettify_column_names=prettify_column_names
    )
    return Listorm(
        records, fill_missed=False,
        uniques=uniques,
    )


def read_csv(file, encoding='utf-8', uniques=None, **csv_reader_kwargs):
    records = extensions.read_csv(file, encoding=encoding, **csv_reader_kwargs)
    return Listorm(
        records, fill_missed=False,
        uniques=uniques
    )