Run
===

Flask server
------------

For testing or debugging you can run the Flask app directly:

.. code-block:: bash

    FLASK_APP=babelfish.py flask run

.. hint::
    
    Please note that you must be in the ``babelfish/`` directory and that you might need to activate your virtualenv first.

WSGI
----

To run BabelFish in production, it's recommended that you use a proper WSGI application server.
We're using `uWSGI <https://github.com/unbit/uwsgi>`_ for our installation.

Here are to most important bits of our config:

.. code-block:: ini

    [uwsgi]
    socket     = <path to socket>
    plugins    = python3
    chdir      = <path to babelfish directory>
    virtualenv = <path to virtualenv directory>
    module     = babelfish:app
    # more config…

