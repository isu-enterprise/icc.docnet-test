from nose.plugins.skip import SkipTest
from nose.tools import assert_raises, nottest

from isu.webapp.interfaces import IApplication
from isu.webapp import app
from zope.component import getUtility, getSiteManager

from pyramid.paster import get_app
from icc.cellula.tasks import DocumentAcceptingTask, FileSystemScanTask

from pyramid.threadlocal import get_current_registry

from icc.docnet.tests import StopTests
import icc.docnet.tests.app as testapp

import pkg_resources
import os.path

DATA_PATH = pkg_resources.resource_filename(
    'icc.docnet.tests', '../../../../../DATA')
DATA_PATH = os.path.abspath(DATA_PATH)
SRC = os.path.join(DATA_PATH, "source")

application = get_app('icc.cellula-test-file.ini', name='main')


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

    def test_fs_scan(self):
        FileSystemScanTask().enqueue()

    def tearDown(self):
        pass


# This test set must be the last one in the source

class TestZStopQueue:

    def setUp(self):
        pass

    def test_stop_queue(self):
        event = StopTests(application)
        getSiteManager().notify(event)
