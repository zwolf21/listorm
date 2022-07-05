import pytest

from listorm.api.forlist import *
from .samples import *


test_select_cases = [
    (userTable, 'name', ['location'], None, userTable_select_name_exclude_location),
    (userTable, [], None, lambda age: age > 20, userTable_age_over_20),
    (userTable, ['name', 'gender', 'location' ], None, lambda age: age > 20, userTable_select_name_gender_location_where_age_gt_20),
]
@pytest.mark.parametrize('records, columns, excludes, where, results', test_select_cases)
def test_select(records, columns, excludes, where, results):
    lst = select(records, columns, excludes=excludes, where=where)
    assert results == lst

test_drop_column_cases = [
    (userTable, ['age'], userTable_dropped_age),
    (userTable, ['gender', 'location'], userTable_dropped_gender_location),
]
@pytest.mark.parametrize('records, columns, results', test_drop_column_cases)
def test_drop(records, columns, results):
    lst = drop(records, columns)
    assert results == lst

test_add_column_cases = [
    (userTable, {'key': 'value'}, userTable_column_added_value),
    (userTable, {'gender/age': lambda gender, age: '{}/{}'.format(gender, age)}, userTable_column_added_gender_age_concated)
]
@pytest.mark.parametrize('records, column_mapset, results', test_add_column_cases)
def test_add_column(records, column_mapset, results):
    lst = add_column(records, **column_mapset)
    assert results == lst

test_rename_cases = [
    (userTable, {'location': 'address'}, userTable_renamed_location2address),
    (userTable, {'location': 'address', 'gender': 'sex'}, userTable_renamed_location2address_gender2sex),
]
@pytest.mark.parametrize('records, renamemap, results', test_rename_cases)
def test_rename(records, renamemap, results):
    lst = rename(records, **renamemap)
    assert results == lst

test_update_cases = [
    (userTable, {'name': str.upper}, None, userTable_updated_name_upper),
    (userTable, {'name': str.upper}, lambda age: age > 20, userTable_updated_name_upper_where_age_gt_20),
    (userTable, {'gender': lambda gender, age: "{}/{}".format(gender, age) }, None, userTable_updated_gender_concat_with_age),
]
@pytest.mark.parametrize('records, updatemap, where, results', test_update_cases)
def test_update(records, updatemap, where, results):
    lst = update(records, where=where, **updatemap)
    assert results == lst


test_values_cases = [
    (userTable, ['name'], True, userTable_values_by_name),
    (userTable, ['name'], False, userTable_values_by_name_flat_flase),
    (userTable, ['name', 'gender'], True, userTable_values_by_name_and_gender),
]
@pytest.mark.parametrize('records, columns, flat_one, results', test_values_cases)
def test_values(records, columns, flat_one, results):
    lst = values(records, columns, flat_one=flat_one)
    assert results == lst

test_distinct_cases = [
    (buyTable, ['name'], True, False, buyTable_distinct_by_name_keep_first),
    (buyTable, ['name'], False, False, buyTable_distinct_by_name_keep_last),
    (buyTable, ['name'], True, True, buyTable_distinct_by_name_singles),
]
@pytest.mark.parametrize('records, columns, first, singles, results', test_distinct_cases)
def test_distinct(records, columns, first, singles, results):
    lst = distinct(records, columns, keep_first=first, singles=singles)
    assert results == lst

test_orderby_cases = [
    (userTable, ['location', '-age'], userTable_orderby_location_age_desc)
]
@pytest.mark.parametrize('records, sortkeys, results', test_orderby_cases)
def test_orderby(records, sortkeys, results):
    lst = orderby(records, sortkeys)
    assert results == lst

test_groupby_cases = [
    (userTable, ['location', 'gender'], {'gender': len, 'age': lambda vals: sum(vals)/len(vals)}, {'gender': 'count', 'age': 'avg_age'}, userTable_groupby_location_gender)
]
@pytest.mark.parametrize('records, columns, aggset, renames, results', test_groupby_cases)
def test_groupby(records, columns, aggset, renames, results):
    lst = groupby(records, columns, renames=renames, **aggset)
    assert results == lst

test_join_cases = [
    (userTable, buyTable, 'name', None, 'inner', user_buy_table_inner_joined),
    (userTable, buyTable, 'name', None, 'left', user_buy_table_left_joined),
    (userTable, buyTable, 'name', None, 'right', user_buy_table_right_joined),
    (userTable, buyTable, 'name', None, 'outer', user_buy_table_outer_joined),
]
@pytest.mark.parametrize('records, other, on, right_on, how, results', test_join_cases)
def test_join(records, other, on, right_on, how, results):
    lst = join(records, other, on, on, right_on, how)
    lst = fillmissed(lst, '')
    lst = orderby(lst, 'name', 'product')
    lst = set_number_format(lst, amount=0)
    for rec, l in zip(results, lst):
        assert rec == l