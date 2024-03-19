# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 820)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comPort = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comPort.setGeometry(QtCore.QRect(20, 20, 69, 22))
        self.comPort.setEditable(False)
        self.comPort.setObjectName("comPort")
        self.connect = QtWidgets.QPushButton(parent=self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(230, 20, 75, 24))
        self.connect.setObjectName("connect")
        self.label_22 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(20, 60, 31, 16))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.folderLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.folderLabel.setEnabled(False)
        self.folderLabel.setGeometry(QtCore.QRect(150, 60, 291, 20))
        self.folderLabel.setObjectName("folderLabel")
        self.site = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.site.setEnabled(True)
        self.site.setGeometry(QtCore.QRect(50, 60, 41, 22))
        self.site.setText("")
        self.site.setReadOnly(True)
        self.site.setObjectName("site")
        self.start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.start.setEnabled(False)
        self.start.setGeometry(QtCore.QRect(370, 430, 75, 24))
        self.start.setObjectName("start")
        self.FiltersGroup = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.FiltersGroup.setEnabled(False)
        self.FiltersGroup.setGeometry(QtCore.QRect(20, 100, 421, 321))
        self.FiltersGroup.setObjectName("FiltersGroup")
        self.startTime2 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime2.setGeometry(QtCore.QRect(33, 137, 131, 22))
        self.startTime2.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime2.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime2.setObjectName("startTime2")
        self.totalTime5 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime5.setGeometry(QtCore.QRect(172, 227, 51, 22))
        self.totalTime5.setText("")
        self.totalTime5.setObjectName("totalTime5")
        self.label_4 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.label_4.setGeometry(QtCore.QRect(370, 40, 41, 16))
        self.label_4.setObjectName("label_4")
        self.totalTime3 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime3.setGeometry(QtCore.QRect(172, 167, 51, 22))
        self.totalTime3.setText("")
        self.totalTime3.setObjectName("totalTime3")
        self.totalTime0 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime0.setGeometry(QtCore.QRect(172, 77, 51, 22))
        self.totalTime0.setText("")
        self.totalTime0.setObjectName("totalTime0")
        self.startTime0 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime0.setGeometry(QtCore.QRect(33, 77, 131, 22))
        self.startTime0.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime0.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime0.setObjectName("startTime0")
        self.totalAir7 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir7.setEnabled(False)
        self.totalAir7.setGeometry(QtCore.QRect(263, 287, 61, 22))
        self.totalAir7.setText("")
        self.totalAir7.setReadOnly(True)
        self.totalAir7.setObjectName("totalAir7")
        self.status2 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status2.setGeometry(QtCore.QRect(364, 140, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status2.setFont(font)
        self.status2.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status2.setObjectName("status2")
        self.totalTime2 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime2.setGeometry(QtCore.QRect(172, 137, 51, 22))
        self.totalTime2.setText("")
        self.totalTime2.setObjectName("totalTime2")
        self.label_6 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.label_6.setEnabled(False)
        self.label_6.setGeometry(QtCore.QRect(190, 50, 21, 16))
        self.label_6.setObjectName("label_6")
        self.filter1 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter1.setEnabled(False)
        self.filter1.setGeometry(QtCore.QRect(13, 110, 16, 16))
        self.filter1.setObjectName("filter1")
        self.status4 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status4.setGeometry(QtCore.QRect(364, 200, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status4.setFont(font)
        self.status4.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status4.setObjectName("status4")
        self.startTime1 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime1.setGeometry(QtCore.QRect(33, 107, 131, 22))
        self.startTime1.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime1.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime1.setObjectName("startTime1")
        self.startTime7 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime7.setGeometry(QtCore.QRect(33, 287, 131, 22))
        self.startTime7.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime7.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime7.setObjectName("startTime7")
        self.status3 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status3.setGeometry(QtCore.QRect(364, 170, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status3.setFont(font)
        self.status3.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status3.setObjectName("status3")
        self.filter0 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter0.setEnabled(False)
        self.filter0.setGeometry(QtCore.QRect(13, 80, 16, 16))
        self.filter0.setObjectName("filter0")
        self.filter4 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter4.setEnabled(False)
        self.filter4.setGeometry(QtCore.QRect(13, 200, 16, 16))
        self.filter4.setObjectName("filter4")
        self.filter5 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter5.setEnabled(False)
        self.filter5.setGeometry(QtCore.QRect(13, 230, 16, 16))
        self.filter5.setObjectName("filter5")
        self.label_8 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.label_8.setGeometry(QtCore.QRect(35, 50, 131, 20))
        self.label_8.setObjectName("label_8")
        self.filter7 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter7.setEnabled(False)
        self.filter7.setGeometry(QtCore.QRect(13, 290, 16, 16))
        self.filter7.setObjectName("filter7")
        self.label_7 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.label_7.setGeometry(QtCore.QRect(290, 50, 16, 16))
        self.label_7.setObjectName("label_7")
        self.totalAir5 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir5.setEnabled(False)
        self.totalAir5.setGeometry(QtCore.QRect(263, 227, 61, 22))
        self.totalAir5.setText("")
        self.totalAir5.setReadOnly(True)
        self.totalAir5.setObjectName("totalAir5")
        self.totalTime7 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime7.setGeometry(QtCore.QRect(172, 287, 51, 22))
        self.totalTime7.setText("")
        self.totalTime7.setObjectName("totalTime7")
        self.startTime3 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime3.setGeometry(QtCore.QRect(33, 167, 131, 22))
        self.startTime3.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime3.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime3.setObjectName("startTime3")
        self.totalAir4 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir4.setEnabled(False)
        self.totalAir4.setGeometry(QtCore.QRect(263, 197, 61, 22))
        self.totalAir4.setText("")
        self.totalAir4.setReadOnly(True)
        self.totalAir4.setObjectName("totalAir4")
        self.totalAir0 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir0.setEnabled(False)
        self.totalAir0.setGeometry(QtCore.QRect(263, 77, 61, 22))
        self.totalAir0.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.totalAir0.setText("")
        self.totalAir0.setReadOnly(True)
        self.totalAir0.setObjectName("totalAir0")
        self.totalAir3 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir3.setEnabled(False)
        self.totalAir3.setGeometry(QtCore.QRect(263, 167, 61, 22))
        self.totalAir3.setText("")
        self.totalAir3.setReadOnly(True)
        self.totalAir3.setObjectName("totalAir3")
        self.filter2 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter2.setEnabled(False)
        self.filter2.setGeometry(QtCore.QRect(13, 140, 16, 16))
        self.filter2.setObjectName("filter2")
        self.status7 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status7.setGeometry(QtCore.QRect(364, 290, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status7.setFont(font)
        self.status7.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status7.setObjectName("status7")
        self.totalTime4 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime4.setGeometry(QtCore.QRect(172, 197, 51, 22))
        self.totalTime4.setText("")
        self.totalTime4.setObjectName("totalTime4")
        self.totalTime6 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime6.setGeometry(QtCore.QRect(172, 257, 51, 22))
        self.totalTime6.setText("")
        self.totalTime6.setObjectName("totalTime6")
        self.startTime5 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime5.setGeometry(QtCore.QRect(33, 227, 131, 22))
        self.startTime5.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime5.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime5.setObjectName("startTime5")
        self.startTime4 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime4.setGeometry(QtCore.QRect(33, 197, 131, 22))
        self.startTime4.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime4.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime4.setObjectName("startTime4")
        self.label_5 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.label_5.setGeometry(QtCore.QRect(274, 29, 41, 16))
        self.label_5.setObjectName("label_5")
        self.status6 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status6.setGeometry(QtCore.QRect(364, 260, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status6.setFont(font)
        self.status6.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status6.setObjectName("status6")
        self.filter3 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter3.setEnabled(False)
        self.filter3.setGeometry(QtCore.QRect(13, 170, 16, 16))
        self.filter3.setObjectName("filter3")
        self.totalAir1 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir1.setEnabled(False)
        self.totalAir1.setGeometry(QtCore.QRect(263, 107, 61, 22))
        self.totalAir1.setText("")
        self.totalAir1.setReadOnly(True)
        self.totalAir1.setObjectName("totalAir1")
        self.startTime6 = QtWidgets.QDateTimeEdit(parent=self.FiltersGroup)
        self.startTime6.setGeometry(QtCore.QRect(33, 257, 131, 22))
        self.startTime6.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime6.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime6.setObjectName("startTime6")
        self.status0 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status0.setGeometry(QtCore.QRect(364, 80, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status0.setFont(font)
        self.status0.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status0.setObjectName("status0")
        self.status1 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status1.setGeometry(QtCore.QRect(364, 110, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status1.setFont(font)
        self.status1.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status1.setObjectName("status1")
        self.status5 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.status5.setGeometry(QtCore.QRect(364, 230, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.status5.setFont(font)
        self.status5.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.status5.setObjectName("status5")
        self.totalAir6 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir6.setEnabled(False)
        self.totalAir6.setGeometry(QtCore.QRect(263, 257, 61, 22))
        self.totalAir6.setText("")
        self.totalAir6.setReadOnly(True)
        self.totalAir6.setObjectName("totalAir6")
        self.filter6 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.filter6.setEnabled(False)
        self.filter6.setGeometry(QtCore.QRect(13, 260, 16, 16))
        self.filter6.setObjectName("filter6")
        self.totalAir2 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalAir2.setEnabled(False)
        self.totalAir2.setGeometry(QtCore.QRect(263, 137, 61, 22))
        self.totalAir2.setText("")
        self.totalAir2.setReadOnly(True)
        self.totalAir2.setObjectName("totalAir2")
        self.label_2 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.label_2.setGeometry(QtCore.QRect(73, 29, 51, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.FiltersGroup)
        self.label_3.setGeometry(QtCore.QRect(173, 29, 51, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.totalTime1 = QtWidgets.QLineEdit(parent=self.FiltersGroup)
        self.totalTime1.setGeometry(QtCore.QRect(172, 107, 51, 22))
        self.totalTime1.setText("")
        self.totalTime1.setObjectName("totalTime1")
        self.reset = QtWidgets.QPushButton(parent=self.centralwidget)
        self.reset.setEnabled(False)
        self.reset.setGeometry(QtCore.QRect(20, 432, 75, 24))
        self.reset.setObjectName("reset")
        self.datetime = QtWidgets.QLabel(parent=self.centralwidget)
        self.datetime.setEnabled(True)
        self.datetime.setGeometry(QtCore.QRect(320, 23, 131, 16))
        font = QtGui.QFont()
        font.setBold(False)
        self.datetime.setFont(font)
        self.datetime.setText("")
        self.datetime.setObjectName("datetime")
        self.folderSelect = QtWidgets.QPushButton(parent=self.centralwidget)
        self.folderSelect.setGeometry(QtCore.QRect(100, 60, 41, 24))
        self.folderSelect.setObjectName("folderSelect")
        self.PumpGroup = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.PumpGroup.setEnabled(False)
        self.PumpGroup.setGeometry(QtCore.QRect(20, 480, 421, 80))
        self.PumpGroup.setObjectName("PumpGroup")
        self.flow = QtWidgets.QLineEdit(parent=self.PumpGroup)
        self.flow.setEnabled(False)
        self.flow.setGeometry(QtCore.QRect(80, 30, 61, 22))
        self.flow.setText("")
        self.flow.setReadOnly(True)
        self.flow.setObjectName("flow")
        self.Label_10 = QtWidgets.QLabel(parent=self.PumpGroup)
        self.Label_10.setGeometry(QtCore.QRect(150, 32, 31, 16))
        font = QtGui.QFont()
        font.setBold(False)
        self.Label_10.setFont(font)
        self.Label_10.setObjectName("Label_10")
        self.pumpStatus = QtWidgets.QLabel(parent=self.PumpGroup)
        self.pumpStatus.setGeometry(QtCore.QRect(350, 32, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.pumpStatus.setFont(font)
        self.pumpStatus.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.pumpStatus.setObjectName("pumpStatus")
        self.Label_11 = QtWidgets.QLabel(parent=self.PumpGroup)
        self.Label_11.setGeometry(QtCore.QRect(310, 32, 41, 16))
        font = QtGui.QFont()
        font.setBold(False)
        self.Label_11.setFont(font)
        self.Label_11.setObjectName("Label_11")
        self.Label_9 = QtWidgets.QLabel(parent=self.PumpGroup)
        self.Label_9.setGeometry(QtCore.QRect(30, 32, 51, 16))
        font = QtGui.QFont()
        font.setBold(False)
        self.Label_9.setFont(font)
        self.Label_9.setObjectName("Label_9")
        self.commsGroup = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.commsGroup.setEnabled(False)
        self.commsGroup.setGeometry(QtCore.QRect(20, 580, 421, 201))
        self.commsGroup.setObjectName("commsGroup")
        self.serialOutput = QtWidgets.QPlainTextEdit(parent=self.commsGroup)
        self.serialOutput.setGeometry(QtCore.QRect(10, 80, 401, 101))
        self.serialOutput.setPlainText("")
        self.serialOutput.setObjectName("serialOutput")
        self.Label_12 = QtWidgets.QLabel(parent=self.commsGroup)
        self.Label_12.setGeometry(QtCore.QRect(10, 43, 61, 16))
        font = QtGui.QFont()
        font.setBold(False)
        self.Label_12.setFont(font)
        self.Label_12.setObjectName("Label_12")
        self.serianInput = QtWidgets.QLineEdit(parent=self.commsGroup)
        self.serianInput.setGeometry(QtCore.QRect(80, 40, 331, 22))
        self.serianInput.setObjectName("serianInput")
        self.baudrate = QtWidgets.QComboBox(parent=self.centralwidget)
        self.baudrate.setGeometry(QtCore.QRect(100, 20, 69, 22))
        self.baudrate.setMaxVisibleItems(11)
        self.baudrate.setObjectName("baudrate")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.baudrate.addItem("")
        self.label_23 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(176, 23, 31, 16))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.baudrate.setCurrentIndex(12)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect.setText(_translate("MainWindow", "Connect"))
        self.label_22.setText(_translate("MainWindow", "site"))
        self.folderLabel.setText(_translate("MainWindow", "folder"))
        self.start.setText(_translate("MainWindow", "Start"))
        self.FiltersGroup.setTitle(_translate("MainWindow", "Filters"))
        self.startTime2.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.label_4.setText(_translate("MainWindow", "Status"))
        self.startTime0.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.status2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "(m)"))
        self.filter1.setText(_translate("MainWindow", "1"))
        self.status4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.startTime1.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.startTime7.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.status3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.filter0.setText(_translate("MainWindow", "0"))
        self.filter4.setText(_translate("MainWindow", "4"))
        self.filter5.setText(_translate("MainWindow", "5"))
        self.label_8.setText(_translate("MainWindow", "(dd/mm/yyyy HH:MM)"))
        self.filter7.setText(_translate("MainWindow", "7"))
        self.label_7.setText(_translate("MainWindow", "(L)"))
        self.startTime3.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.filter2.setText(_translate("MainWindow", "2"))
        self.status7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.startTime5.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.startTime4.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.label_5.setText(_translate("MainWindow", "Total air"))
        self.status6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.filter3.setText(_translate("MainWindow", "3"))
        self.startTime6.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm"))
        self.status0.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.status1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.status5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.filter6.setText(_translate("MainWindow", "6"))
        self.label_2.setText(_translate("MainWindow", "start time"))
        self.label_3.setText(_translate("MainWindow", "total time"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.folderSelect.setText(_translate("MainWindow", "folder"))
        self.PumpGroup.setTitle(_translate("MainWindow", "Pump"))
        self.Label_10.setText(_translate("MainWindow", "SLPM"))
        self.pumpStatus.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#aa0000;\">OFF</span></p></body></html>"))
        self.Label_11.setText(_translate("MainWindow", "Status"))
        self.Label_9.setText(_translate("MainWindow", "Air flow"))
        self.commsGroup.setTitle(_translate("MainWindow", "Serial Communication"))
        self.Label_12.setText(_translate("MainWindow", "command"))
        self.baudrate.setCurrentText(_translate("MainWindow", "115200"))
        self.baudrate.setItemText(0, _translate("MainWindow", "300"))
        self.baudrate.setItemText(1, _translate("MainWindow", "600"))
        self.baudrate.setItemText(2, _translate("MainWindow", "750"))
        self.baudrate.setItemText(3, _translate("MainWindow", "1200"))
        self.baudrate.setItemText(4, _translate("MainWindow", "2400"))
        self.baudrate.setItemText(5, _translate("MainWindow", "4800"))
        self.baudrate.setItemText(6, _translate("MainWindow", "9600"))
        self.baudrate.setItemText(7, _translate("MainWindow", "19200"))
        self.baudrate.setItemText(8, _translate("MainWindow", "31250"))
        self.baudrate.setItemText(9, _translate("MainWindow", "38400"))
        self.baudrate.setItemText(10, _translate("MainWindow", "57600"))
        self.baudrate.setItemText(11, _translate("MainWindow", "74880"))
        self.baudrate.setItemText(12, _translate("MainWindow", "115200"))
        self.baudrate.setItemText(13, _translate("MainWindow", "230400"))
        self.label_23.setText(_translate("MainWindow", "bauds"))
