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
        try:
            # print(f'"{bbdowndir}" {self.command}')
            p = subprocess.Popen(f'"{bbdowndir}" {self.command}', shell=True)
            p.wait()
        except:
            self.exitcode = -1

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
                        self.resize(1560, 500)
                        self.advanced = True
                    else:
                        self.pushButton_advanced.setText("高级选项>")
                        self.resize(620, 400)
                        self.advanced = False
                elif type(config[item]) == type(True):
                    exec(f'self.{item}.setChecked({config[item]})')
                elif type(config[item]) == type(''):
                    exec(f'self.{item}.setText(r"{config[item]}")')
                elif type(config[item]) == type(0):
                    exec(f'self.{item}.setCurrentIndex({config[item]})')
        
        super(FormMain, self).__init__()
        self.setupUi(self)
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_logintv.clicked.connect(self.logintv)
        self.lineEdit_ffmpeg.setText(os.path.join(workdir, "ffmpeg.exe"))
        self.lineEdit_aria2c_path.setText(os.path.join(workdir, "aria2c.exe"))
        self.lineEdit_dir.setText(os.path.join(workdir, "Download"))
        self.lineEdit_bbdown.setText(bbdowndir)
        self.pushButton_ffmpeg.clicked.connect(self.ffmpegpath)
        self.pushButton_dir.clicked.connect(self.downpath)
        self.pushButton_bbdown.clicked.connect(self.bbdownpath)
        self.pushButton_download.clicked.connect(self.download)
        self.pushButton_advanced.clicked.connect(self.advanced)
        self.advanced = False
        self.pushButton_about.clicked.connect(self.about)
        try:
            Load(self)
        except:
            self.resize(620, 400)

    # 登录（网页端）
    def login(self):
        self.win_login = FormLogin("login")
        self.win_login.show()  

    # 登录（tv端）
    def logintv(self):
        self.win_login = FormLogin("logintv")
        self.win_login.show()   

    # 设置ffmpeg位置
    def ffmpegpath(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(),
        "ffmpeg (ffmpeg.exe);;All Files (*.*)")
        filepath = filepath.replace("/","\\")
        self.lineEdit_ffmpeg.setText(filepath)

    # 设置下载目录
    def downpath(self):
        downpath = QFileDialog.getExistingDirectory(self, "选择文件夹", os.getcwd())
        downpath = downpath.replace("/","\\")
        self.lineEdit_dir.setText(downpath)

    # 设置BBDown位置
    def bbdownpath(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(), \
        "BBDown (BBDown.exe);;All Files (*.*)")
        filepath = filepath.replace("/","\\")
        self.lineEdit_bbdown.setText(filepath)
        global bbdowndir
        bbdowndir = self.lineEdit_bbdown.text()

    # 开始下载
    def download(self):
        def Save():
            config = {}
            for i in dir(self):
                if i[:9]=="checkBox_":
                    exec(f"config[i] = self.{i}.isChecked()")
                elif i[:12]=="radioButton_":
                    exec(f"config[i] = self.{i}.isChecked()")
                elif i[:9]=="lineEdit_":
                    exec(f"config[i] = self.{i}.text()")
                elif i[:9]=="comboBox_":
                    exec(f"config[i] = self.{i}.currentIndex()")
            config["advanced"] = self.advanced
            f = open(os.path.join(workdir, "config.json"), "w")
            f.write(json.dumps(config, indent=4))
            f.close()

        Save()
        args = ''

        # 下载地址
        args += f' {self.lineEdit_url.text()} '

        # 画质选择
        if self.radioButton_dfn_priority.isChecked():
            pass
        elif self.radioButton_dfn_1080P.isChecked():
            args += ' --dfn-priority "1080P 高清" '
        elif self.radioButton_dfn_720P.isChecked():
            args += ' --dfn-priority "720P 高清" '
        elif self.radioButton_dfn_480P.isChecked():
            args += ' --dfn-priority "480P 清晰" '
        elif self.radioButton_dfn_360P.isChecked():
            args += ' --dfn-priority "360P 流畅" '
        elif self.radioButton_dfn_more.isChecked():
            if self.comboBox_dfn_more.currentIndex()!=0:
                dfn = self.comboBox_dfn_more.itemText(self.comboBox_dfn_more.currentIndex())
                args += f' --dfn-priority "{dfn}"'
        
        # 下载源选择
        if self.comboBox_source.currentIndex()!=0:
            choice = ['', '-tv', '-app', '-intl']
            args += ' ' + choice[self.comboBox_source.currentIndex()] + ' '
        
        # 下载视频编码选择
        if self.comboBox_encoding.currentIndex()!=0:
            choice = ['', 'AVC', 'AV1', 'HEVC']
            args += ' --encoding-priority ' + choice[self.comboBox_encoding.currentIndex()] + ' '

        # 指定FFmpeg路径
        if self.checkBox_ffmpeg.isChecked():
            args += f' --ffmpeg-path "{self.lineEdit_ffmpeg.text()}" '

        # 下载分P选项
        if self.radioButton_p_current.isChecked():
            pass
        elif self.radioButton_p_all.isChecked():
            args += ' -p ALL '
        elif self.radioButton_p_new.isChecked():
            args += ' -p NEW '

        # 高级选项
        if self.advanced:
            # 下载选项
            if self.checkBox_audio_only.isChecked():
                args += ' --audio-only '
            if self.checkBox_video_only.isChecked():
                args += ' --video-only '
            if self.checkBox_sub_only.isChecked():
                args += ' --sub-only '
            if self.checkBox_danmaku.isChecked():
                args += ' -dd '

            # 交互选项
            if self.checkBox_ia.isChecked():
                args += ' -ia '
            if self.checkBox_info.isChecked():
                args += ' -info '
            if self.checkBox_hs.isChecked():
                args += ' -hs '
            if self.checkBox_debug.isChecked():
                args += ' --debug '

            # Cookies
            if self.checkBox_token.isChecked():
                args += f' -token "{self.lineEdit_token.text()}" '
            if self.checkBox_c.isChecked():
                args += f' -c "{self.lineEdit_c.text()}" '

            # 跳过选项
            if self.checkBox_skip_subtitle.isChecked():
                args += ' --skip-subtitle '
            if self.checkBox_skip_cover.isChecked():
                args += ' --skip-cover '
            if self.checkBox_skip_mux.isChecked():
                args += ' --skip-mux '

            # MP4box
            if self.checkBox_mp4box.isChecked():
                args += ' --use-mp4box '
            if self.checkBox_mp4box_path.isChecked():
                args += f' --mp4box-path "{self.lineEdit_mp4box_path.text()}" '

            # 其他
            if self.checkBox_mt.isChecked():
                args += ' -mt '
            if self.checkBox_language.isChecked():
                args += f' --language {self.lineEdit_language.text()} '

            # 分P
            if self.checkBox_p_show_all.isChecked():
                args += ' --show-all '
            if self.checkBox_p.isChecked():
                args += f' -p {self.lineEdit_p.text()} '
            if self.checkBox_p_delay.isChecked():
                args += f' --delay-per-page {self.lineEdit_p_delay.text()} '

            # aria2c
            if self.checkBox_use_aria2c.isChecked():
                args += ' --use-aria2c '
            if self.checkBox_aria2c_path.isChecked():
                args += f' --aria2c-path "{self.lineEdit_aria2c_path.text()}" '
            if self.checkBox_aria2c_proxy.isChecked():
                args += f' --aria2c-proxy {self.lineEdit_aria2c_proxy.text()} '

            # 文件名选项
            if self.checkBox_F.isChecked():
                args += f' -F "{self.lineEdit_F.text()}" '
            if self.checkBox_M.isChecked():
                args += f' -M "{self.lineEdit_M.text()}" '

        # 下载路径
        args += f' --work-dir "{self.lineEdit_dir.text()}" '

        # 测试专用
        '''
        if self.advanced and self.checkBox_debug.isChecked():
            print("[BBDown_GUI_args]")
            print(args)
        '''
        try:
            self.job1 = RunBBDown(args)
            self.job1.start()
            if self.job1.wait() and self.job1.exitcode == -1:
                print(self.job1.wait())
                print(self.job1.exitcode)
                raise self.job1.exception
        except:
            pass

    # 高级选项
    def advanced(self):
        if not self.advanced:
            self.pushButton_advanced.setText("简易选项<")
            self.resize(1560, 500)
            self.advanced = True
        else:
            self.pushButton_advanced.setText("高级选项>")
            self.resize(620, 400)
            self.advanced = False

    # 关于
    def about(self):
        self.win_about = FormAbout()
        self.win_about.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win_main = FormMain()
    win_main.show()
    sys.exit(app.exec_())

