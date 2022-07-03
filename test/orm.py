import pytest

from listorm import Listorm, read_csv, read_excel, aslambda
from listorm.exceptions import UniqueConstraintError
from .samples import *



test_init_arg_cases = [
    (userTable, None, False, None, userTable),
    (userTable_missing_values, None, False, None, userTable_missing_values),
    (userTable_missing_values, None, False, None, userTable_missing_values),
    (userTable_missing_values, None, True, 'undefined', userTable_missing_values_filling_with_undefined),
    (userTable, ('location', 'gender',), False, None, userTable),
    (userTable_missing_values, 'name', False, None, userTable_missing_values),
]
@pytest.mark.parametrize('records, uniques, fill_missed, fill_value, results', test_init_arg_cases)
def test_init(records, uniques, fill_missed, fill_value, results):
    if not uniques:
        lst = Listorm(records,uniques,fill_missed,fill_value)
        assert lst == results

    if uniques:
        with pytest.raises(UniqueConstraintError):
            lst = Listorm(records,uniques,fill_missed,fill_value)


test_select_cases = [
    (userTable, 'name', ['location'], None, userTable_select_name_exclude_location),
    (userTable, [], None, lambda row: row.age > 20, userTable_age_over_20),
    (userTable, ['name', 'gender', 'location' ], None, lambda row: row.age > 20, userTable_select_name_gender_location_where_age_gt_20),
]
@pytest.mark.parametrize('records, columns, excludes, where, results', test_select_cases)
def test_select(records, columns, excludes, where, results):
    lst = Listorm(records).select(columns, excludes=excludes, where=where)
    assert lst == results


test_drop_column_cases = [
    (userTable, ['age'], userTable_dropped_age),
    (userTable, ['gender', 'location'], userTable_dropped_gender_location),
]
@pytest.mark.parametrize('records, columns, results', test_drop_column_cases)
def test_drop_column(records, columns, results):
    lst = Listorm(records).drop_column(columns)
    assert lst == results


test_add_column_cases = [
    (userTable, {'key': 'value'}, userTable_column_added_value),
    (userTable, {'gender/age': lambda row: '{}/{}'.format(row.gender, row.age)}, userTable_column_added_gender_age_concated)
]
@pytest.mark.parametrize('records, column_mapset, results', test_add_column_cases)
def test_add_column(records, column_mapset, results):
    lst = Listorm(records).add_column(column_mapset)
    assert lst == results


test_rename_cases = [
    (userTable, {'location': 'address'}, userTable_renamed_location2address),
    (userTable, {'location': 'address', 'gender': 'sex'}, userTable_renamed_location2address_gender2sex),
]
@pytest.mark.parametrize('records, renamemap, results', test_rename_cases)
def test_rename(records, renamemap, results):
    lst = Listorm(records).rename(renamemap)
    assert lst == results


test_update_cases = [
    (userTable, {'name': aslambda(str.upper, 'name')}, None, userTable_updated_name_upper),
    (userTable, {'name': aslambda(str.upper, 'name')}, lambda row: row.age > 20, userTable_updated_name_upper_where_age_gt_20),
    (userTable, {'gender': aslambda("{}/{}".format, 'gender', 'age') }, None, userTable_updated_gender_concat_with_age),
]
@pytest.mark.parametrize('records, renamemap, where, results', test_update_cases)
def test_update(records, renamemap, where, results):
    lst = Listorm(records).update(renamemap, where=where)
    assert lst == results


test_values_cases = [
    (userTable, ['name'], True, userTable_values_by_name),
    (userTable, ['name'], False, userTable_values_by_name_flat_flase),
    (userTable, ['name', 'gender'], True, userTable_values_by_name_and_gender),
]
@pytest.mark.parametrize('records, columns, flat_one, results', test_values_cases)
def test_values(records, columns, flat_one, results):
    lst = Listorm(records).values(columns, flat_one=flat_one)
    assert lst == results


test_distinct_cases = [
    (buyTable, ['name'], True, False, buyTable_distinct_by_name_keep_first),
    (buyTable, ['name'], False, False, buyTable_distinct_by_name_keep_last),
    (buyTable, ['name'], True, True, buyTable_distinct_by_name_singles),
]
@pytest.mark.parametrize('records, columns, first, singles, results', test_distinct_cases)
def test_distinct(records, columns, first, singles, results):
    assert results == Listorm(records).distinct(columns, keep_first=first, singles=singles)


test_orderby_cases = [
    (userTable, ['location', '-age'], userTable_orderby_location_age_desc)
]
@pytest.mark.parametrize('records, sortkeys, results', test_orderby_cases)
def test_orderby(records, sortkeys, results):
    assert results == Listorm(records).orderby(sortkeys)

test_groupby_cases = [
    (userTable, ['location', 'gender'], {'gender': len, 'age': lambda vals: sum(vals)/len(vals)}, {'gender': 'count', 'age': 'avg_age'}, userTable_groupby_location_gender)
]
@pytest.mark.parametrize('records, columns, aggset, renames, results', test_groupby_cases)
def test_groupby(records, columns, aggset, renames, results):
    assert results == Listorm(records).groupby(columns, aggset=aggset, renames=renames)


test_join_cases = [
    (userTable, buyTable, 'name', None, 'inner', user_buy_table_inner_joined),
    (userTable, buyTable, 'name', None, 'left', user_buy_table_left_joined),
    (userTable, buyTable, 'name', None, 'right', user_buy_table_right_joined),
    (userTable, buyTable, 'name', None, 'outer', user_buy_table_outer_joined),
]
@pytest.mark.parametrize('records, other, on, right_on, how, results', test_join_cases)
def test_join(records, other, on, right_on, how, results):
    lst = Listorm(records, fill_value= '') \
        .join(other, on, right_on, how) \
        .orderby('name', 'product') \
        .set_number_type(amount=0)
    for rec, l in zip(results, lst):
        assert rec == l


test_write_and_read_csv_cases = [
    (userTable, 'user_table_write_test.csv', userTable),
    (userTable_missing_values, 'user_table_write_missing_values_test.csv', userTable_missing_values_filling_with_undefined),
    (userTable_has_one_column_name, 'user_table_write_has_oncolumn_test.csv', userTable_has_one_column_name)
]
@pytest.mark.parametrize('records, file, results', test_write_and_read_csv_cases)
def test_write_and_read_csv(records, file, results):
    lstsrc = Listorm(records, fill_value='undefined')
    lstsrc.to_csv(file)
    lstdest = read_csv(file).update(
        age=aslambda(int, 'age'),
        where=lambda row: row.age and row.age.isnumeric()
    )
    assert results == lstdest

test_write_and_read_excel_cases = [
    (userTable, 'user_table_write_test.xlsx', userTable),
    (userTable_missing_values, 'user_table_write_missing_values_test.xlsx', userTable_missing_values_filling_with_undefined),
    (userTable_has_one_column_name, 'user_table_write_has_oncolumn_test.xlsx', userTable_has_one_column_name)
]
@pytest.mark.parametrize('records, file, results', test_write_and_read_excel_cases)
def test_write_and_read_excel(records, file, results):
    lst = Listorm(records, fill_value='undefined')
    lst.to_excel(file)
    lstdest = read_excel(file)
    assert results == lstdest
