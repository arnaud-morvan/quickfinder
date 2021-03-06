#-----------------------------------------------------------
#
# QGIS Quick Finder Plugin
# Copyright (C) 2014 Denis Rouzaud, Arnaud Morvan
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------
import urllib, urllib2, json

from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, \
                            QNetworkReply

from qgis.gui import QgsMessageBar

from .abstractfinder import AbstractFinder


class HttpFinder(AbstractFinder):

    def __init__(self, parent):
        super(HttpFinder, self).__init__(parent)
        self.asynchonous = True
        self.reply = None
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.replyFinished)

    def _sendRequest(self, url, params):
        if self.asynchonous:
            url = QUrl(url)
            for key, value in params.iteritems():
                url.addQueryItem(key, value)
            request = QNetworkRequest(url)
            self.reply = self.manager.get(request)

        else:
            response = urllib2.urlopen(self.url + '?' + urllib.urlencode(params))
            data = json.load(response)
            self.loadData(data)

    def stop(self):
        if self.reply:
            self.reply.abort()
            self.reply = None
        self._finish()

    def replyFinished(self, reply):
        self.reply = None
        error = reply.error()
        if error == QNetworkReply.NoError:
            data = json.loads(reply.readAll().data())
            self.loadData(data)
        else:
            self.message.emit(self, self.getErrorMessage(error), QgsMessageBar.CRITICAL)
            self._finish()

    def getErrorMessage(self, error):
        if error == QNetworkReply.NoError:
            # No error condition.
            # Note: When the HTTP protocol returns a redirect no error will be reported.
            # You can check if there is a redirect with the
            # QNetworkRequest::RedirectionTargetAttribute attribute.
            return ''

        if error == QNetworkReply.ConnectionRefusedError:
            return self.tr('The remote server refused the connection'
                           ' (the server is not accepting requests)')

        if error == QNetworkReply.RemoteHostClosedError :
            return self.tr('The remote server closed the connection prematurely,'
                           ' before the entire reply was received and processed')

        if error == QNetworkReply.HostNotFoundError :
            return self.tr('The remote host name was not found (invalid hostname)')

        if error == QNetworkReply.TimeoutError :
            return self.tr('The connection to the remote server timed out')

        if error == QNetworkReply.OperationCanceledError :
            return self.tr('The operation was canceled via calls to abort()'
                           ' or close() before it was finished.')

        if error == QNetworkReply.SslHandshakeFailedError :
            return self.tr('The SSL/TLS handshake failed'
                           ' and the encrypted channel could not be established.'
                           ' The sslErrors() signal should have been emitted.')

        if error == QNetworkReply.TemporaryNetworkFailureError :
            return self.tr('The connection was broken'
                           ' due to disconnection from the network,'
                           ' however the system has initiated roaming'
                           ' to another access point.'
                           ' The request should be resubmitted and will be processed'
                           ' as soon as the connection is re-established.')

        if error == QNetworkReply.ProxyConnectionRefusedError :
            return self.tr('The connection to the proxy server was refused'
                           ' (the proxy server is not accepting requests)')

        if error == QNetworkReply.ProxyConnectionClosedError :
            return self.tr('The proxy server closed the connection prematurely,'
                           ' before the entire reply was received and processed')

        if error == QNetworkReply.ProxyNotFoundError :
            return self.tr('The proxy host name was not found (invalid proxy hostname)')

        if error == QNetworkReply.ProxyTimeoutError :
            return self.tr('The connection to the proxy timed out'
                           ' or the proxy did not reply in time to the request sent')

        if error == QNetworkReply.ProxyAuthenticationRequiredError :
            return self.tr('The proxy requires authentication'
                           ' in order to honour the request'
                           ' but did not accept any credentials offered (if any)')

        if error == QNetworkReply.ContentAccessDenied :
            return self.tr('The access to the remote content was denied'
                           ' (similar to HTTP error 401)'),
        if error == QNetworkReply.ContentOperationNotPermittedError :
            return self.tr('The operation requested on the remote content is not permitted')

        if error == QNetworkReply.ContentNotFoundError :
            return self.tr('The remote content was not found at the server'
                           ' (similar to HTTP error 404)')
        if error == QNetworkReply.AuthenticationRequiredError :
            return self.tr('The remote server requires authentication to serve the content'
                           ' but the credentials provided were not accepted (if any)')

        if error == QNetworkReply.ContentReSendError :
            return self.tr('The request needed to be sent again, but this failed'
                           ' for example because the upload data could not be read a second time.')

        if error == QNetworkReply.ProtocolUnknownError :
            return self.tr('The Network Access API cannot honor the request'
                           ' because the protocol is not known')

        if error == QNetworkReply.ProtocolInvalidOperationError :
            return self.tr('the requested operation is invalid for this protocol')

        if error == QNetworkReply.UnknownNetworkError :
            return self.tr('An unknown network-related error was detected')

        if error == QNetworkReply.UnknownProxyError :
            return self.tr('An unknown proxy-related error was detected')

        if error == QNetworkReply.UnknownContentError :
            return self.tr('An unknown error related to the remote content was detected')

        if error == QNetworkReply.ProtocolFailure :
            return self.tr('A breakdown in protocol was detected'
                           ' (parsing error, invalid or unexpected responses, etc.)')

        return self.tr('An unknown network-related error was detected')
