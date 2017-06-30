import os

#
# Plugins.
#
# Please add all the desired plugins to the  below. Plugins not listed here
# won't be activated and won't work.
#

PLUGINS = (
    'giphy',
    'github',
)

#
# Mattermost tokens.
#
# Register your slash commands and configure the returned Mattermost tokens
# in the dict below. If you don't specify a token for a plugin, the token of the
# incoming request won't be verified at all. This means, anyone who has access
# to the HTTP(S) service can use the plugin implementation.
#

TOKENS = {
    'giphy': os.environ.get('GIPHY_TOKEN', ''),
}

#
# Mattermost webhooks.
#
# Register your incoming webhooks in the dict below. If you don't specify a
# webhook URL for a plugin, the plugin won't work as it obviousely doesn't know
# where the data should be sent to.
#

WEBHOOKS = {
    'github': os.environ.get('GITHUB_WEBHOOK', ''),
}

#
# Giphy settings.
#
# Define your giphy settings right below. Please note that the default key is
# Giphy's official beta key.
#

GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY', 'dc6zaTOxFJmzC')
GIPHY_RATING  = os.environ.get('GIPHY_RATING', 'pg')

#
# GitHub settings.
#
# Please note that the secret is optional. However, if you don't define a
# secret, everybody who has access to your URL endpoint can send data to your
# Mattermost webhook.
#

GITHUB_SECRET = os.environ.get('GITHUB_SECRET', '')


try:
    from settings_local import *
except ImportError:
    pass
