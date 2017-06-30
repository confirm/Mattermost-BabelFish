'''
Implementation of the GiphyPlugin class.

Please read the class description for more informations.
'''

import requests

from .base import BaseSlashCommandPlugin


class GiphyPlugin(BaseSlashCommandPlugin):
    '''
    The giphy plugin will take the retreived text to request the Giphy API
    (https://giphy.com/) for a matching GIF image. If an image was found, it
    will be displayd in the Mattermost channel for all users.
    '''

    def request(self, username, text):
        '''
        Requests the Giphy API and returns the URL to the gif.
        '''
        p = {
            's': text,
            'rating': self.rating,
            'api_key': self.api_key,
        }

        r = requests.get('https://api.giphy.com/v1/gifs/translate', params=p)
        if r.status_code != 200:
            raise Exception('Giphy API error, text={}, status={}, response={}'.format(
                text,
                r.status_code,
                r.text
            ))

        json = r.json()
        if not json.get('data', None):
            return self.response(
                'No GIF found matching your text',
                response_type='ephemeral'
            )

        return self.response(
            json['data']['images']['original']['url'],
            username=username
        )
