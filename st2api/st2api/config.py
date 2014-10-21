"""
Configuration options registration and useful routines.
"""

from oslo.config import cfg

import st2common.config as common_config

CONF = cfg.CONF


def _register_common_opts():
    common_config.register_opts()


def _register_app_opts():
    api_opts = [
        cfg.StrOpt('host', default='0.0.0.0', help='StackStorm Robotinator API server host'),
        cfg.IntOpt('port', default=9101, help='StackStorm Robotinator API server port'),
        cfg.ListOpt('allow_origin', default=['http://localhost:3000'],
                    help='List of origins allowed')
    ]
    CONF.register_opts(api_opts, group='api')

    pecan_opts = [
        cfg.StrOpt('root',
                   default='st2api.controllers.root.RootController',
                   help='Action root controller'),
        cfg.StrOpt('static_root', default='%(confdir)s/public'),
        cfg.StrOpt('template_path',
                   default='%(confdir)s/st2api/templates'),
        cfg.ListOpt('modules', default=['st2api']),
        cfg.BoolOpt('debug', default=True),
        cfg.BoolOpt('auth_enable', default=True),
        cfg.DictOpt('errors', default={'__force_dict__': True})
    ]
    CONF.register_opts(pecan_opts, group='api_pecan')

    logging_opts = [
        cfg.StrOpt('logging', default='conf/logging.conf',
                   help='location of the logging.conf file')
    ]
    CONF.register_opts(logging_opts, group='api')


def regsiter_opts():
    _register_common_opts()
    _register_app_opts()


def parse_args(args=None):
    CONF(args=args)


regsiter_opts()
