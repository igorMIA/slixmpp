
# slixmpp.exceptions
# ~~~~~~~~~~~~~~~~~~~~
# Part of Slixmpp: The Slick XMPP Library
# :copyright: (c) 2011 Nathanael C. Fritz
# :license: MIT, see LICENSE for more details

class XMPPError(Exception):

    """
    A generic exception that may be raised while processing an XMPP stanza
    to indicate that an error response stanza should be sent.

    The exception method for stanza objects extending
    :class:`~slixmpp.stanza.rootstanza.RootStanza` will create an error
    stanza and initialize any additional substanzas using the extension
    information included in the exception.

    Meant for use in Slixmpp plugins and applications using Slixmpp.

    Extension information can be included to add additional XML elements
    to the generated error stanza.

    :param condition: The XMPP defined error condition.
                      Defaults to ``'undefined-condition'``.
    :param text: Human readable text describing the error.
    :param etype: The XMPP error type, such as ``'cancel'`` or ``'modify'``.
                  Defaults to ``'cancel'``.
    :param extension: Tag name of the extension's XML content.
    :param extension_ns: XML namespace of the extensions' XML content.
    :param extension_args: Content and attributes for the extension
                           element. Same as the additional arguments to
                           the :class:`~xml.etree.ElementTree.Element`
                           constructor.
    :param clear: Indicates if the stanza's contents should be
                  removed before replying with an error.
                  Defaults to ``True``.
    :param silent: Indicates if the stanza's error should be silenced and
                  do not send an error to the XMPP server.
                  Defaults to ``False``.
    """

    def __init__(self, condition='undefined-condition', text='',
                etype='cancel', extension=None, extension_ns=None,
                extension_args=None, clear=True, silent=False):
        if extension_args is None:
            extension_args = {}

        self.condition = condition
        self.text = text
        self.etype = etype
        self.clear = clear
        self.silent = silent
        self.extension = extension
        self.extension_ns = extension_ns
        self.extension_args = extension_args

    def format(self):
        """
        Format the error in a simple user-readable string.
        """
        text = [self.etype, self.condition]
        if self.text:
            text.append(self.text)
        if self.extension:
            text.append(self.extension)
        # TODO: handle self.extension_args
        return ': '.join(text)


class IqTimeout(XMPPError):

    """
    An exception which indicates that an IQ request response has not been
    received within the alloted time window.
    """

    def __init__(self, iq, silent=False):
        super().__init__(
                condition='remote-server-timeout',
                etype='cancel',
                silent=silent)

        #: The :class:`~slixmpp.stanza.iq.Iq` stanza whose response
        #: did not arrive before the timeout expired.
        self.iq = iq


class IqError(XMPPError):

    """
    An exception raised when an Iq stanza of type 'error' is received
    after making a blocking send call.
    """

    def __init__(self, iq, silent=False):
        super().__init__(
                condition=iq['error']['condition'],
                text=iq['error']['text'],
                etype=iq['error']['type'],
                silent=silent)

        #: The :class:`~slixmpp.stanza.iq.Iq` error result stanza.
        self.iq = iq


class PresenceError(XMPPError):
    """
    An exception raised in specific circumstances for presences
    of type 'error' received.
    """
    def __init__(self, pres, silent=False):
        super().__init__(
            condition=pres['error']['condition'],
            text=pres['error']['text'],
            etype=pres['error']['type'],
            silent=silent
        )
        self.presence = pres
