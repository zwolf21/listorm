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
ls.select(['name', 'gender', 'location']).print()
# {'name': 'Hong', 'gender': 'M', 'location': 'Korea'}
# {'name': 'Charse', 'gender': 'M', 'location': 'USA'}
# {'name': 'Lyn', 'gender': 'F', 'location': 'China'}
# {'name': 'Xiaomi', 'gender': 'M', 'location': 'China'}
# {'name': 'Park', 'gender': 'M', 'location': 'Korea'}
# {'name': 'Smith', 'gender': 'M', 'location': 'USA'}
# {'name': 'Lee', 'gender': 'F', 'location': 'Korea'}


# select columns with filter
ls.select('name', 'gender', 'age', where=lambda age: age > 20).print()
# {'name': 'Lyn', 'gender': 'F', 'age': 28}
# {'name': 'Park', 'gender': 'M', 'age': 29}

# drop columns
ls.drop_column('gender', 'age').print()
# {'name': 'Lyn', 'gender': 'F', 'age': 28}
# {'name': 'Park', 'gender': 'M', 'age': 29}
# {'name': 'Hong', 'location': 'Korea'}
# {'name': 'Charse', 'location': 'USA'}
# {'name': 'Lyn', 'location': 'China'}
# {'name': 'Xiaomi', 'location': 'China'}
# {'name': 'Park', 'location': 'Korea'}
# {'name': 'Smith', 'location': 'USA'}
# {'name': 'Lee', 'location': 'Korea'}


# method chaining
values = ls.select(
    'name', 'gender', 'location', where=lambda age: age > 20
    ).values('name', 'location')
print(values)
# [('Lyn', 'China'), ('Park', 'Korea')]

