import os
import sys
import time
import json
import subprocess

from UI.main import Ui_Form_main
from UI.qrcode import Ui_Form_QRcode
from UI.about import Ui_Form_about

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

workdir = os.path.dirname(os.path.abspath(sys.argv[0]))
bbdowndir = os.path.join(workdir, "BBDown.exe")

class RunBBDown(QThread):
    def __init__(self, command):
        super(RunBBDown, self).__init__()
        self.command = command
    def run(self):
        p = subprocess.Popen(f"\"{bbdowndir}\" {self.command}", shell=True)
        p.wait()

class FormLogin(QMainWindow, Ui_Form_QRcode):
    def __init__(self, arg):
        super(FormLogin, self).__init__()
        self.arg = arg
        self.setupUi(self)
        self.label_QR.setScaledContents(True)
        if (arg == "login") and (os.path.exists(os.path.join(workdir, "BBDown.data"))):
            os.remove(os.path.join(workdir, "BBDown.data"))
        if (arg == "logintv") and (os.path.exists(os.path.join(workdir, "BBDownTV.data"))):
            os.remove(os.path.join(workdir, "BBDownTV.data"))
        self.job1 = RunBBDown(self.arg)
        self.job1.start()
        self.execute()
    def execute(self):
        self.work = workthread(self.arg)
        self.work.start()
        self.work.signal.connect(self.display)
    def display(self, s):
        self.label_QR.setPixmap(QPixmap(os.path.join(workdir, "qrcode.png")))
        self.label.setText(s)
        if s == "0":
            self.close()

class workthread(QThread):
    signal = pyqtSignal(str)
    def __init__(self, arg):
        super(workthread, self).__init__()
        self.arg = arg
    def run(self):
        for _ in range(181):
            time.sleep(1)
            if ((self.arg == "login") and (os.path.exists(os.path.join(workdir, "BBDown.data")))) or \
               ((self.arg == "logintv") and (os.path.exists(os.path.join(workdir, "BBDownTV.data")))):
                self.signal.emit("登录成功")
                time.sleep(2)
                self.signal.emit("0")
                break
            elif os.path.exists(os.path.join(workdir, "qrcode.png")):
                self.signal.emit("请扫描二维码")

class FormAbout(QMainWindow, Ui_Form_about):
    def __init__(self):
        super(FormAbout, self).__init__()
        self.setupUi(self)
        

class FormMain(QMainWindow, Ui_Form_main):
    def __init__(self):
        def Load(self):
            f = open(os.path.join(workdir, "config.json"), "r")
            config = json.loads(f.read())
            f.close()
            for item in config:
                if item == "advanced":
                    self.advanced = config[item]
                    if self.advanced:
                        self.pushButton_advanced.setText("简易选项<")
                        self.resize(1220, 500)
                        self.advanced = True
                    else:
                        self.pushButton_advanced.setText("高级选项>")
                        self.resize(620, 400)
                        self.advanced = False
                elif type(config[item]) == type(True):
                    exec(f"self.{item}.setChecked({config[item]})")
                elif type(config[item]) == type(""):
                    exec(f"self.{item}.setText(r\"{config[item]}\")")
        super(FormMain, self).__init__()
        self.setupUi(self)
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_logintv.clicked.connect(self.logintv)
        self.lineEdit_ffmpeg.setText(os.path.join(workdir, "ffmpeg.exe"))
        self.lineEdit_aria2c.setText(os.path.join(workdir, "aria2c.exe"))
        self.lineEdit_dir.setText(os.path.join(workdir, "Download"))
        self.lineEdit_bbdown.setText(bbdowndir)
        self.pushButton_ffmpeg.clicked.connect(self.ffmpegpath)
        self.pushButton_aria2c.clicked.connect(self.aria2cpath)
        self.pushButton_dir.clicked.connect(self.downpath)
        self.pushButton_bbdown.clicked.connect(self.bbdownpath)
        self.pushButton_download.clicked.connect(self.download)
        self.pushButton_advanced.clicked.connect(self.advanced)
        self.advanced = False
        self.pushButton_about.clicked.connect(self.about)
        try:
            Load(self)
        except:
            pass
    def login(self):
        self.win_login = FormLogin("login")
        self.win_login.show()  
    def logintv(self):
        self.win_login = FormLogin("logintv")
        self.win_login.show()    
    def ffmpegpath(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(), \
        "ffmpeg (ffmpeg.exe);;All Files (*.*)")
        self.lineEdit_ffmpeg.setText(filepath)
    def aria2cpath(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(), \
        "aria2c (aria2c.exe);;All Files (*.*)")
        self.lineEdit_aria2c.setText(filepath)
    def downpath(self):
        downpath = QFileDialog.getExistingDirectory(self, "选择文件夹", os.getcwd())
        self.lineEdit_dir.setText(downpath)
    def bbdownpath(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(), \
        "BBDown (BBDown.exe);;All Files (*.*)")
        self.lineEdit_bbdown.setText(filepath)
        global bbdowndir
        bbdowndir = self.lineEdit_bbdown.text()
    def download(self):
        def Save():
            config = {}
            for i in range(1, 9):
                exec(f"config[\"radioButton_{i}\"]=self.radioButton_{i}.isChecked()")
            config["checkBox_ffmpeg"] = self.checkBox_ffmpeg.isChecked()
            config["lineEdit_ffmpeg"] = self.lineEdit_ffmpeg.text()
            config["checkBox_aria2c"] = self.checkBox_aria2c.isChecked()
            config["lineEdit_aria2c"] = self.lineEdit_aria2c.text()
            config["advanced"] = self.advanced
            for i in range(1, 26):
                exec(f"config[\"checkBox_{i}\"]=self.checkBox_{i}.isChecked()")
            for i in range(1, 8):
                exec(f"config[\"lineEdit_{i}\"]=self.lineEdit_{i}.text()")
            config["lineEdit_dir"] = self.lineEdit_dir.text()
            config["lineEdit_url"] = self.lineEdit_url.text()
            f = open(os.path.join(workdir, "config.json"), "w")
            f.write(json.dumps(config, indent=4))
            f.close()

        Save()
        arg = ""
        if self.radioButton_1.isChecked():
            pass
        elif self.radioButton_2.isChecked():
            arg += " -tv"
        elif self.radioButton_3.isChecked():
            arg += " -app"
        elif self.radioButton_4.isChecked():
            arg += " -intl"
        if self.radioButton_5.isChecked():
            pass
        elif self.radioButton_6.isChecked():
            arg += " -hevc"
        elif self.radioButton_7.isChecked():
            arg += " -avc"
        elif self.radioButton_8.isChecked():
            arg += " -av1"
        if self.checkBox_ffmpeg.isChecked():
            arg += f" --ffmpeg-path \"{self.lineEdit_ffmpeg.text()}\""
        if self.checkBox_aria2c.isChecked():
            arg += f" --use-aria2c --aria2c-path \"{self.lineEdit_aria2c.text()}\""
        if self.checkBox_25.isChecked():
            arg += " -p ALL"
        if self.advanced:
            if self.checkBox_1.isChecked():
                arg += " --use-mp4box"
            if self.checkBox_2.isChecked():
                arg += " -info"
            if self.checkBox_3.isChecked():
                arg += " -hs"
            if self.checkBox_4.isChecked():
                arg += " -ia"
            if self.checkBox_5.isChecked():
                arg += " --show-all"
            if self.checkBox_6.isChecked():
                arg += f" --aria2c-proxy {self.lineEdit_1.text()}"
            if self.checkBox_7.isChecked():
                arg += " -mt"
            if self.checkBox_8.isChecked():
                arg += f" -p {self.lineEdit_2.text()}"
            if self.checkBox_9.isChecked():
                arg += " --audio-only"
            if self.checkBox_10.isChecked():
                arg += " --video-only"
            if self.checkBox_11.isChecked():
                arg += " --sub-only"
            if self.checkBox_12.isChecked():
                arg += " --no-padding-page-num"
            if self.checkBox_13.isChecked():
                arg += " --debug"
            if self.checkBox_14.isChecked():
                arg += " --skip-mux"
            if self.checkBox_15.isChecked():
                arg += " --skip-subtitle"
            if self.checkBox_16.isChecked():
                arg += " --skip-cover"
            if self.checkBox_17.isChecked():
                arg += " -dd"
            if self.checkBox_18.isChecked():
                arg += " --add-dfn-subfix"
            if self.checkBox_19.isChecked():
                arg += " --no-part-prefix"
            if self.checkBox_20.isChecked():
                arg += f" --language {self.lineEdit_3.text()}"
            if self.checkBox_21.isChecked():
                arg += f" -c {self.lineEdit_4.text()}"
            if self.checkBox_22.isChecked():
                arg += f" -token {self.lineEdit_5.text()}"
            if self.checkBox_23.isChecked():
                arg += f" --mp4box-path \"{self.lineEdit_6.text()}\""
            if self.checkBox_24.isChecked():
                arg += f" --delay-per-page {self.lineEdit_7.text()}"
        arg += f" --work-dir \"{self.lineEdit_dir.text()}\""
        arg += f" {self.lineEdit_url.text()}"
        self.job1 = RunBBDown(arg)
        self.job1.start()

    def advanced(self):
        if not self.advanced:
            self.pushButton_advanced.setText("简易选项<")
            self.resize(1220, 500)
            self.advanced = True
        else:
            self.pushButton_advanced.setText("高级选项>")
            self.resize(620, 400)
            self.advanced = False
    def about(self):
        self.win_about = FormAbout()
        self.win_about.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win_main = FormMain()
    win_main.show()
    sys.exit(app.exec_())

