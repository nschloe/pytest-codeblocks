code\_extract
=============

|Build Status| |codecov| |PyPi Version| |GitHub stars|

This is code\_extract, a Python tool for extracting code blocks markdown
files.

code\_extract can be used, for example, for automatically turning
snippets from a ``README.md`` into unit tests.

For example, the command

::
    code_extract input.md output.py

turns

::
    Lorem ipsum
    ```python
    some_code = 1
    ```

into

.. code:: python

    def test0():
        some_code = 1
        return


Distribution
~~~~~~~~~~~~

To create a new release

1. bump the ``__version__`` number,

2. publish to PyPi and GitHub:

   ::

       $ make publish

License
~~~~~~~

code\_extract is published under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

.. |Build Status| image:: https://travis-ci.org/nschloe/code_extract.svg?branch=master
   :target: https://travis-ci.org/nschloe/code_extract
.. |codecov| image:: https://codecov.io/gh/nschloe/code_extract/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nschloe/code_extract
.. |PyPi Version| image:: https://img.shields.io/pypi/v/code_extract.svg
   :target: https://pypi.python.org/pypi/code_extract
.. |GitHub stars| image:: https://img.shields.io/github/stars/nschloe/code_extract.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/nschloe/code_extract
