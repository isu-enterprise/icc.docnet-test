from nose.plugins.skip import SkipTest
from nose.tools import assert_raises, nottest
from pyramid.config import Configurator
from zope.component import getGlobalSiteManager
from zope.interface import directlyProvides
from isu.webapp.interfaces import IConfigurationEvent, IApplication

from isu.webapp import app

from isu.enterprise.configurator import createConfigurator

from pyramid.paster import get_appsettings


def configurator(global_config, **settings):
    config = app.configurator(global_config, **settings)
    return app.create_application(config)


settings = get_appsettings('icc.cellula-test.ini', name='main')
application = configurator(settings)


#@SkipTest
class TestBasic:

    def setUp(self):
        pass

    def test_something(self):
        assert 1 + 1 == 2

    def tearDown(self):
        pass
