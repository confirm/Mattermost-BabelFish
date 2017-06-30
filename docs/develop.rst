Developing plugins
==================

Naming
------

Plugins should be named properly and obviousely according to their function.
For example:

- Desired slash command: ``/giphy`` _(can still be customised in your Mattermost integration)_
- Plugin name: ``giphy``
- URL endpoint: ``/giphy``
- Python plugin module & class: ``plugins.giphy.GiphyPlugin``
- Settings: ``GIPHY_*``

As you can see, the name of the plugin matches the URL endpoint and the Python module. The class itself is properly written in ``UpperCamelCase`` with the suffix ``…Plugin``.

Base plugin classes
-------------------

Ensure your plugin class is inherting from one of the following classes:

- ``plugins.base.BaseSlashCommandPlugin`` for slash command plugins
- ``plugins.base.BaseWebhookPlugin`` for webhook plugins

These classes implement the required parsing of the requests & responses, as well as the checks of the mattermost tokens.

How your class should look like
-------------------------------

In case you want to add a plugin for the slash command `/example`, your plugin should be stored under `plugins/example.py` and it should look like this:

.. code-block:: python

    from base import BaseSlashCommandPlugin


    class ExamplePlugin(BaseSlashCommandPlugin):

        def request(self, username, text):
            #
            # your code goes here
            #
            return self.response('Your response text')

- If you want to **overwrite the username** of the response, just set the ``username`` attribute of the ``response()`` method. 
- If you want your message to be **displayed only to the user** which has executed the slash command, set the ``response_type`` attribute of the ``response()`` method to ``ephermal``.

Settings
--------

Just add your plugin settings to the ``settings.py`` file. 
Your settings variables need to be all uppercase and prefixed with your plugin name and an underscore (``_``).

If you've done this properly, you should've direct access to the settings in your plugin!  
For example, let's say you've a plugin called ``foo`` with the following settings:

.. code-block:: python

    FOO_SPAM = "eggs"

In your class ``FooPlugin`` you should've access to the settings as follows:

.. code-block:: python

    class FooPlugin(BaseSlashCommandPlugin):

        def request(self, username, text):
            print(self.foo)     # should print "spam"
            # …
