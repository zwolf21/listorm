from listorm import read_csv, select, groupby, asmap, fillmissed, read_excel
import re, math



def _split_amtunit(lst, columns, pfix_amt='amt', pfix_unit='unit'):
    pat = re.compile(r"(?P<amount>\d*\.?\d+)\s*(?P<unit>\w+)")
    def extract_amount(value):
        if g := pat.search(value):
            return g.group('amount')
    def extract_unit(value):
        if g:= pat.search(value):
            return g.group('unit')
        
    if isinstance(columns, str):
        columns = [columns]
    for column in columns:
        column_amt = f"{column}_{pfix_amt}"
        column_unit = f"{column}_{pfix_unit}"
        lst = lst.add_column(
            keymap={
                column_amt: lambda **row: extract_amount(row[column]),
                column_unit: lambda **row: extract_unit(row[column])
            }
        )
        lst = lst.set_number_type(formats={column_amt: 0.0})
#         lst = lst.add_column(**{column_amt: extract_amount, column_unit: extract_unit})
    return lst

if __name__ == '__main__':

    PRN_COLUMNS = [
        '발행처', '등록번호', '환자명', 'No.', '약품코드', '약품명', '투여량', '횟수', '일수', '총량', '용법', 'ADC', 'PRN', '퇴원', '처방의사', '입력일시',
        '투약번호', '차수', '접수일시'
    ]
    INJ_GROUPS = ['고가약', '고위험', '냉장약', '일반2', '마약', '향정약']

    lstdrug = read_excel('EUMC20210827약품정보.xlsx', fields_contains=['약품코드'], uniques='한글약품명' )
    lstprn = read_csv('prn_sample.txt', fields=PRN_COLUMNS, encoding='cp949',  delimiter='	')
    prn = lstprn.join(lstdrug, left_on='약품명', right_on='상용약품명').select(['발행처', '약품명', '기본투여단위', '함량', '규격', '환산단위', '투여량', '주사그룹번호(입)', '입력일시'])

    prn = _split_amtunit(prn, ['투여량', '함량', '규격'])

    prn = prn.add_column(수량=None)

    prn = prn.update(
        수량=lambda 투여량_amt, 함량_amt: 투여량_amt/함량_amt,
        where=lambda 함량_unit, 투여량_unit, 함량_amt: 함량_amt > 0 and  함량_unit == 투여량_unit
    )
    
    prn = prn.update(
        수량=lambda 투여량_amt, 규격_amt: 투여량_amt/규격_amt,
        where=lambda 수량, 규격_unit, 투여량_unit: 수량 is None and 규격_unit == 투여량_unit
    )

    prn = prn.update(
        수량=lambda 투여량_amt: 투여량_amt,
        where=lambda 환산단위, 투여량_unit, 수량: 수량 is None and 환산단위 == 투여량_unit
    )

    prn = prn.select(where=lambda 수량: 수량).update(수량=math.ceil)

    prn = prn.select(where=lambda **row: row['주사그룹번호(입)'] in INJ_GROUPS)

    grouped = prn.groupby(
        '약품명', '환산단위', '주사그룹번호(입)',
        수량=sum,
    ).orderby('주사그룹번호(입)', '약품명')

    grouby_word = prn.groupby(
        '주사그룹번호(입)', '약품명','발행처',
        수량=sum
    ).orderby('주사그룹번호(입)', '약품명')

    # grouped.print(1000)

    grouby_word.print(100)