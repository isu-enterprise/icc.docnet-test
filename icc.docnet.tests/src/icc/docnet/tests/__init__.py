# Example package with a console entry point
from __future__ import print_function
from zope.interface import implementer
from .interfaces import IStopTestEvent


def includeme(global_config, **settings):
    from .app import configuration
    return configuration(global_config, **settings)


@implementer(IStopTestEvent)
class StopTests(object):
    def __init__(self, app):
        self.app = app
