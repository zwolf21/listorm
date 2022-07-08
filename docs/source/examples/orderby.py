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


# sorting by location asc age desc
ls.orderby('location', '-age')
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
# {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'}
# {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'}
# {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'}
# {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'}
# {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}


# sorting by callback; order by length of age, name, loacation as concat
ls.orderby(lambda age, name, location: -len(f'{age}{name}{location}')).print()
# {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'}
# {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'}
# {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
# {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
# {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'}


