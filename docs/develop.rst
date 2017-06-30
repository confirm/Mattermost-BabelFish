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

A slash command plugin example
------------------------------

Creating new plugins is easy and straight-forward as you can see in the following example. 

Say hello
~~~~~~~~~

Let's say for some reason you want to create a plugin which simply writes ``Hello <name>`` to the channel. In the case, create a new file stored under ``plugins/hello.py`` with the following content:

.. code-block:: python

    from base import BaseSlashCommandPlugin


    class HelloPlugin(BaseSlashCommandPlugin):

        def request(self, username, text):
            return self.response('Hello ' + text)

Now add the plugin to the ``PLUGINS`` list in the ``settings.py`` file and you're ready to go!

Custom response username
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to send the message as a different user, set the ``username`` argument:

.. code-block:: python

            return self.response('Hello ' + text, username="Awesome Plugin")

Add plugin settings
~~~~~~~~~~~~~~~~~~~

Now let's say you want be able to configure the ``Hello`` string outside of your plugin.
Let's add a new parameter to the ``settings.py`` file.

Your plugin settings variables need to be…

- all uppercase
- prefixed with your plugin name and an underscore (``_``)
- not named ``<PLUGIN>_TOKEN`` or ``<PLUGIN>_WEBHOOK``

So let's add the following variable to the ``settings.py`` file:

.. code-block:: python

    HELLO_WORD = "Hello"

Now let's update our class accordingly and access that string:

.. code-block:: python

            return self.response('{} {}'.format(self.word, text)

As you can see, the variable defined in the settings is now available as instance property. Nice, isn't it?