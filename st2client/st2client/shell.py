"""
Command-line interface to Stanley
"""

import sys
import argparse
import logging

from st2client import models
from st2client.client import Client
from st2client.commands import resource
from st2client.commands import action
from st2client.commands import datastore


LOG = logging.getLogger(__name__)


class Shell(object):

    def __init__(self):

        # Set up of endpoints is delayed until program is run.
        self.client = None

        # Set up the main parser.
        self.parser = argparse.ArgumentParser(
            description='CLI for Stanley, an automation platform by '
                        'StackStorm. http://stackstorm.com')

        # Set up general program options.
        self.parser.add_argument(
            '--url',
            action='store',
            dest='url',
            default=None,
            help='Base URL for the API servers. Assumes all servers uses the '
                 'same base URL and default ports are used. Get ST2_BASE_URL'
                 'from the environment variables by default.'
        )

        self.parser.add_argument(
            '--api-url',
            action='store',
            dest='api_url',
            default=None,
            help='URL for the API server. Get ST2_API_URL'
                 'from the environment variables by default.'
        )

        self.parser.add_argument(
            '--datastore-url',
            action='store',
            dest='datastore_url',
            default=None,
            help='URL for the Datastore API server. Get ST2_DATASTORE_URL'
                 'from the environment variables by default.'
        )

        # Set up list of commands and subcommands.
        self.subparsers = self.parser.add_subparsers()
        self.commands = dict()

        self.commands['key'] = datastore.KeyValuePairBranch(
            'Key value pair is used to store commonly used configuration '
            'for reuse in sensors, actions, and rules.',
            self, self.subparsers)

        self.commands['trigger'] = resource.ResourceBranch(
            models.Trigger,
            'An external event that is mapped to a stanley input. It is the '
            'stanley invocation point.',
            self, self.subparsers)

        self.commands['rule'] = resource.ResourceBranch(
            models.Rule,
            'A specification to invoke an "action" on a "trigger" selectively '
            'based on some criteria.',
            self, self.subparsers)

        self.commands['action'] = action.ActionBranch(
            'An activity that happens as a response to the external event.',
            self, self.subparsers)
        self.commands['runner'] = resource.ResourceBranch(
            models.RunnerType,
            'Runner is a type of handler for a specific class of actions.',
            self, self.subparsers, read_only=True)
        self.commands['run'] = action.ActionRunCommand(
            models.Action, self, self.subparsers, name='run', add_help=False)
        self.commands['execution'] = action.ActionExecutionBranch(
            'An invocation of an action.',
            self, self.subparsers)

    def get_client(self, args):
        endpoints = dict()
        if args.url:
            endpoints['base_url'] = args.url
        if args.api_url:
            endpoints['api_url'] = args.api_url
        if args.datastore_url:
            endpoints['datastore_url'] = args.datastore_url
        return Client(**endpoints)

    def run(self, argv):
        try:
            # Parse command line arguments.
            args = self.parser.parse_args(args=argv)

            # Set up client.
            self.client = self.get_client(args)

            # Execute command.
            args.func(args, argv=argv)

            return 0
        except Exception as e:
            print 'ERROR: %s\n' % e.message
            return 1


def main(argv=sys.argv[1:]):
    return Shell().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
