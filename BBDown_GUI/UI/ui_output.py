# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_output(object):
    def setupUi(self, Form_output):
        Form_output.setObjectName("Form_output")
        Form_output.resize(738, 343)
        Form_output.setMinimumSize(QtCore.QSize(738, 343))
        Form_output.setMaximumSize(QtCore.QSize(738, 343))
        self.verticalLayoutWidget = QtWidgets.QWidget(Form_output)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 721, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_cmd = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_cmd.setText("")
        self.lineEdit_cmd.setDragEnabled(True)
        self.lineEdit_cmd.setReadOnly(True)
        self.lineEdit_cmd.setObjectName("lineEdit_cmd")
        self.horizontalLayout.addWidget(self.lineEdit_cmd)
        self.pushButton_stop = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout.addWidget(self.pushButton_stop)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit_output = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_output.setReadOnly(True)
        self.textEdit_output.setObjectName("textEdit_output")
        self.verticalLayout.addWidget(self.textEdit_output)

        self.retranslateUi(Form_output)
        QtCore.QMetaObject.connectSlotsByName(Form_output)

    def retranslateUi(self, Form_output):
        _translate = QtCore.QCoreApplication.translate
        Form_output.setWindowTitle(_translate("Form_output", "下载"))
        self.pushButton_stop.setText(_translate("Form_output", "停止"))
        self.textEdit_output.setHtml(_translate("Form_output", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">[输出内容]</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))