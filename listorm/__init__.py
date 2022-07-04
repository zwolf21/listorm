'''
About
=====================

* listorm is a simple library that handles dict and list of dict data structures
* Provides APIs for code patterns frequently used in dict and list processing
* It has been implemented so that some key keywords and functions of SQL can be used similarly


listorm at a glance
-------------------

* process of list of dict, a form that is often dealt with

.. code-block::

   # select

   from listorm import Listorm, aslambda, read_excel, read_csv

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

   # if it need to bd check for unique constraint
   # ls = Listorm(userTable, uniques=('name', 'location'))

   # ls.select(['name', 'age', 'location']) or
   
   # selecting
   >>> ls.select('name', 'age', 'location').print()
    {'name': 'Hong', 'age': 18, 'location': 'Korea'}
    {'name': 'Charse', 'age': 19, 'location': 'USA'}
    {'name': 'Lyn', 'age': 28, 'location': 'China'}
    {'name': 'Xiaomi', 'age': 15, 'location': 'China'}
    {'name': 'Park', 'age': 29, 'location': 'Korea'}
    {'name': 'Smith', 'age': 17, 'location': 'USA'}
    {'name': 'Lee', 'age': 12, 'location': 'Korea'}

    # filtering
   >>> ls.select(where=lambda row: row.age > 20).print()
    {'name': 'Lyn', 'gender': 'F', 'age': 28, 'location': 'China'}
    {'name': 'Park', 'gender': 'M', 'age': 29, 'location': 'Korea'}
    # select and filter
   >>> ls.select('name', 'age', 'location', where=lambda row: row.age > 20).print()
    {'name': 'Lyn', 'age': 28, 'location': 'China'}
    {'name': 'Park', 'age': 29, 'location': 'Korea'}


.. code-block::

   # retriving values

   >>> ls.values('name', 'gender')
   [('Hong', 'M'),
   ('Charse', 'M'),
   ('Lyn', 'F'),
   ('Xiaomi', 'M'),
   ('Park', 'M'),
   ('Smith', 'M'),
   ('Lee', 'F')]


.. code-block::

   # update

   >> ls.update()


'''

from .api import *
from .core import *

