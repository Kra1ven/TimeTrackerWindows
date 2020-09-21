from win32gui import GetWindowText, GetForegroundWindow
import pyautogui
import time
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from DBmanage import DBhandle
from matplotlib import pyplot as plt
import matplotlib.backends.backend_tkagg
import matplotlib.backends.backend_svg
import os
import sys
import math

# APP RUNNING STATE
Running = True


# CHECKING CURRENT WINDOW WITH TIMER
def wathdog():
	t0 = time.time()
	while True:
		x = GetWindowText(GetForegroundWindow())
		time.sleep(1)
		if x != GetWindowText(GetForegroundWindow()):
			t1 = time.time()
			thrd = threading.Thread(target=DBhandle.DBstore, args=(x.replace("'", ""), math.floor(t1-t0)))
			thrd.start()
			t0 = time.time()
		elif math.floor(time.time() - t0) == 60:
			t1 = time.time()
			thrd = threading.Thread(target=DBhandle.DBstore, args=(x.replace("'", ""), math.floor(t1-t0)))
			thrd.start()
			t0 = time.time()
		elif Running == False:
			DBhandle.DBstore(x.replace("'", ""), counter)
			quit()
		elif Running == "Paused" or Running == "Afk":
			while Running == "Paused" or Running == "Afk":
				time.sleep(1)


# CHECKING IF USER AFK TO PAUSE
def mouseTrack():
	global Running
	x = pyautogui.position()
	counter = 0
	global count
	count = True
	while True:
		if x == pyautogui.position() and counter == 1200:
			Running = "Afk"
			count = False
			counter = 0
		elif not Running:
			break
		elif x != pyautogui.position() and Running == "Afk":
			Running = True
			count = True
		if x != pyautogui.position():
			x = pyautogui.position()
			counter = 0

		time.sleep(2)
		if count:
			counter += 2


# STARTING THE MAIN WATCHDOG AND MOUSETRACK FUNCTION
main_thread = threading.Thread(target=wathdog)
main_thread.start()

mouse_thread = threading.Thread(target=mouseTrack)
mouse_thread.start()


# EXTERNAL FUNCTIONS
data = DBhandle.DBextract("Weekly")
header = "Weekly"

class window(QWidget):
		def __init__(self, parent=None):
			QWidget.__init__(self, parent)
			self.set0 = QBarSet(f'Hours')
			
			self.set0.append([float(x) for x in data.values()])
			
			self.series = QBarSeries()
			self.series.append(self.set0)
			
			self.chart = QChart()
			self.chart.setTheme(QChart.ChartThemeHighContrast)
			self.chart.addSeries(self.series)
			self.chart.setTitle(header)
			self.chart.setAnimationOptions(QChart.SeriesAnimations)

			months = (data.keys())

			self.axisX = QBarCategoryAxis()
			self.axisX.append(months)

			self.axisY = QValueAxis()
			try: 
				self.axisY.setRange(0, float(list(data.values())[0]))
				if (float(list(data.values())[0])) > 19:
				    self.axisY.setTickCount(15)
				elif (float(list(data.values())[0])) > 10:
				    self.axisY.setTickCount(10)
				else:
				    self.axisY.setTickCount(5)
				#axisY.setTickInterval(1)
				#axisY.applyNiceNumbers()
			except:
				self.chart.setTitle("No Data")
			self.chart.addAxis(self.axisX, Qt.AlignBottom)
			self.chart.addAxis(self.axisY, Qt.AlignLeft)

			self.chart.legend().setVisible(True)
			self.chart.legend().setAlignment(Qt.AlignBottom)

			self.chartView = QChartView(self.chart)
			self.vert_l = QVBoxLayout()
			self.vert_l.addWidget(self.chartView)
			self.setLayout(self.vert_l)

def CurrentState():
	if Running == "Paused":
		ui.State.setText("Paused")
	elif Running == "Afk":
		ui.State.setText("Paused")
	else:
		ui.State.setText("Running")

def Closing():
	global Running
	Running = False
	quit()

def Pause():
	global Running
	global count
	if Running == "Paused":
		Running = True
		count = True
	elif Running:
		Running = "Paused"

# QT GUI
class Ui_MainWindow(object):

	def __init__(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setEnabled(True)
		MainWindow.resize(980, 628)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
		MainWindow.setSizePolicy(sizePolicy)
		MainWindow.setMinimumSize(QtCore.QSize(980, 628))
		MainWindow.setMaximumSize(QtCore.QSize(980, 628))
		MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
		MainWindow.setAutoFillBackground(False)
		MainWindow.setStyleSheet("")
		MainWindow.setAnimated(True)
		MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setEnabled(True)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
		self.centralwidget.setSizePolicy(sizePolicy)
		self.centralwidget.setObjectName("centralwidget")
		self.DataOutputs = QtWidgets.QLabel(self.centralwidget)
		self.DataOutputs.setGeometry(QtCore.QRect(20, 10, 151, 51))
		font = QtGui.QFont()
		font.setFamily("Century Gothic")
		font.setPointSize(13)
		font.setBold(False)
		font.setItalic(True)
		font.setWeight(50)
		self.DataOutputs.setFont(font)
		self.DataOutputs.setScaledContents(False)
		self.DataOutputs.setWordWrap(False)
		self.DataOutputs.setIndent(0)
		self.DataOutputs.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.DataOutputs.setObjectName("DataOutputs")
		self.Monthly = QtWidgets.QPushButton(self.centralwidget)
		self.Monthly.setGeometry(QtCore.QRect(20, 60, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Monthly.setFont(font)
		self.Monthly.setObjectName("Monthly")
		self.Weekly = QtWidgets.QPushButton(self.centralwidget)
		self.Weekly.setGeometry(QtCore.QRect(20, 120, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Weekly.setFont(font)
		self.Weekly.setObjectName("Weekly")
		self.Daily = QtWidgets.QPushButton(self.centralwidget)
		self.Daily.setGeometry(QtCore.QRect(20, 180, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Daily.setFont(font)
		self.Daily.setObjectName("Daily")
		self.Sublime = QtWidgets.QPushButton(self.centralwidget)
		self.Sublime.setGeometry(QtCore.QRect(20, 270, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Sublime.setFont(font)
		self.Sublime.setObjectName("Sublime")
		self.Chrome = QtWidgets.QPushButton(self.centralwidget)
		self.Chrome.setGeometry(QtCore.QRect(20, 330, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Chrome.setFont(font)
		self.Chrome.setObjectName("Chrome")
		self.CurrentState = QtWidgets.QLabel(self.centralwidget)
		self.CurrentState.setGeometry(QtCore.QRect(20, 460, 151, 51))
		font = QtGui.QFont()
		font.setFamily("Century Gothic")
		font.setPointSize(13)
		font.setBold(False)
		font.setItalic(True)
		font.setWeight(50)
		self.CurrentState.setFont(font)
		self.CurrentState.setScaledContents(False)
		self.CurrentState.setWordWrap(False)
		self.CurrentState.setIndent(0)
		self.CurrentState.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.CurrentState.setObjectName("CurrentState")
		self.Pause = QtWidgets.QPushButton(self.centralwidget)
		self.Pause.setGeometry(QtCore.QRect(20, 550, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Pause.setFont(font)
		self.Pause.setAutoDefault(False)
		self.Pause.setDefault(False)
		self.Pause.setFlat(False)
		self.Pause.setObjectName("Pause")
		self.State = QtWidgets.QLabel(self.centralwidget)
		self.State.setGeometry(QtCore.QRect(10, 490, 151, 51))
		font = QtGui.QFont()
		font.setFamily("Century Gothic")
		font.setPointSize(18)
		font.setBold(False)
		font.setItalic(False)
		font.setWeight(50)
		self.State.setFont(font)
		self.State.setScaledContents(False)
		self.State.setAlignment(QtCore.Qt.AlignCenter)
		self.State.setWordWrap(False)
		self.State.setIndent(0)
		self.State.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.State.setObjectName("State")
		self.widget = window(self.centralwidget)
		self.widget.setUpdatesEnabled(True)
		self.widget.setGeometry(QtCore.QRect(150, -30, 851, 691))
		self.widget.setObjectName("widget")
		self.widget.raise_()
		self.DataOutputs.raise_()
		self.CurrentState.raise_()
		self.Sublime.raise_()
		self.Daily.raise_()
		self.Pause.raise_()
		self.Monthly.raise_()
		self.State.raise_()
		self.Weekly.raise_()
		self.Chrome.raise_()

		self.Sublime.clicked.connect(lambda: self.update(DataRange = "Sublime Text"))
		self.Chrome.clicked.connect(lambda: self.update(DataRange = "Google Chrome"))
		self.Daily.clicked.connect(lambda: self.update(DataRange = "Daily"))
		self.Weekly.clicked.connect(lambda: self.update(DataRange = "Weekly"))
		self.Monthly.clicked.connect(lambda: self.update(DataRange = "Monthly"))
		self.Pause.clicked.connect(Pause)

		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "TTW"))
		self.DataOutputs.setText(_translate("MainWindow", "Data Outputs : "))
		self.Monthly.setText(_translate("MainWindow", "Monthly"))
		self.Weekly.setText(_translate("MainWindow", "Weekly"))
		self.Daily.setText(_translate("MainWindow", "Daily"))
		self.Sublime.setText(_translate("MainWindow", "Sublime Text"))
		self.Chrome.setText(_translate("MainWindow", "Google Chrome"))
		self.CurrentState.setText(_translate("MainWindow", "Current State : "))
		self.Pause.setText(_translate("MainWindow", "Pause"))
		self.State.setText(_translate("MainWindow", "State"))

	def update(self, DataRange):
		global data
		global header
		data = DBhandle.DBextract(DataRange)
		header = DataRange
		if len(data) < 2:
			data["NotEnoughData"] = 0

		self.widget.close()
		del self.widget
		self.widget = window(self.centralwidget)
		self.widget.setUpdatesEnabled(True)
		self.widget.setGeometry(QtCore.QRect(150, -30, 851, 691))
		self.widget.setObjectName("widget")
		self.widget.show()

	def closeEvent(self, event):
		if can_exit:
			event.accept()
		else:
			event.ignore()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow(MainWindow)
MainWindow.show()
app.aboutToQuit.connect(Closing)
timer = QtCore.QTimer()
timer.timeout.connect(CurrentState)
timer.start(100)
sys.exit(app.exec_())
