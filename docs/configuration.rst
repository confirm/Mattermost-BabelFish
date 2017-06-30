Configuration
=============

Settings
--------

All the configuration settings can be found in the ``babelfish/settings.py`` file.

.. tip:: 

    Please read the comments in ``settings.py`` for more informations about the configuration parameters.

.. caution::

    Do not change or overwrite ``settings.py``. Instead of it, use one of the methods described below.

Local settings
--------------

If you want to customize your settings in a file, we recommend you create a new ``settings_local.py`` file next to the ``settings.py`` file. This will automatically be loaded and it is ignored by git. You can overwrite all the settings variable within this file.

Environment variables
---------------------

As you might see in ``babelfish/settings.py``, most of the parameters can also be configured via environment variables.
