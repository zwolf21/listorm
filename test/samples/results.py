userTable_missing_values_filling_with_undefined = [
    {'age': 18, 'location': 'Korea', 'name': 'undefined', 'gender': 'undefined'},
    {'name': 'Charse', 'gender': 'M', 'location': 'USA', 'age': 'undefined'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'undefined', 'age': 'undefined', 'location': 'undefined'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'name': 'undefined', 'gender': 'undefined', 'age': 'undefined', 'location': 'Korea'},
]

userTable_select_name_exclude_location = [
    {'name': 'Hong'},
    {'name': 'Charse'},
    {'name': 'Lyn'},
    {'name': 'Xiaomi'},
    {'name': 'Park'},
    {'name': 'Smith'},
    {'name': 'Lee'},
]

userTable_age_over_20 = [
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
]

userTable_select_name_gender_location_where_age_gt_20 = [
    {'name': 'Lyn', 'gender': 'F', 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'location': 'Korea'},
]

userTable_dropped_age = [
    {'name': 'Hong', 'gender': 'M', 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'location': 'Korea'},
]

userTable_dropped_gender_location = [
    {'name': 'Hong', 'age': 18},
    {'name': 'Charse', 'age': 19},
    {'name': 'Lyn', 'age': 28},
    {'name': 'Xiaomi', 'age': 15},
    {'name': 'Park', 'age': 29},
    {'name': 'Smith', 'age': 17},
    {'name': 'Lee', 'age': 12},
]

userTable_column_added_gender_age_concated = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'gender/age': 'M/18'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'gender/age': 'M/19'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'gender/age': 'F/28'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'gender/age': 'M/15'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'gender/age': 'M/29'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'gender/age': 'M/17'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'gender/age': 'F/12'},
]

userTable_column_added_value = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'key': 'value'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'key': 'value'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'key': 'value'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'key': 'value'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'key': 'value'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'key': 'value'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'key': 'value'},
]

userTable_renamed_location2address = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'address': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'address': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'address': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'address': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'address': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'address': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'address': 'Korea'},
]
userTable_renamed_location2address_gender2sex = [
    {'name': 'Hong', 'sex': 'M', 'age': 18, 'address': 'Korea'},
    {'name': 'Charse', 'sex': 'M', 'age': 19, 'address': 'USA'},
    {'name': 'Lyn', 'sex': 'F', 'age': 28, 'address': 'China'},
    {'name': 'Xiaomi', 'sex': 'M', 'age': 15, 'address': 'China'},
    {'name': 'Park', 'sex': 'M', 'age': 29, 'address': 'Korea'},
    {'name': 'Smith', 'sex': 'M', 'age': 17, 'address': 'USA'},
    {'name': 'Lee', 'sex': 'F', 'age': 12, 'address': 'Korea'},
]

userTable_updated_name_upper = [
    {'name': 'HONG', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'CHARSE', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'LYN', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'XIAOMI', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'PARK', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'SMITH', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'name': 'LEE', 'gender': 'F', 'age': 12, 'location': 'Korea'},
]
userTable_updated_name_upper_where_age_gt_20 = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'LYN', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'PARK', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
]
userTable_updated_gender_concat_with_age = [
    {'name': 'Hong', 'gender': 'M/18', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M/19', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F/28', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M/15', 'age': 15, 'location': 'China'},
    {'name': 'Park', 'gender': 'M/29', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M/17', 'age': 17, 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F/12', 'age': 12, 'location': 'Korea'},
]

userTable_values_by_name = ['Hong','Charse','Lyn','Xiaomi','Park','Smith','Lee']
userTable_values_by_name = ['Hong','Charse','Lyn','Xiaomi','Park','Smith','Lee']
userTable_values_by_name_flat_flase = [('Hong',),('Charse',),('Lyn',),('Xiaomi',),('Park',),('Smith',),('Lee',)]
userTable_values_by_name_and_gender = [
    ("Hong", "M",),
    ("Charse", "M",),
    ("Lyn", "F",),
    ("Xiaomi", "M",),
    ("Park", "M",),
    ("Smith", "M",),
    ("Lee", "F",),
]

buyTable_distinct_by_name_keep_first = [
    {'name': 'Xiaomi', 'product': 'battery', 'amount':7},
    {'name': 'Hong', 'product': 'keyboard', 'amount':1},
    {'name': 'Lyn', 'product': 'cleaner', 'amount':5},
    {'name': 'Unknown', 'product': 'keyboard', 'amount':1},
    {'name': 'Lee', 'product': 'hardcase', 'amount':2},
    {'name': 'Yuki', 'product': 'manual', 'amount':1},
    {'name': 'anonymous', 'product': 'adopter', 'amount':2},
    {'name': 'Park', 'product': 'battery', 'amount':2},
    {'name': 'Smith', 'product': 'mouse', 'amount':1},
]
buyTable_distinct_by_name_keep_last = [
    {'name': 'Lyn', 'product': 'mouse', 'amount':1},
    {'name': 'Unknown', 'product': 'keyboard', 'amount':1},
    {'name': 'Lee', 'product': 'keycover', 'amount':2},
    {'name': 'Yuki', 'product': 'manual', 'amount':1},
    {'name': 'Xiaomi', 'product': 'cable', 'amount':1},
    {'name': 'anonymous', 'product': 'adopter', 'amount':2},
    {'name': 'Park', 'product': 'battery', 'amount':2},
    {'name': 'Hong', 'product': 'cleaner', 'amount':3},
    {'name': 'Smith', 'product': 'mouse', 'amount':1},
]
buyTable_distinct_by_name_singles = [
    {'name': 'Unknown', 'product': 'keyboard', 'amount':1},
    {'name': 'Yuki', 'product': 'manual', 'amount':1},
    {'name': 'anonymous', 'product': 'adopter', 'amount':2},
    {'name': 'Park', 'product': 'battery', 'amount':2},
    {'name': 'Smith', 'product': 'mouse', 'amount':1},
]


userTable_orderby_location_age_desc = [
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
]

userTable_groupby_location_gender = [
    {'location': 'Korea', 'gender': 'M', 'count': 2, 'avg_age': 23.5},
    {'location': 'USA', 'gender': 'M', 'count': 2, 'avg_age': 18.0},
    {'location': 'China', 'gender': 'F', 'count': 1, 'avg_age': 28.0},
    {'location': 'China', 'gender': 'M', 'count': 1, 'avg_age': 15.0},
    {'location': 'Korea', 'gender': 'F', 'count': 1, 'avg_age': 12.0}
]


user_buy_table_inner_joined = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'cleaner', 'amount': 3},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'hardcase', 'amount': 2},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'keycover', 'amount': 2},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'product': 'battery', 'amount': 2},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'product': 'mouse', 'amount': 1},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'battery', 'amount': 7},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'cable', 'amount': 1},
]

user_buy_table_left_joined = [
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'product': '', 'amount': 0.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'cleaner', 'amount': 3.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3.0},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'hardcase', 'amount': 2.0},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'keycover', 'amount': 2.0},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5.0},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1.0},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'product': 'battery', 'amount': 2.0},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'product': 'mouse', 'amount': 1.0},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'battery', 'amount': 7.0},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'cable', 'amount': 1.0},
]

user_buy_table_right_joined = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'cleaner', 'amount': 3.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3.0},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'hardcase', 'amount': 2.0},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'keycover', 'amount': 2.0},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5.0},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1.0},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'product': 'battery', 'amount': 2.0},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'product': 'mouse', 'amount': 1.0},
    {'name': 'Unknown', 'gender': '', 'age': '', 'location': '', 'product': 'keyboard', 'amount': 1.0},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'battery', 'amount': 7.0},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'cable', 'amount': 1.0},
    {'name': 'Yuki', 'gender': '', 'age': '', 'location': '', 'product': 'manual', 'amount': 1.0},
    {'name': 'anonymous', 'gender': '', 'age': '', 'location': '', 'product': 'adopter', 'amount': 2.0},
]

user_buy_table_outer_joined = [
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'product': '', 'amount': 0.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'cleaner', 'amount': 3.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1.0},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3.0},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'hardcase', 'amount': 2.0},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea', 'product': 'keycover', 'amount': 2.0},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5.0},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1.0},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea', 'product': 'battery', 'amount': 2.0},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA', 'product': 'mouse', 'amount': 1.0},
    {'name': 'Unknown', 'gender': '', 'age': '', 'location': '', 'product': 'keyboard', 'amount': 1.0},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'battery', 'amount': 7.0},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China', 'product': 'cable', 'amount': 1.0},
    {'name': 'Yuki', 'gender': '', 'age': '', 'location': '', 'product': 'manual', 'amount': 1.0},
    {'name': 'anonymous', 'gender': '', 'age': '', 'location': '', 'product': 'adopter', 'amount': 2.0},
]


buyTable_values_count_by_product = {
    'adopter': 1,
    'battery': 2,
    'cable': 1,
    'cleaner': 2,
    'hardcase': 1,
    'keyboard': 2,
    'keycover': 1,
    'manual': 1,
    'monitor': 1,
    'mouse': 3
}

userTable_created = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
    {'name': 'moon', 'gender': 'M', 'age': 38, 'location': 'Korea'},
    {'name': 'choi', 'gender': 'F', 'age': 28, 'location': 'Korea'},
    {'name': 'vice', 'gender': 'M', 'age': 41, 'location': 'Mexico'},
]

userTable_created_and_updated = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'F', 'age': 21, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'F', 'age': 27, 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
    {'name': 'moon', 'gender': 'M', 'age': 38, 'location': 'Korea'},
    {'name': 'choi', 'gender': 'F', 'age': 28, 'location': 'Korea'},
    {'name': 'vice', 'gender': 'M', 'age': 41, 'location': 'Mexico'},
]


userTable_created_and_deleted = [
    {'name': 'moon', 'gender': 'M', 'age': 38, 'location': 'Korea'},
    {'name': 'choi', 'gender': 'F', 'age': 28, 'location': 'Korea'},
    {'name': 'vice', 'gender': 'M', 'age': 41, 'location': 'Mexico'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
]