from nose.plugins.skip import SkipTest
from nose.tools import assert_raises, nottest

from isu.webapp.interfaces import IApplication
from isu.webapp import app
from zope.component import getUtility

from pyramid.paster import get_appsettings

import pkg_resources
import os.path

DATA_PATH = pkg_resources.resource_filename('icc.docnet.tests', '../DATA')
DATA_PATH = os.path.abspath(DATA_PATH)


def configurator(global_config, **settings):
    config = app.configurator(global_config, **settings)
    return app.create_application(config)


settings = get_appsettings('icc.cellula-test.ini', name='main')
application = configurator(settings)


#@SkipTest
class TestBasic:

    def setUp(self):
        pass

    def test_registry_works(self):
        assert getUtility(IApplication, name="application") == application

    def test_import_file(self):
        assert 0

    def tearDown(self):
        pass
