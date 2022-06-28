import csv
from ..list import get_allkeys
from .io import get_stringio, reduce_fp



def read_csv(file, encoding='utf-8'):
    fp = reduce_fp(file, encoding=encoding)
    csv_reader = csv.reader(fp)
    fields = next(csv_reader)
    result = [dict(zip(fields, map(str, row))) for row in csv_reader]
    return result



def write_csv(records:list[dict], filename=None, fields=None, lineterminator='\n', encoding='utf-8'):
    output = get_stringio()
    fields = fields or get_allkeys(records)
    writer = csv.DictWriter(output, fields, lineterminator=lineterminator)
    writer.writeheader()
    for row in records:
        writer.writerow(row)
    if filename:
        with open(filename, 'w', encoding=encoding) as fp:
            fp.write(output.getvalue())
    else:
        return output.getvalue()
