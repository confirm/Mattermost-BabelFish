'''
Implementation of the BasePlugin class.

Please read the class description for more informations.
'''

__all__ = (
    'BaseSlashCommandPlugin',
    'BaseWebhookPlugin',
)

import json
import requests

from flask import request, Response


class BasePlugin:
    '''
    Base plugin which provides the most fundamental methods to work with the
    Mattermost API.

    This class is inherited by the BaseSlashCommand and BaseWebhookPlugin
    classes.
    '''

    def __init__(self, **kwargs):
        '''
        Class constructor which simply accepts several keyword arguments and
        stores them as instance properties. The properties are most likely
        settings for the concrete plugin.
        '''
        for p, v in kwargs.items():
            setattr(self, p, v)


class BaseSlashCommandPlugin(BasePlugin):
    '''
    Base class for slash command plugins, which provides fundamental methods
    to work with Mattermost slash commands.

    The whole magic starts within the __call__() method of this class, which is
    retreiving the HTTP JSON request sent by a Mattermost slash command. In case
    a token is defined in the class constructor, the method will validate the
    retreived token in the HTTP request with the token of the class constructor.

    If the token doesn't match, the method will raise an exception.

    If no token was defined in the constructor or the retreived token matches
    the one of the constructor, the class will call the request() method, which
    is implemented by the concrete plugin class. It will also pass the keyword
    arguments `user` and `text` to the request() method.

    As mentioned in the last paragraph, the request() method is mandatory and
    it MUST be implemented by the concrete plugin class. The method can be used
    to handle the request and finally return the desired response.

    Please note that you might want to use the response() method to create a
    proper Mattermost-compatible response.
    '''

    def __init__(self, token, **kwargs):
        '''
        Mattermost slash commands have an (optional) secure token, which ensures
        that the incoming command is really from an authorized Mattermost
        installation.

        Therefore this class must be configured with at least a token and
        optional keyword arguments, which will be stored as instance properties.
        '''
        self.token = token
        super(BaseSlashCommandPlugin, self).__init__(**kwargs)

    def __call__(self):
        '''
        Method which will be executed when the class instance / object is
        called.

        This method is most likely the registered Flask URL endpoint and it will
        be called automatically by Flask, when a request for the appropriate
        plugin is made.
        '''
        data  = request.form

        token = self.token
        if token:
            if 'token' not in data:
                raise Exception('Missing token in request data')
            elif data['token'] != token:
                raise Exception('Invalid mattermost token received')

        username = data.get('user_name')
        text     = data.get('text', '').strip()

        if not text:
            return self.response(
                'Please enter a text after the slash command',
                response_type='ephemeral'
            )

        return self.request(username=username, text=text)

    def response(self, text, response_type='in_channel', **kwargs):
        '''
        Creates a proper Mattermost-compatible response for the requester.
        '''
        data = {
            'text': text,
            'response_type': response_type
        }

        for p, v in kwargs.items():
            data[p] = v

        r = Response(content_type='application/json')
        r.set_data(json.dumps(data))

        return r


class BaseWebhookPlugin(BasePlugin):
    '''
    Base class for webhook plugins, which provides fundamental methods to work
    with Mattermost webhooks.

    A webhook plugin is most likely a proxy between a properitary web service
    and an incoming Mattermost webhook. This is used when the 3rd-party web
    service doesn't "talk Mattermost JSONish" and Mattermost can't understand
    the data of the 3rd-party web service. Therefore this class MUST be
    instantiated with a proper Mattermost webhook URL.

    The whole magic starts within the __call__() method of this class, which is
    retreiving a HTTP request sent by a client or service, which will then be
    forwarded to the request() method. It will also forward the Flask request
    object as `request` keyword argument to the request() method.

    As mentioned in the last paragraph, the request() method is mandatory and
    it MUST be implemented by the concrete plugin class. The method can be used
    to handle the request and finally return the desired response.

    Please note that you might want to use the webhook() method to call the
    appropriate Mattermost webhook.
    '''

    def __init__(self, webhook, **kwargs):
        '''
        Incoming webhook plugins
        '''
        self.webhook = webhook
        super(BaseWebhookPlugin, self).__init__(**kwargs)

    def __call__(self):
        '''
        Method which will be executed when the class instance / object is
        called.

        This method is most likely the registered Flask URL endpoint and it will
        be called automatically by Flask, when a request for the appropriate
        plugin is made.
        '''
        return self.request(request=request)

    def webhook_request(self, text, **kwargs):
        '''
        Calls the registered Mattermost webhook.
        '''
        if not self.webhook:
            raise Exception('Invalid webhook for {}'.format(__class__.__name__))

        data = {
            'text': text,
        }

        for p, v in kwargs.items():
            data[p] = v

        requests.post(self.webhook, json=data)

        return text
