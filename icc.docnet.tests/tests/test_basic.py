from nose.plugins.skip import SkipTest
from nose.tools import assert_raises, nottest

from isu.webapp.interfaces import IApplication
from isu.webapp import app
from zope.component import getUtility

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
        assert getUtility(IApplication, name="application") == application

    def tearDown(self):
        pass
