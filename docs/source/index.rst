=====================
Listorm documentation
=====================


About
=====

* listorm is a simple library that handles dict and list of dict data structures
* Provides APIs for code patterns frequently used in dict and list processing
* It has been implemented so that some key keywords and functions of SQL can be used similarly

Installation
============


.. code-block:: console

    >>> pip install listorm


.. warning::

    1.0.0 or later version is not compatible previous 0.x.x version

    If you want to use older version as 0.x,


    .. code-block::
        
        >>> pip install listorm==0.2.16
    


listorm at a glance
===================



select
-----------------------


    .. literalinclude:: examples/select.py


.. note::
    How to use the callback function used in listom
        - Pass the keys (columns) of the values, to retrieve from the row as arguments to the callback
        - The callback function is used to change or determine values such as select, filtering, and update except **groupby** aggregate callback


        .. code-block::

            user = [
                {'name': 'Hong', 'country': 'de', 'age': 55},
                {'name': 'abc', 'country': 'br', 'age': 30},
            ]

            # Pass the keys to be referenced in the row as an argument to the callback function

            callback1 = lambda name: name.upper()
            
            def callback2(country):
                return country
            
            def callback3(name, country):
                return f"{country}/{name}"

        - In case of it need to refer to the entire row for example, a space exists in the key name


        .. code-block::

            where = lambda **row: row['age of ultron'] > 18


update
--------------


    .. literalinclude:: examples/update.py

      
orderby
---------------


    .. literalinclude:: examples/orderby.py


groupby
---------------


    .. literalinclude:: examples/groupby.py


join
---------------


    .. literalinclude:: examples/join.py







.. toctree::
   :maxdepth: 2
   :caption: Listorm API:


   module/orm
   module/asdict
   module/forlist
   


