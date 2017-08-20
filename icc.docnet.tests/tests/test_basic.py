from nose.plugins.skip import SkipTest
from nose.tools import assert_raises, nottest

from isu.webapp.interfaces import IApplication
from isu.enterprise.interfaces import IConfigurator
from isu.webapp import app
from zope.component import getUtility, getSiteManager

from pyramid.paster import get_app, setup_logging
from icc.cellula.tasks import DocumentAcceptingTask, FileSystemScanTask, ScannedFilesProcessingTask

from pyramid.threadlocal import get_current_registry

from icc.docnet.tests import StopTests
import icc.docnet.tests.app as testapp

import pkg_resources
import os.path


INI = 'icc.cellula-test.ini'


DATA_PATH = pkg_resources.resource_filename(
    'icc.docnet.tests', '../../../../../DATA')
DATA_PATH = os.path.abspath(DATA_PATH)
SRC = os.path.join(DATA_PATH, "source")

application = get_app(INI, name='main')
setup_logging(INI)

import logging
logger = logging.getLogger("icc.cellula")


def bookname(name):
    return os.path.join(SRC, name)


class DebugFileSystemScanTask(FileSystemScanTask):

    def finalize(self):
        def_bunch_size = 10
        config = getUtility(IConfigurator, "configuration")
        bunch_size = config.getint(
            "scanner", "bunch_size", fallback=def_bunch_size)
        if self.files:
            files = self.files[:1]
            logger.debug("PROCESSING FILES {}".format(files))
            self.enqueue(ScannedFilesProcessingTask(files, bunch_size))


#@SkipTest
class TestBasic:

    def setUp(self):
        self.book1name = "French_ways_and_their_Meaning-Wharton.pdf"
        self.book1 = bookname(self.book1name)

    def test_registry_works(self):
        assert getUtility(IApplication, name="application") == application

    def test_import_file(self):
        assert self.book1.endswith("pdf")

    @nottest
    def test_book_processing(self):
        book = self.book1
        headers = {"File-Name": self.book1name}
        content = open(book, "rb").read()
        DocumentAcceptingTask(content, headers).enqueue(block=False, view=None)

    def test_fs_scan(self):
        DebugFileSystemScanTask().enqueue()

    def tearDown(self):
        pass


# This test set must be the last one in the source

class TestZStopQueue:

    def setUp(self):
        pass

    def test_stop_queue(self):
        event = StopTests(application)
        getSiteManager().notify(event)


def main():
    t1 = TestBasic()
    t1.setUp()

    te = TestZStopQueue()
    te.setUp()
    te.test_stop_queue()
    logger.info("Forced test stopped.")
    print(logger)


if __name__ == "__main__":
    main()
