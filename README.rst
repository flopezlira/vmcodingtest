======
vmware
======

This is the vmware application.


Minimum Requirements
====================

- Python 3.5+


Optional Requirements
=====================

- `pytest`_ (for running the test suite)
- `pdoc`_ (for generating documentation)
- `black`_ (formatter)
- `pycodestyle`_ (Python style guide checker)
- `isort`_ (sort imports alphabetically)

Basic Setup
===========

Install for the current user:

.. code-block:: console

    # Create virtual env
    # For Linux and Mac
    $ python3 -e venv venv
    $ source venv/bin/activate
    # For windows
    c:\>py -e venv venvwin
    c:\>py -m venv venvwin\Scripts\activate
    # Install requirements
    pip install -r requirements.txt
    # install requests
    # For Linux and Mac
    sudo apt-get install python3-requests
    # For windows
    pip install requests



Run the application:

.. code-block:: console

    # For Linux and Mac at vmware directory
    $ python3 src/main.py <args>
    # For Windows
    c:\> py

Run the test suite:

.. code-block:: console

    for Linux
    $ sh quality_check.sh

    for Windows
    $ quality_check.bat

Build documentation:

.. code-block:: console

    from vmware directory
    $ pdoc src/*.py
