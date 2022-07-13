## Note: This documentation is for older version of listorm as 0.x.x

## [View documentation of listorm after version 1.0](https://zwolf21.github.io/listorm/)

----

### Installation of older version
`pip install listorm==0.2.16`

----

```python
import listorm as ls
```

1-1. Basic useage - create a Listorm Object

1)Listorm Ojbect is derived from list

2)The Elements of Listorm Object is 'Scheme' derived from dict


```python
scheme1 = ls.Scheme({'name': 'park', 'age': 15, 'phone':None})
scheme2 = ls.Scheme({'name': 'kim', 'age':5, 'location': 'Seoul', 'phone': '111-222-333'})
```


```python
# if add operating smart overwrite (overwrite if value is none on Same key)
scheme1+scheme2
```




    {'age': 15, 'location': 'Seoul', 'name': 'park', 'phone': '111-222-333'}




```python
# The List within different key of dict
lst = [
    {'name': 'Hong', 'age': 18, 'location': 'Korea'},
    {'name': 'Yuki', 'age': 19,},
    {'name': 'Lee', 'age': 12, 'phone': '010-2451-1532'},   
]
```


```python
# Auto normailize: set same keys for each record(set to None if key does not exists)
ls.Listorm(lst)
```




    [{'age': 18, 'location': 'Korea', 'name': 'Hong', 'phone': None},
     {'age': 19, 'location': None, 'name': 'Yuki', 'phone': None},
     {'age': 12, 'location': None, 'name': 'Lee', 'phone': '010-2451-1532'}]



1-2. Basic useage - retrieve and parsing data


```python
# Customer's info in a Shopping mall
userTable = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
    {'name': 'Smith', 'gender': 'M', 'age': 17, 'location': 'USA'},
    {'name': 'Lee', 'gender': 'F', 'age': 12, 'location': 'Korea'},
]
```


```python
#select Columns
lst_customer = ls.Listorm(userTable)
lst_customer.select('name', 'location')
```




    [{'location': 'Korea', 'name': 'Hong'},
     {'location': 'USA', 'name': 'Charse'},
     {'location': 'China', 'name': 'Lyn'},
     {'location': 'China', 'name': 'Xiaomi'},
     {'location': 'Japan', 'name': 'Yuki'},
     {'location': 'Korea', 'name': 'Park'},
     {'location': 'USA', 'name': 'Smith'},
     {'location': 'Korea', 'name': 'Lee'}]




```python
#select Columns only with values, 2dArry
lst_customer = ls.Listorm(userTable)
lst_customer.select('name', 'location', values=True)
```




    [('Hong', 'Korea'),
     ('Charse', 'USA'),
     ('Lyn', 'China'),
     ('Xiaomi', 'China'),
     ('Yuki', 'Japan'),
     ('Park', 'Korea'),
     ('Smith', 'USA'),
     ('Lee', 'Korea')]




```python
#select Columns only with values, Similar to select(*args, values=True)
lst_customer = ls.Listorm(userTable)
lst_customer.row_values('name', 'location')
```




    [['Hong', 'Korea'],
     ['Charse', 'USA'],
     ['Lyn', 'China'],
     ['Xiaomi', 'China'],
     ['Yuki', 'Japan'],
     ['Park', 'Korea'],
     ['Smith', 'USA'],
     ['Lee', 'Korea']]




```python
#filtering
lst_customer = ls.Listorm(userTable)
lst_customer.filter(where=lambda row:row.age > 18)
```




    [{'age': 19, 'gender': 'M', 'location': 'USA', 'name': 'Charse'},
     {'age': 28, 'gender': 'F', 'location': 'China', 'name': 'Lyn'},
     {'age': 19, 'gender': 'F', 'location': 'Japan', 'name': 'Yuki'},
     {'age': 29, 'gender': 'M', 'location': 'Korea', 'name': 'Park'}]




```python
# With Method Chaining
lst_customer = ls.Listorm(userTable)
lst_customer.select('name', 'location', 'age').filter(where=lambda row:row['age'] > 18)
```




    [{'age': 19, 'location': 'USA', 'name': 'Charse'},
     {'age': 28, 'location': 'China', 'name': 'Lyn'},
     {'age': 19, 'location': 'Japan', 'name': 'Yuki'},
     {'age': 29, 'location': 'Korea', 'name': 'Park'}]




```python
# Get a Column values
lst_customer = ls.Listorm(userTable)
lst_customer.column_values('age')
```




    [18, 19, 28, 15, 19, 29, 17, 12]




```python
# Get a Column values unique
lst_customer = ls.Listorm(userTable)
lst_customer.unique('location')
```




    {'China', 'Japan', 'Korea', 'USA'}




```python
# Get a Column values count
lst_customer = ls.Listorm(userTable)
lst_customer.value_count('location')
```




    Counter({'China': 2, 'Japan': 1, 'Korea': 3, 'USA': 2})



2. Basic useage - modifying and update data


```python
# change number type
numbers = [
    {'flt': 0.5, 'string': '123', 'string_float': '123.5', 
     'int': 412, 'string_int': '5123', 'blabla': 'what?'
    }
]

lst_numbers = ls.Listorm(numbers)

# column name and example of types to change, if faild to change, example value will be default value
lst_numbers.set_number_type(flt='', string=0.0, string_float=0, int='', string_int=0, blabla=0)
```




    [{'blabla': 0,
      'flt': '0.5',
      'int': '412',
      'string': 123.0,
      'string_float': 123,
      'string_int': 5123}]




```python
# modify by record qpplied function
lst_customer = ls.Listorm(userTable)
lst_customer.apply_row(
    age= lambda row:'{}_{}'.format(row.gender, row.age),
    name = lambda row:'{}_{}_{}'.format(row.gender, row.age, row.name),
)
```




    [{'age': 'M_18', 'gender': 'M', 'location': 'Korea', 'name': 'M_M_18_Hong'},
     {'age': 'M_19', 'gender': 'M', 'location': 'USA', 'name': 'M_M_19_Charse'},
     {'age': 'F_28', 'gender': 'F', 'location': 'China', 'name': 'F_F_28_Lyn'},
     {'age': 'M_15', 'gender': 'M', 'location': 'China', 'name': 'M_M_15_Xiaomi'},
     {'age': 'F_19', 'gender': 'F', 'location': 'Japan', 'name': 'F_F_19_Yuki'},
     {'age': 'M_29', 'gender': 'M', 'location': 'Korea', 'name': 'M_M_29_Park'},
     {'age': 'M_17', 'gender': 'M', 'location': 'USA', 'name': 'M_M_17_Smith'},
     {'age': 'F_12', 'gender': 'F', 'location': 'Korea', 'name': 'F_F_12_Lee'}]




```python
# modify by value only applied function
lst_customer = ls.Listorm(userTable)
lst_customer.map(gender=lambda val:{'M':'Male', 'F':'Female'}.get(val, val))
```




    [{'age': 18, 'gender': 'Male', 'location': 'Korea', 'name': 'Hong'},
     {'age': 19, 'gender': 'Male', 'location': 'USA', 'name': 'Charse'},
     {'age': 28, 'gender': 'Female', 'location': 'China', 'name': 'Lyn'},
     {'age': 15, 'gender': 'Male', 'location': 'China', 'name': 'Xiaomi'},
     {'age': 19, 'gender': 'Female', 'location': 'Japan', 'name': 'Yuki'},
     {'age': 29, 'gender': 'Male', 'location': 'Korea', 'name': 'Park'},
     {'age': 17, 'gender': 'Male', 'location': 'USA', 'name': 'Smith'},
     {'age': 12, 'gender': 'Female', 'location': 'Korea', 'name': 'Lee'}]




```python
# rename columns
lst_customer = ls.Listorm(userTable)
lst_customer.rename(name='who', location='nation')
```




    [{'age': 18, 'gender': 'M', 'nation': 'Korea', 'who': 'Hong'},
     {'age': 19, 'gender': 'M', 'nation': 'USA', 'who': 'Charse'},
     {'age': 28, 'gender': 'F', 'nation': 'China', 'who': 'Lyn'},
     {'age': 15, 'gender': 'M', 'nation': 'China', 'who': 'Xiaomi'},
     {'age': 19, 'gender': 'F', 'nation': 'Japan', 'who': 'Yuki'},
     {'age': 29, 'gender': 'M', 'nation': 'Korea', 'who': 'Park'},
     {'age': 17, 'gender': 'M', 'nation': 'USA', 'who': 'Smith'},
     {'age': 12, 'gender': 'F', 'nation': 'Korea', 'who': 'Lee'}]




```python
# adding new columns by record applied function
lst_customer = ls.Listorm(userTable)
lst_customer.add_columns(is_child=lambda row:row.age<15).select('name', 'age', 'is_child')
```




    [{'age': 18, 'is_child': False, 'name': 'Hong'},
     {'age': 19, 'is_child': False, 'name': 'Charse'},
     {'age': 28, 'is_child': False, 'name': 'Lyn'},
     {'age': 15, 'is_child': False, 'name': 'Xiaomi'},
     {'age': 19, 'is_child': False, 'name': 'Yuki'},
     {'age': 29, 'is_child': False, 'name': 'Park'},
     {'age': 17, 'is_child': False, 'name': 'Smith'},
     {'age': 12, 'is_child': True, 'name': 'Lee'}]




```python
# get top of records by N
lst_customer = ls.Listorm(userTable)
lst_customer.top('age', n=2) # get oldest 2 people in Listorm
```




    [{'age': 29, 'gender': 'M', 'location': 'Korea', 'name': 'Park'},
     {'age': 28, 'gender': 'F', 'location': 'China', 'name': 'Lyn'}]




```python
# get top of records by percentage(if 0<n<1)
lst_customer = ls.Listorm(userTable)
lst_customer.top('age', n=0.5) # get oldest people by top 50% of age
```




    [{'age': 29, 'gender': 'M', 'location': 'Korea', 'name': 'Park'},
     {'age': 28, 'gender': 'F', 'location': 'China', 'name': 'Lyn'},
     {'age': 19, 'gender': 'M', 'location': 'USA', 'name': 'Charse'},
     {'age': 19, 'gender': 'F', 'location': 'Japan', 'name': 'Yuki'}]



3 . Advanced useage - sorting, grouping, join


```python
# 1.orderby location ASC age DESC
lst_customer = ls.Listorm(userTable)
lst_customer.orderby('location', '-age')
```




    [{'age': 28, 'gender': 'F', 'location': 'China', 'name': 'Lyn'},
     {'age': 15, 'gender': 'M', 'location': 'China', 'name': 'Xiaomi'},
     {'age': 19, 'gender': 'F', 'location': 'Japan', 'name': 'Yuki'},
     {'age': 29, 'gender': 'M', 'location': 'Korea', 'name': 'Park'},
     {'age': 18, 'gender': 'M', 'location': 'Korea', 'name': 'Hong'},
     {'age': 12, 'gender': 'F', 'location': 'Korea', 'name': 'Lee'},
     {'age': 19, 'gender': 'M', 'location': 'USA', 'name': 'Charse'},
     {'age': 17, 'gender': 'M', 'location': 'USA', 'name': 'Smith'}]




```python
# 2-1groupby location, retrieve gender count and max age
lst_customer = ls.Listorm(userTable)
lst_customer.groupby('location', age=max, gender=len)
```




    [{'age': 28, 'gender': 2, 'location': 'China'},
     {'age': 19, 'gender': 1, 'location': 'Japan'},
     {'age': 29, 'gender': 3, 'location': 'Korea'},
     {'age': 19, 'gender': 2, 'location': 'USA'}]




```python
# 2-2.you can rename retrieving columns name which set by grouped result 
lst_customer = ls.Listorm(userTable)
lst_customer.groupby('location', 
            age=max, gender=len, location=len, 
            renames={'age':'Oldest', 'gender': 'GenderCount', 'location': 'locationCount'}
    )
```




    [{'GenderCount': 2, 'Oldest': 28, 'locationCount': 2},
     {'GenderCount': 1, 'Oldest': 19, 'locationCount': 1},
     {'GenderCount': 3, 'Oldest': 29, 'locationCount': 3},
     {'GenderCount': 2, 'Oldest': 19, 'locationCount': 2}]




```python
# 2-2.you can include extra column value(value might be last record of group)
lst_customer = ls.Listorm(userTable)
lst_customer.groupby('location',
            age=max, gender=len, location=len, 
            renames={'age':'Oldest', 'gender': 'GenderCount', 'location': 'locationCount'},
            extra_columns = ['location']
    )
```




    [{'GenderCount': 2, 'Oldest': 28, 'location': 'China', 'locationCount': 2},
     {'GenderCount': 1, 'Oldest': 19, 'location': 'Japan', 'locationCount': 1},
     {'GenderCount': 3, 'Oldest': 29, 'location': 'Korea', 'locationCount': 3},
     {'GenderCount': 2, 'Oldest': 19, 'location': 'USA', 'locationCount': 2}]




```python
# 3.join
#Customers buy records for join Example
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
```


```python
lst_customer = ls.Listorm(userTable)
lst_buyitems = ls.Listorm(buyTable)
```


```python
# 3-1 inner join
# Add Extra customer's Info (location) to each buytime
lst_buyitems.join(lst_customer.select('location', 'name'), on='name')
```




    [{'amount': 1, 'location': 'Japan', 'name': 'Yuki', 'product': 'manual'},
     {'amount': 1, 'location': 'USA', 'name': 'Smith', 'product': 'mouse'},
     {'amount': 2, 'location': 'Korea', 'name': 'Lee', 'product': 'hardcase'},
     {'amount': 2, 'location': 'Korea', 'name': 'Lee', 'product': 'keycover'},
     {'amount': 7, 'location': 'China', 'name': 'Xiaomi', 'product': 'battery'},
     {'amount': 1, 'location': 'China', 'name': 'Xiaomi', 'product': 'cable'},
     {'amount': 1, 'location': 'Korea', 'name': 'Hong', 'product': 'keyboard'},
     {'amount': 1, 'location': 'Korea', 'name': 'Hong', 'product': 'monitor'},
     {'amount': 3, 'location': 'Korea', 'name': 'Hong', 'product': 'mouse'},
     {'amount': 3, 'location': 'Korea', 'name': 'Hong', 'product': 'cleaner'},
     {'amount': 2, 'location': 'Korea', 'name': 'Park', 'product': 'battery'},
     {'amount': 5, 'location': 'China', 'name': 'Lyn', 'product': 'cleaner'},
     {'amount': 1, 'location': 'China', 'name': 'Lyn', 'product': 'mouse'}]




```python
# 3-2 left join
# if names in buy table are not in customer table, then set to none the customer's info(location is set to none)
lst_buyitems.join(lst_customer.select('location', 'name'), on='name', how='left')
# Unknown and anonymouse location would be set to None
```




    [{'amount': 1, 'location': 'Korea', 'name': 'Hong', 'product': 'keyboard'},
     {'amount': 1, 'location': 'Korea', 'name': 'Hong', 'product': 'monitor'},
     {'amount': 3, 'location': 'Korea', 'name': 'Hong', 'product': 'mouse'},
     {'amount': 3, 'location': 'Korea', 'name': 'Hong', 'product': 'cleaner'},
     {'amount': 2, 'location': 'Korea', 'name': 'Lee', 'product': 'hardcase'},
     {'amount': 2, 'location': 'Korea', 'name': 'Lee', 'product': 'keycover'},
     {'amount': 5, 'location': 'China', 'name': 'Lyn', 'product': 'cleaner'},
     {'amount': 1, 'location': 'China', 'name': 'Lyn', 'product': 'mouse'},
     {'amount': 2, 'location': 'Korea', 'name': 'Park', 'product': 'battery'},
     {'amount': 1, 'location': 'USA', 'name': 'Smith', 'product': 'mouse'},
     {'amount': 1, 'location': None, 'name': 'Unknown', 'product': 'keyboard'},
     {'amount': 7, 'location': 'China', 'name': 'Xiaomi', 'product': 'battery'},
     {'amount': 1, 'location': 'China', 'name': 'Xiaomi', 'product': 'cable'},
     {'amount': 1, 'location': 'Japan', 'name': 'Yuki', 'product': 'manual'},
     {'amount': 2, 'location': None, 'name': 'anonymous', 'product': 'adopter'}]




```python
# 3-3 outer join
lst_buyitems.join(lst_customer.select('location', 'name'), on='name', how='outer')
```




    [{'amount': None, 'location': 'USA', 'name': 'Charse', 'product': None},
     {'amount': 1, 'location': 'Japan', 'name': 'Yuki', 'product': 'manual'},
     {'amount': 1, 'location': 'USA', 'name': 'Smith', 'product': 'mouse'},
     {'amount': 2, 'location': 'Korea', 'name': 'Lee', 'product': 'hardcase'},
     {'amount': 2, 'location': 'Korea', 'name': 'Lee', 'product': 'keycover'},
     {'amount': 7, 'location': 'China', 'name': 'Xiaomi', 'product': 'battery'},
     {'amount': 1, 'location': 'China', 'name': 'Xiaomi', 'product': 'cable'},
     {'amount': 1, 'location': None, 'name': 'Unknown', 'product': 'keyboard'},
     {'amount': 1, 'location': 'Korea', 'name': 'Hong', 'product': 'keyboard'},
     {'amount': 1, 'location': 'Korea', 'name': 'Hong', 'product': 'monitor'},
     {'amount': 3, 'location': 'Korea', 'name': 'Hong', 'product': 'mouse'},
     {'amount': 3, 'location': 'Korea', 'name': 'Hong', 'product': 'cleaner'},
     {'amount': 2, 'location': None, 'name': 'anonymous', 'product': 'adopter'},
     {'amount': 2, 'location': 'Korea', 'name': 'Park', 'product': 'battery'},
     {'amount': 5, 'location': 'China', 'name': 'Lyn', 'product': 'cleaner'},
     {'amount': 1, 'location': 'China', 'name': 'Lyn', 'product': 'mouse'}]



4-1.Utilities - Find Different in two different table - The Changed thing in table


```python
# changing to add two record, delete two record and modified a recored where name ==Lyn set age 28 
before = [
    {'name': 'Hong', 'gender': 'M', 'age': 18, 'location': 'Korea'},
    {'name': 'Charse', 'gender': 'M', 'age': 19, 'location': 'USA'},
    {'name': 'Lyn', 'gender': 'F', 'age': 29, 'location': 'China'},
]
after = [
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'},
    {'name': 'Xiaomi', 'gender': 'M', 'age': 15, 'location': 'China'},
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'},
]
```


```python
changes = ls.Listorm(before).get_changes(after, pk='name')
#pk: primary key is needed
```


```python
changes
```




    Changes(added=[Added(pk='Xiaomi', rows={'location': 'China', 'gender': 'M', 'name': 'Xiaomi', 'age': 15}), Added(pk='Park', rows={'location': 'Korea', 'gender': 'M', 'name': 'Park', 'age': 29})], deleted=[Deleted(pk='Hong', rows={'location': 'Korea', 'gender': 'M', 'name': 'Hong', 'age': 18}), Deleted(pk='Charse', rows={'location': 'USA', 'gender': 'M', 'name': 'Charse', 'age': 19})], updated=[Updated(pk='Lyn', before={'location': 'China', 'gender': 'F', 'name': 'Lyn', 'age': 29}, after={'location': 'China', 'gender': 'F', 'name': 'Lyn', 'age': 28}, where=['age'])])




```python
changes.added
```




    [Added(pk='Xiaomi', rows={'location': 'China', 'gender': 'M', 'name': 'Xiaomi', 'age': 15}),
     Added(pk='Park', rows={'location': 'Korea', 'gender': 'M', 'name': 'Park', 'age': 29})]




```python
changes.deleted
```




    [Deleted(pk='Hong', rows={'location': 'Korea', 'gender': 'M', 'name': 'Hong', 'age': 18}),
     Deleted(pk='Charse', rows={'location': 'USA', 'gender': 'M', 'name': 'Charse', 'age': 19})]




```python
changes.updated
```




    [Updated(pk='Lyn', before={'location': 'China', 'gender': 'F', 'name': 'Lyn', 'age': 29}, after={'location': 'China', 'gender': 'F', 'name': 'Lyn', 'age': 28}, where=['age'])]



4-2. Utilities - Read And Write to Excel, CSV

lst = ls.read_excel(file_name=None, file_contents=None, sheet_index=0, start_row=0, index=None)

Excel File or byte Content of Excel to Listorm object

lst = ls.read_csv(filename=None, encoding='utf-8',  fp=None, index=None)

CSV file or filepointer of CSV to Listorm object


```python
# saving date to excel or CSV
lst_customer = ls.Listorm(userTable)
excel_file_content = lst_customer.to_excel(filename=None) # If filnames is None, returns bytes of filecontents
csv_file_content = lst_customer.to_csv(filename=None) # If filnames is None, returns bytes of filecontents
```


```python

```
# listorm
# listorm
