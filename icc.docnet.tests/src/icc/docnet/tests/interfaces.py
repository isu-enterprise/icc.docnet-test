from zope.interface import Interface, Attribute


class IStopTestEvent(Interface):
    """Defines an event denoting end of test sequence"""

    app = Attribute("Application that about to be stopped")
