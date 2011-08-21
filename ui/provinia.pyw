# -*- coding: utf-8 -*-

import os
import random
import socket

from PyQt4 import QtCore, QtGui
from PyQt4 import QtWebKit

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

class Worker(QtCore.QThread):

    def __init__(self, parent, port):
        super(Worker, self).__init__(parent)
        self.port = port

    def run(self):
        """Launches the Django app"""

        """
        from gunicorn.app.djangoapp import DjangoApplicationCommand
        DjangoApplicationCommand({}, '').run()
        """

        from django.core.management import call_command
        call_command('runserver', port=self.port, verbosity=2)

class ProviniaUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.server = Worker(self, self.port)
        self.server.start()
        self.setupUi()

    @property
    def port(self):
        """Attempts to find a port that we can bind to"""

        if not hasattr(self, '_port'):
            attempted = []
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while True:
                port = random.randint(1001, 65000)
                if port not in attempted:
                    print 'Trying port', port
                    attempted.append(port)
                else:
                    # try another port
                    continue

                s.connect(('127.0.0.1', 8000))
                s.shutdown(2)
                break

            self._port = port

        return self._port

    def setupUi(self):
        self.resize(790, 562)
        self.setWindowTitle("Provinia")

        self.centralwidget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")

        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl("http://127.0.0.1:%s/" % (self.port,)))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def __del__(self):
        """
        Performs any required cleanup tasks
        """

        self.server.terminate()
        self.server.wait()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = ProviniaUI()
    ui.show()
    app.exec_()

