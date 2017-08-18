from zope.component import getUtility
from icc.cellula.interfaces import IRTMetadataIndex
from icc.cellula import get_storage, default_storage

import logging
logger = logging.getLogger("icc.cellula")


def clean_indexes(event):
    store = getUtility(IRTMetadataIndex, "elastic")
    marc = getUtility(IRTMetadataIndex, "marc")
    indices = [store, marc]
    for i in indices:
        i.remove_index()
        logger.debug("Removed index '{}'.".format(i.index))


def clear_storages(event):
    content = default_storage()
    #locations = get_storage("locations")
    #storages = [content, locations]
    storages = [content]
    for s in storages:
        s.begin()
        s.clear()
        s.commit()
        logger.debug("Cleared storage '{}'({})".format(s.storage_name,
                                                       s.__class__.__name__))


def bad_subscriber(event):
    raise RuntimeError("This is a bad subscriber.")
