'''
About
=====================




-------------------

* process of list of dict, a form that is often dealt with

.. code-block::

   
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



'''

from .api import *
from .core import *

