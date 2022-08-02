import csv
from typing import List, Dict, Text, Tuple

from ..records import get_allkeys, merge
from .io import get_stringio, reduce_csv_input
from ...utils import pluralize_params



def read_csv(file, encoding='utf-8', fields:List=None, **csv_kwargs):
    fp = reduce_csv_input(file, encoding=encoding)
    csv_reader = csv.reader(fp, **csv_kwargs)
    fields = fields or next(csv_reader)
    result = [dict(zip(fields, map(str, row))) for row in csv_reader]
    return result


def write_csv(records:List[Dict], filename=None, fields=None, encoding='utf-8', lineterminator='\n', **csv_kwargs):
    output = get_stringio()
    fields = fields or get_allkeys(records)
    writer = csv.DictWriter(output, fields, lineterminator=lineterminator, **csv_kwargs)
    writer.writeheader()
    for row in records:
        writer.writerow(row)
    if filename:
        with open(filename, 'w', encoding=encoding) as fp:
            fp.write(output.getvalue())
    else:
        return output.getvalue()


@pluralize_params('uniques')
def merge2csv(csv, records:List[Dict], uniques:Tuple[Text], mode='create', append=False, **kwargs):
    rows = read_csv(csv, **kwargs)
    merged = merge(rows, records, uniques, mode=mode, append=append)
    return write_csv(merged, csv)
