import subprocess

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal

from BBDown_GUI.UI.ui_output import Ui_Form_output
from BBDown_GUI.tool import get_bbdowndir, resource_path, log

class DownloadThread(QThread):
    output_signal = pyqtSignal(str)
    def __init__(self, args) -> None:
        super().__init__()
        # Run the command and capture its output
        self.p = subprocess.Popen(f'"{get_bbdowndir()}" {args}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    def run(self):
        # Read the output line by line and display it in real-time
        while True:
            out = self.p.stdout.readline().decode("gbk")
            if out == '' and self.p.poll() is not None:
                break
            if out:
                self.output_signal.emit(out)
                
class FormOutput(QMainWindow, Ui_Form_output):
    def __init__(self, args):
        super(FormOutput, self).__init__()
        self.setupUi(self)
        self.args = args
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("./UI/favicon.ico")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.lineEdit_cmd.setText(self.args)
        self.lineEdit_cmd.setCursorPosition(0) # Set the cursor to the beginning
        self.pushButton_stop.clicked.connect(self.stop)
        self.flag_stop = False
        self.execute()
    def execute(self):
        self.work = DownloadThread(self.args)
        self.work.start()
        self.work.output_signal.connect(self.display)
    def display(self, message):
        self.textEdit_output.setText(self.textEdit_output.toPlainText() + message.strip() + '\n')
        self.textEdit_output.verticalScrollBar().setValue(self.textEdit_output.verticalScrollBar().maximum())
    def stop(self):
        if self.flag_stop == True:
            return
        else:
            subprocess.Popen(['taskkill', '/F', '/T', '/PID',  str(self.work.p.pid)], shell=True)
            self.display("")
            self.display("")
            self.display(log("[BBDown_GUI] 下载已停止"))
            self.flag_stop = True