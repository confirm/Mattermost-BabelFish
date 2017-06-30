The Docs
========

The purpose of the docs is the documentation of the Mattermost BabelFish framework. We're building the docs based on `Sphinx Doc <http://www.sphinx-doc.org/en/stable/>`_, the Python documentation tool.

Requirements
------------

Before you can work with the docs you've to make sure you've installed all required Python packages / libraries. To install all dependencies you can use the `requirements file <requirements.txt>`_.

It's recommended to use a **Python virtualenv** and place it in ``.venv`` or symlink it to ``.venv``:

.. code-block:: bash

  # Install virtualenv.
  pip install virtualenv virtualenvwrapper

  # Create new virtualenv and activate it.
  virtualenv .venv
  source .venv/bin/activate

  # Install Python dependencies.
  pip install -r requirements.txt

If you **don't want to use a virtualenv** you can simply run the following command to install the dependencies in your system site-packages:

.. code-block:: bash

    pip install -r requirements.txt

Building the HTML docs
----------------------

The built documentation is not included in the git repository.
However, you can easily **build the documentation** by running the following command:

.. code-block:: bash

    make html

.. note::

  In case you get an error that the ``sphinx-build`` command was not found, you've to make sure you've installed the `requirements <#requirements>`_ and loaded the virtualenv by executing ``source .venv/bin/activate``.
