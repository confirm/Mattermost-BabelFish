Introduction
============

What is BabelFish?
------------------

BabelFish is a **framework** for Mattermost **webhooks** and **slash commands**. See it as a central hub for all your integrations. BabelFish is also…

- written in `Python <https://python.org>`_
- using `Flask <https://flask.pocoo.org/>`_
- modular
- plugin-based
- well documented

Why BabelFish?
--------------

Let me explain why we created BabelFish.

We switched from Slack to Mattermost a while ago. Slack supports a lot of integrations for popular services. Unfortunately, Mattermost isn't that mature (yet) and will only support properitary webhooks and slash commands.

This means, if your service doesn't talk Mattermost JSON-ish, the integration won't work out of the box. Thus, you need something in between Mattermost and your application. And this is exactly why BabelFish was created.

BabelFish is a central hub which translates between the Mattermost JSON API and 3rd party services like Github and Giphy. Of course there are other alternatives out there, but most of them aim at exactly one function and you'll end up with running multiple application servers, each configured differently.

Another reason why we've created BabelFish is the open-source community. We love open-source and we want to give something back. We really hope that you like the concept and we'd love to see people developing more plugins.
