from nose.plugins.skip import SkipTest
from nose.tools import assert_raises, nottest

from isu.webapp.interfaces import IApplication
from isu.webapp import app
from zope.component import getUtility

from pyramid.paster import get_appsettings
from icc.cellula.tasks import DocumentAcceptingTask

import pkg_resources
import os.path

DATA_PATH = pkg_resources.resource_filename(
    'icc.docnet.tests', '../../../../../DATA')
DATA_PATH = os.path.abspath(DATA_PATH)
SRC = os.path.join(DATA_PATH, "source")


def configurator(global_config, **settings):
    config = app.configurator(global_config, **settings)
    return app.create_application(config)
    pass


settings = get_appsettings('icc.cellula-test.ini', name='main')
application = configurator(settings)


def bookname(name):
    return os.path.join(SRC, name)

#@SkipTest


class TestBasic:

    def setUp(self):
        self.book1name = "French_ways_and_their_Meaning-Wharton.pdf"
        self.book1 = bookname(self.book1name)

    def test_registry_works(self):
        assert getUtility(IApplication, name="application") == application

    def test_import_file(self):
        assert self.book1.endswith("pdf")

    def test_book_processing(self):
        book = self.book1
        headers = {"File-Name": self.book1name}
        content = open(book, "rb").read()
        DocumentAcceptingTask(content, headers).enqueue(block=False, view=None)

    def tearDown(self):
        pass
