Plugins
=======

Giphy
-----

Usage
~~~~~

The giphy plugin can be used as slash command, for example by typing ``/giphy <text>``.

The plugin will lookup a matching gif image via the `Giphy API <https://giphy.com/>`_ and display it to all users in the channel.

Configuration
~~~~~~~~~~~~~

The giphy plugin requires minimal configuration:

- Create a new slash command in Mattermost to the URL endpoint ``/giphy``
- Configure the token for the giphy plugin in BabelFish (*optional but recommended*)
- Configure a Giphy API key and/or the image rating (*optional*)

Github
------

Usage
~~~~~

The github plugin implements a webhook to display Github notifications in a Mattermost channel.

The plugin makes use of Mattermost's ``attachments`` and Markdown features (e.g. commits will be displayed in a Markdown table).

Configuration
~~~~~~~~~~~~~

Configuration of the github plugin is required:

- Create a new incoming webhook in Mattermost
- Configure the webook URL for the github plugin in BabelFish
- Create a new webhook in Github and point it to the URL endpoint ``/github``
- Configure a github secret in BabelFish and in the GitHub webhook (*optional but recommended*)
