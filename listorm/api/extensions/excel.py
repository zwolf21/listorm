import openpyxl
import xlsxwriter

from .io import get_bytesio, reduce_fp
from ..list import asvalues, fillmissed



def read_excel(file=None, sheet_name=None):
    '''Excel File or byte Content of Excel to Listorm object
    '''
    file = reduce_fp(file, 'rb')
    workbook= openpyxl.load_workbook(file)
    worksheet = workbook[sheet_name] if sheet_name else workbook.active
    fields, *values = worksheet.values
    return [
        dict(zip(fields, row)) for row in values
    ]



def write_excel(records:list[dict], filename=None, fields=None):
    records = fillmissed(records)
    fields = fields or records[0].keys()
    output = get_bytesio()
    workbook =  xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.write_row(0,0,fields)
    for i, row in enumerate(records, 1):
        values = asvalues(row, fields, flat=False)
        worksheet.write_row(i, 0, values)
    workbook.close()

    content = output.getvalue()

    if not filename:
        return content

    with open(filename, 'wb') as fp:
        fp.write(content)
