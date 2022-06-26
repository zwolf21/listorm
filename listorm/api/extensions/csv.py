import csv

from .io import get_stringio, path2fp



def read_csv(file, encoding='utf-8'):
    fp = path2fp(file, encoding=encoding)
    csv_reader = csv.reader(fp)
    fields = next(csv_reader)
    result = [dict(zip(fields, map(str, row))) for row in csv_reader]
    return result



def write_csv(records:list[dict], filename=None):
    output = get_stringio()
    writer = csv.DictWriter(output, lineterminator='\n')
    writer.writeheader()
    for row in records:
        writer.writerow(row)
    if filename:
        with open(filename, 'w') as fp:
            fp.write(output.getvalue())
    else:
        return output.getvalue()
