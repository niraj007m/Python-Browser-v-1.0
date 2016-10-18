from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys
import SocketServer

class MainWindow(QMainWindow):
	
	def __init__(self, *args, **kwargs):

		super(MainWindow,self).__init__(*args, **kwargs)

		self.browser = QWebEngineView()
		self.browser.setUrl( QUrl("https://www.google.com"))

		self.setCentralWidget(self.browser)

		navtb = QToolBar("Navigation")
		navtb.setIconSize( QSize(16,16))
		self.addToolBar(navtb)

		back_btn = QAction( QIcon(os.path.join('icons','back.png')), "Back", self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.triggered.connect(self.browser.back)
		navtb.addAction(back_btn)

		next_btn = QAction( QIcon(os.path.join('icons','next.png')), "Forward", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.triggered.connect(self.browser.forward)
		navtb.addAction(next_btn)

		reload_btn = QAction( QIcon(os.path.join('icons','Refresh.png')), "Reload", self)
		reload_btn.setStatusTip("Forward to next page")
		reload_btn.triggered.connect(self.browser.reload)
		navtb.addAction(reload_btn)

		home_btn = QAction( QIcon(os.path.join('icons','home.png')), "Home", self)
		home_btn.setStatusTip("Home page")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		navtb.addSeparator()

		self.httpsicon = QLabel() #Yes, really !
		self.httpsicon.setPixmap( QPixmap (os.path.join('icons','lockssl.png')))
		navtb.addWidget(self.httpsicon)

		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		navtb.addWidget(self.urlbar)

		stop_btn = QAction( QIcon(os.path.join('icons','cross.png')), "Stop", self)
		stop_btn.setStatusTip("Stop Loading current page")
		stop_btn.triggered.connect(self.browser.stop)
		navtb.addAction(stop_btn)

		self.browser.urlChanged.connect(self.update_urlbar)

		self.menuBar().setNativeMenuBar(False)

		file_menu = self.menuBar().addMenu("&File")

		print_action = QAction(QIcon(), "Print...", self)
		print_action.setStatusTip("Print current page")
		print_action.triggered.connect(self.print_page)
		file_menu.addAction(print_action)

		self.show()

		self.setWindowTitle("Infosecplatform Browser")
		self.setWindowIcon( QIcon( os.path.join('icons','infosec.png')))

	def print_page(self):
		dlg = QPrintPreviewDialog()
		#dlg.painterRequested.connect(self.browser.print_)
		dlg.exec_()

	def navigate_home(self):
		self.browser.setUrl( QUrl("http://www.google.com"))

	def navigate_to_url(self): #Does not receive the Url
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")

		self.browser.setUrl(q)

	def update_urlbar(self, q):

		if q.scheme() == 'https':
			# secure padlock icon
			self.httpsicon.setPixmap( QPixmap (os.path.join('icons','lockssl.png')))
		else:
			# Insecure padlock icon
			self.httpsicon.setPixmap( QPixmap (os.path.join('icons','lock.png')))

		self.urlbar.setText( q.toString())
		self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Infosecplatform Browser")
app.setOrganizationName("Infosecplatform")
app.setOrganizationName("https://github.com/niraj007m")

window = MainWindow()
window.show()

app.exec_()