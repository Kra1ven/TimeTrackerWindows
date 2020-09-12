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
		elif Running == "Paused":
			while Running == "Paused":
				time.sleep(1)


# CHECKING IF USER AFK TO PAUSE
def mouseTrack():
	global Running
	x = pyautogui.position()
	counter = 0
	count = True
	while True:
		if x == pyautogui.position() and counter == 12:
			Running = "Paused"
			count = False
			counter = 0
		elif not Running:
			break
		elif x != pyautogui.position() and Running == "Paused":
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
def DisplayData(DateRange):
	data = DBhandle.DBextract(DateRange)
	if len(data) < 2:
		data["NotEnoughData"] = 0
	
	class window(QMainWindow):
		def __init__(self, parent=None):
			super(window, self).__init__(parent=parent)
			self.resize(800, 600)

			set0 = QBarSet(f'Hours')

			set0.append([float(x) for x in data.values()])

			series = QBarSeries()
			series.append(set0)

			chart = QChart()
			chart.addSeries(series)
			chart.setTitle(DateRange)
			chart.setAnimationOptions(QChart.SeriesAnimations)
			
			months = (data.keys())

			axisX = QBarCategoryAxis()
			axisX.append(months)

			axisY = QValueAxis()
			axisY.setRange(0, float(list(data.values())[0]))
			if (float(list(data.values())[0])) > 19:
				axisY.setTickCount(15)
			elif (float(list(data.values())[0])) > 10:
				axisY.setTickCount(10)
			else:
				axisY.setTickCount(5)
			#axisY.setTickInterval(1)
			#axisY.applyNiceNumbers()

			chart.addAxis(axisX, Qt.AlignBottom)
			chart.addAxis(axisY, Qt.AlignLeft)

			chart.legend().setVisible(True)
			chart.legend().setAlignment(Qt.AlignBottom)

			chartView = QChartView(chart)
			self.setCentralWidget(chartView)

	window = window()
	window.show()

	def remove(e):
		window.deleteLater()
	window.closeEvent = remove

def CurrentState():
	if Running == "Paused":
		ui.State.setText("Paused")
	else:
		ui.State.setText("Running")

def Closing():
	global Running
	Running = False
	quit()

def Pause():
	global Running
	if Running == "Paused":
		Running = True
	elif Running:
		Running = "Paused"

def Monthly():
	DisplayData("Monthly")

def Weekly():
	DisplayData("Weekly")


def Daily():
	DisplayData("Daily")

# SUPPORTED APPS
def Sublime():
	DisplayData("Sublime Text")

def GoogleChrome():
	DisplayData("Google Chrome")

# TKINTER GUI
class Ui_MainWindow(object):
	def __init__(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setEnabled(True)
		MainWindow.resize(625, 312)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
		MainWindow.setSizePolicy(sizePolicy)
		MainWindow.setMinimumSize(QtCore.QSize(625, 312))
		MainWindow.setMaximumSize(QtCore.QSize(625, 312))
		MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
		MainWindow.setAutoFillBackground(False)
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
		self.DataOutputs.setGeometry(QtCore.QRect(20, 30, 151, 51))
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
		self.Monthly.clicked.connect(Monthly)
		self.Monthly.setGeometry(QtCore.QRect(170, 30, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Monthly.setFont(font)
		self.Monthly.setObjectName("Monthly")
		self.Weekly = QtWidgets.QPushButton(self.centralwidget)
		self.Weekly.clicked.connect(Weekly)
		self.Weekly.setGeometry(QtCore.QRect(320, 30, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Weekly.setFont(font)
		self.Weekly.setObjectName("Weekly")
		self.Daily = QtWidgets.QPushButton(self.centralwidget)
		self.Daily.clicked.connect(Daily)
		self.Daily.setGeometry(QtCore.QRect(470, 30, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Daily.setFont(font)
		self.Daily.setObjectName("Daily")
		self.SupportedApps = QtWidgets.QLabel(self.centralwidget)
		self.SupportedApps.setGeometry(QtCore.QRect(20, 130, 151, 51))
		font = QtGui.QFont()
		font.setFamily("Century Gothic")
		font.setPointSize(13)
		font.setBold(False)
		font.setItalic(True)
		font.setWeight(50)
		self.SupportedApps.setFont(font)
		self.SupportedApps.setScaledContents(False)
		self.SupportedApps.setWordWrap(False)
		self.SupportedApps.setIndent(0)
		self.SupportedApps.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.SupportedApps.setObjectName("SupportedApps")
		self.Sublime = QtWidgets.QPushButton(self.centralwidget)
		self.Sublime.clicked.connect(Sublime)
		self.Sublime.setGeometry(QtCore.QRect(190, 130, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Sublime.setFont(font)
		self.Sublime.setObjectName("Sublime")
		self.Chrome = QtWidgets.QPushButton(self.centralwidget)
		self.Chrome.clicked.connect(GoogleChrome)
		self.Chrome.setGeometry(QtCore.QRect(340, 130, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Chrome.setFont(font)
		self.Chrome.setObjectName("Chrome")
		self.line_2 = QtWidgets.QFrame(self.centralwidget)
		self.line_2.setGeometry(QtCore.QRect(0, 210, 641, 16))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.line_2.setFont(font)
		self.line_2.setLineWidth(2)
		self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		self.CurrentState = QtWidgets.QLabel(self.centralwidget)
		self.CurrentState.setGeometry(QtCore.QRect(330, 240, 151, 51))
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
		self.Pause.clicked.connect(Pause)
		self.Pause.setGeometry(QtCore.QRect(90, 240, 131, 51))
		font = QtGui.QFont()
		font.setFamily("Calibri Light")
		font.setPointSize(13)
		self.Pause.setFont(font)
		self.Pause.setObjectName("Pause")
		self.State = QtWidgets.QLabel(self.centralwidget)
		self.State.setGeometry(QtCore.QRect(480, 240, 151, 51))
		font = QtGui.QFont()
		font.setFamily("Century Gothic")
		font.setPointSize(18)
		font.setBold(False)
		font.setItalic(False)
		font.setWeight(50)
		self.State.setFont(font)
		self.State.setScaledContents(False)
		self.State.setWordWrap(False)
		self.State.setIndent(0)
		self.State.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.State.setObjectName("State")
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
		self.SupportedApps.setText(_translate("MainWindow", "Supported Apps : "))
		self.Sublime.setText(_translate("MainWindow", "Sublime Text"))
		self.Chrome.setText(_translate("MainWindow", "Google Chrome"))
		self.CurrentState.setText(_translate("MainWindow", "Current State : "))
		self.Pause.setText(_translate("MainWindow", "Pause"))
		self.State.setText(_translate("MainWindow", "State"))

	def closeEvent(self, event):
		# do stuff
		if can_exit:
			event.accept() # let the window close
		else:
			event.ignore()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow(MainWindow)
state_thread = threading.Thread(target=CurrentState)
state_thread.start()
MainWindow.show()
app.aboutToQuit.connect(Closing)
timer = QtCore.QTimer()
timer.timeout.connect(CurrentState)
timer.start(100)
sys.exit(app.exec_())
