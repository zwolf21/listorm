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


# update by key:value mapping
mapping = {'M': 'male', 'F': 'female'}
ls.update(gender=mapping).print()
# {'name': 'Hong', 'gender': 'male', 'age': 18, 'location': 'Korea'}
# {'name': 'Charse', 'gender': 'male', 'age': 19, 'location': 'USA'}
# {'name': 'Lyn', 'gender': 'female', 'age': 28, 'location': 'China'}
# {'name': 'Xiaomi', 'gender': 'male', 'age': 15, 'location': 'China'}
# {'name': 'Park', 'gender': 'male', 'age': 29, 'location': 'Korea'}
# {'name': 'Smith', 'gender': 'male', 'age': 17, 'location': 'USA'}
# {'name': 'Lee', 'gender': 'female', 'age': 12, 'location': 'Korea'}


# update by callable with where clause
ls.update(name=str.upper, where=lambda gender, age: gender == 'M' and age > 17 ).print()
# **{'name': 'HONG', 'gender': 'M', 'age': 18, 'location': 'Korea'}**
# **{'name': 'CHARSE', 'gender': 'M', 'age': 19, 'location': 'USA'}**
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
# {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'}
# **{'name': 'PARK', 'gender': 'M', 'age': 29, 'location': 'Korea'}**
# {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
# {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'}


ls.update(
    age=lambda age: age + 1,
    where=lambda location: location.lower() in ['china', 'korea']
)
# **{'name': 'Hong', 'gender': 'M', 'age': 19, 'location': 'Korea'}
# {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'}
# **{'name': 'Lyn', 'gender': 'F', 'age': 29, 'location': 'China'}
# **{'name': 'Xiaomi', 'gender': 'M', 'age': 16, 'location': 'China'}
# **{'name': 'Park', 'gender': 'M', 'age': 30, 'location': 'Korea'}
# {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'}
# **{'name': 'Lee', 'gender': 'F', 'age': 13, 'location': 'Korea'}

