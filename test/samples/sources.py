userTable = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
]

userTable_for_create = [
    {'name': 'moon', 'gender': 'M', 'age': 38, 'location': 'Korea'},
    {'name': 'choi', 'gender': 'F', 'age': 28, 'location': 'Korea'},
    {'name': 'vice', 'gender': 'M', 'age': 41, 'location': 'Mexico'},
]

userTable_for_create_and_update = [
    {'name': 'moon', 'gender': 'M', 'age': 38, 'location': 'Korea'},
    {'name': 'choi', 'gender': 'F', 'age': 28, 'location': 'Korea'},
    {'name': 'vice', 'gender': 'M', 'age': 41, 'location': 'Mexico'},
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Xiaomi', 'gender': 'F', 'age': 21, 'location': 'China'},
    {'name': 'Smith', 'gender': 'F', 'age': 27, 'location': 'USA'},
]

userTable_for_create_and_delete = [
    {'name': 'moon', 'gender': 'M', 'age': 38, 'location': 'Korea'},
    {'name': 'choi', 'gender': 'F', 'age': 28, 'location': 'Korea'},
    {'name': 'vice', 'gender': 'M', 'age': 41, 'location': 'Mexico'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
]




userTable_missing_values = [
    {'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', },
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'location': 'Korea'},
]

userTable_has_one_column_name = [
    {'name': 'Charse'},
    {'name': 'Lyn'},
    {'name': 'Xiaomi'},
    {'name': 'Park'},
    {'name': 'Smith'},
]

buyTable = [
    {'name': 'Xiaomi', 'product': 'battery', 'amount':7},
    {'name': 'Hong', 'product': 'keyboard', 'amount':1},
    {'name': 'Lyn', 'product': 'cleaner', 'amount':5},
    {'name': 'Hong', 'product': 'monitor', 'amount':1},
    {'name': 'Hong', 'product': 'mouse', 'amount':3},
    {'name': 'Lyn', 'product': 'mouse', 'amount':1},
    {'name': 'Unknown', 'product': 'keyboard', 'amount':1},
    {'name': 'Lee', 'product': 'hardcase', 'amount':2},
    {'name': 'Lee', 'product': 'keycover', 'amount':2},
    {'name': 'Yuki', 'product': 'manual', 'amount':1},
    {'name': 'Xiaomi', 'product': 'cable', 'amount':1},
    {'name': 'anonymous', 'product': 'adopter', 'amount':2},
    {'name': 'Park', 'product': 'battery', 'amount':2},
    {'name': 'Hong', 'product': 'cleaner', 'amount':3},
    {'name': 'Smith', 'product': 'mouse', 'amount':1},
]
