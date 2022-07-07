from listorm import Listorm


userTable = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
]


buyTable = [
    {'name': 'Xiaomi', 'product': 'battery', 'amount':7},
    {'name': 'Hong', 'product': 'keyboard', 'amount':1},
    {'name': 'Lyn', 'product': 'cleaner', 'amount':5},
    {'name': 'Hong', 'product': 'monitor', 'amount':1},
    {'name': 'Hong', 'product': 'mouse', 'amount':3},
    {'name': 'Lyn', 'product': 'mouse', 'amount':1},
]


users = Listorm(userTable)
buyings = Listorm(buyTable)

# inner join
users.join(buyings, left_on=('name',), right_on=('name',))
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1}

# left join 
# If both join key names are the same, only left_on can be specified
users.join(buyings, left_on='name', how='left')
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3}
# ** {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'product': None, 'amount': None}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1}

# right join
users.join(buyings, left_on='name', how='right')
# ** {'name': 'Xiaomi', 'product': 'battery', 'amount': 7, 'gender': None, 'age': None, 'location': None}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1}

# fill missing 
users.join(buyings, left_on='name', how='outer').print()
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'keyboard', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'monitor', 'amount': 1}
# {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea', 'product': 'mouse', 'amount': 3}
# {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA', 'product': None, 'amount': None}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'cleaner', 'amount': 5}
# {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China', 'product': 'mouse', 'amount': 1}
# {'name': 'Xiaomi', 'product': 'battery', 'amount': 7, 'gender': None, 'age': None, 'location': None}

