#!/usr/bin/env python3
'''
Main file for the Slashy application, the slash command framework for
Mattermost.
'''

from importlib import import_module

from flask import Flask

import settings

app = Flask(__name__)

for p in settings.PLUGINS:
    mod    = import_module('plugins.' + p)
    cls    = getattr(mod, p.title() + 'Plugin')

    kwargs = {x.lower().replace(p + '_', ''): getattr(settings, x) for x in dir(settings) if x.startswith(p.upper() + '_')}

    token = settings.TOKENS.get(p, None)
    if token is not None:
        kwargs['token'] = token

    webhook = settings.WEBHOOKS.get(p, None)
    if webhook is not None:
        kwargs['webhook'] = webhook

    obj = cls(**kwargs)
    app.add_url_rule('/' + p, p, obj, methods=['POST'])
