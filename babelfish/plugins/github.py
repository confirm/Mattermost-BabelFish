'''
Implementation of the GitHubPlugin class.

Please read the class description for more informations.
'''

import hmac
from hashlib import sha1

from .base import BaseWebhookPlugin


class GithubException(Exception):
    pass


class GithubEventNotImplemented(GithubException):

    def __init__(self, event):
        self.event = event

    def __str__(self):
        return 'Github event {} not implemented'.format(self.event)


class GithubActionNotImplemented(GithubException):

    def __init__(self, event, action):
        self.action = action

    def __str__(self):
        return 'Github action {} of event {} not implemented'.format(self.action, self.event)


class GithubActionIgnored(GithubException):

    def __init__(self, event, action):
        self.action = action

    def __str__(self):
        return 'Github action {} of event {} ignored'.format(self.action, self.event)


class GithubPlugin(BaseWebhookPlugin):
    '''
    The github plugin will retreive a GitHub webhook, re-format it for
    Mattermost and forward it to an incoming Mattermost webhook.

    This is basically a wrapper / proxy service for GitHub to Mattermost.
    '''

    def validate_signature(self, request):
        '''
        Validates the retreived signature with the configured secret.
        '''
        if not self.secret:
            return

        sig = request.headers.get('X-Hub-Signature', None)
        assert sig, 'Missing X-Hub-Signature'

        sig2 = hmac.new(self.secret.encode(), digestmod=sha1)
        sig2.update(request.data)
        assert '=' in sig, 'Invalid X-Hub-Signature'
        assert sig2.hexdigest() == sig.split('=')[1], 'X-Hub-Signature missmatch'

    def request(self, request):
        '''
        Retreive the GitHub webhook, extract all the required informations and
        call the appropriate Mattermost webhook with all the informations.
        '''
        self.validate_signature(request)

        event = request.headers.get('X-Github-Event', None)
        assert event is not None, 'Missing X-Github-Event'

        data = request.json
        assert data, 'Missing JSON data / payload'

        try:
            clsname = 'Github{}Event'.format(
                event.replace('_', ' ').title().replace(' ', '')
            )
            try:
                cls  = globals()[clsname]
            except KeyError:
                raise GithubEventNotImplemented(event)
            obj = cls(data)

            kwargs = {'text': str(obj)}
            if hasattr(obj, 'attachment'):
                kwargs['attachments'] = [obj.attachment]

            return self.webhook_request(**kwargs)

        except GithubException as e:
            return str(e)


class GithubEvent:
    '''
    This is the base class for all Github events. It provides some useful
    methods to create appropriate messages in Mattermost.
    '''

    def __init__(self, data):
        self.data        = data

    def create_user_link(self, user):
        '''
        Creates a Markdown-formatted link to a GitHub user by extracting the
        `login` and `html_url` attributes from the provided `user` dict.
        '''
        return '[{login}]({html_url})'.format(**user)

    @property
    def sender(self):
        '''
        Property which returns a Markdown-formatted link to the sender GitHub
        user.
        '''
        return self.create_user_link(self.data['sender'])

    @property
    def repository_url(self):
        '''
        Property which extracts and returns the repository URL.
        '''
        return self.data['repository']['html_url']

    @property
    def repository(self):
        '''
        Property which returns a Markdown-formatted link to the GitHub
        repository.
        '''
        return '[{full_name}]({html_url})'.format(**self.data['repository'])

    def oneline(self, text):
        '''
        Method which shortens multi-line texts to the first line.
        '''
        text  = text.strip()
        if not text:
            return ''
        short = text.split('\n')[0]
        if short != text:
            short += '…'
        return short


class GithubCommitCommentEvent(GithubEvent):

    def __str__(self):
        action               = self.data['action']
        comment              = self.data['comment']
        comment['commit_id'] = comment['commit_id'][:7]

        return '{sender} {action} a comment on commit [`{commit_id}`]({html_url}) in {repository}'.format(
            sender=self.sender,
            action=action,
            repository=self.repository,
            **comment
        )

    @property
    def attachment(self):
        return {
            'text': self.data['comment']['body']
        }


class GithubCreateEvent(GithubEvent):

    def __str__(self):
        ref      = self.data['ref']
        ref_type = self.data['ref_type']

        return '{sender} created {ref_type} `{ref}` in {repository}'.format(
            sender=self.sender,
            ref=ref,
            ref_type=ref_type,
            repository=self.repository,
        )


class GithubDeleteEvent(GithubEvent):

    def __str__(self):
        ref      = self.data['ref']
        ref_type = self.data['ref_type']

        return '{sender} deleted {ref_type} `{ref}` in {repository}'.format(
            sender=self.sender,
            ref=ref,
            ref_type=ref_type,
            repository=self.repository,
        )


class GithubIssueEvent(GithubEvent):

    def __str__(self):
        issue  = self.data['issue']
        action = self.data['action']
        label  = self.data.get('label')

        text = '{sender} {action} an issue [#{number} {title}]({html_url}) in {repository}'.format(
            sender=self.sender,
            action=action,
            repository=self.repository,
            **issue
        )

        if action == 'assigned':
            text += ' to {assignee}'.format(
                assignee=self.create_user_link(self.data['assignee'])
            )
        elif action == 'labeled':
            text += ' with `{label}`'.format(label=label['name'])
        elif action == 'unlabeled':
            text += ' from `{label}`'.format(label=label['name'])

        return text

    @property
    def attachment(self):
        issue  = self.data['issue']
        action = self.data['action']

        if 'opened' in action:
            return {
                'title': issue['title'],
                'text': issue['body'],
            }


class GithubIssueCommentEvent(GithubEvent):

    def __str__(self):
        issue  = self.data['issue']
        action = self.data['action']

        return '{sender} {action} a comment on issue [#{number} {title}]({html_url}) in {repository}'.format(
            sender=self.sender,
            action=action,
            repository=self.repository,
            **issue
        )

    @property
    def attachment(self):
        data = {
            'title': self.data['issue']['title'],
            'text': self.data['comment']['body']
        }

        if data['text']:
            return data


class GithubPullRequestEvent(GithubEvent):

    def __str__(self):
        pull_request = self.data['pull_request']
        action       = self.data['action']

        if action == 'closed' and pull_request['merged']:
            action = 'merged'

        text = '{sender} {action} a pull request [#{number} {title}]({html_url}) in {repository}'.format(
            sender=self.sender,
            action=action,
            repository=self.repository,
            **pull_request
        )

        if action == 'assigned':
            text += ' to {assignee}'.format(
                assignee=self.create_user_link(self.data['assignee'])
            )

        return text

    @property
    def attachment(self):
        pull_request = self.data['pull_request']
        action       = self.data['action']

        if 'opened' in action:
            return {
                'title': pull_request['title'],
                'text': pull_request['body'],
            }


class GithubPullRequestReviewCommentEvent(GithubEvent):

    def __str__(self):
        pull_request = self.data['pull_request']
        action       = self.data['action']

        return '{sender} {action} a comment on pull request [#{number} {title}]({html_url}) in {repository}'.format(
            sender=self.sender,
            action=action,
            repository=self.repository,
            **pull_request
        )

    @property
    def attachment(self):
        data = {
            'title': self.data['pull_request']['title'],
            'text': self.data['comment']['body']
        }

        if data['text']:
            return data


class GithubPushEvent(GithubEvent):

    def __str__(self):
        branch        = self.data['ref'].split('/')[2]
        branch_url    = '{url}/tree/{branch}'.format(url=self.repository_url, branch=branch)
        commits       = self.data['commits']
        commits_count = len(commits)
        commits_str   = 'commits' if commits_count > 1 else 'commit'

        if commits_count == 0:
            raise GithubActionIgnored('push', 'commit_zero')

        text = '{sender} pushed {commits_count} {commits_str} to [{branch}]({branch_url}) at {repository}\n\n'.format(
            sender=self.sender,
            commits_count=commits_count,
            commits_str=commits_str,
            branch=branch,
            branch_url=branch_url,
            repository=self.repository,
        )

        text += '| SHA | Message |\n'
        text += '| --- | ------- |\n'

        for commit in commits:
            commit['id'] = commit['id'][:7]
            commit['message'] = self.oneline(commit['message'])
            text += '| [`{id}`]({url}) | {message} |\n'.format(**commit)

        return text
