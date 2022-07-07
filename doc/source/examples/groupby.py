from listorm import Listorm


userTable = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
]


ls = Listorm(userTable)

# groupby location, gender
ls.groupby(
    'location', 'gender', # columns for grouping
    age=sum, name=len, # aggregate
    renames={           # renaming for columns to retrive aggregation
        'age': 'age_sum',
        'name': 'gender_count',
    }
)
# {'location': 'Korea', 'gender': 'M', 'age_sum': 47, 'gender_count': 2}
# {'location': 'USA', 'gender': 'M', 'age_sum': 36, 'gender_count': 2}
# {'location': 'China', 'gender': 'F', 'age_sum': 28, 'gender_count': 1}
# {'location': 'China', 'gender': 'M', 'age_sum': 15, 'gender_count': 1}
# {'location': 'Korea', 'gender': 'F', 'age_sum': 12, 'gender_count': 1}

# retrive by with dangled groups
ls.groupby(
    'location', 'gender',
    age=sum, name=len,
    renames={
        'age': 'age_sum',
        'name': 'gender_count',
    },
    groupset_name='grouped' # column name for dangling group
)
# {'location': 'Korea', 'gender': 'M', 'age_sum': 47, 'gender_count': 2,
#     'grouped': [
#         {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
#         {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
#     ]
# }
# {'location': 'USA', 'gender': 'M', 'age_sum': 36, 'gender_count': 2,
#     'grouped': [
#         {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
#         {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
#     ]
# }
# {'location': 'China', 'gender': 'F', 'age_sum': 28, 'gender_count': 1,
#     'grouped': [
#         {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
#     ]
# }
# {'location': 'China', 'gender': 'M', 'age_sum': 15, 'gender_count': 1,
#     'grouped': [
#         {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'}
#     ]
# }
# {'location': 'Korea', 'gender': 'F', 'age_sum': 12, 'gender_count': 1,
#     'grouped': [
#         {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'}
#     ]
# }
