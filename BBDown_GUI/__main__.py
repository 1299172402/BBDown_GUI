from genericpath import exists
import os
from sqlite3 import IntegrityError
import sys
import time
import json
import subprocess

from BBDown_GUI.UI.ui_main import Ui_Form_main
from BBDown_GUI.UI.ui_qrcode import Ui_Form_QRcode
from BBDown_GUI.UI.ui_about import Ui_Form_about

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon

workdir = os.path.dirname(os.path.abspath(__file__))
bbdowndir = os.path.join(workdir, "BBDown.exe")

# 显示图标
# 单文件打包引入外部资源
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = workdir

    return os.path.join(base_path, relative_path)

def log(message=''):
    t = time.time()
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))}.{int(t * 1000) % 1000}] - {message}')

class RunBBDown(QThread):
    signal = pyqtSignal(int)
    def __init__(self, command):
        super(RunBBDown, self).__init__()
        self.command = command
        self.p = None
    def run(self):
        self.p = subprocess.Popen(f'"{bbdowndir}" {self.command}', shell=True)
        self.p.wait()

class FormLogin(QMainWindow, Ui_Form_QRcode):
    def __init__(self, arg):
        super(FormLogin, self).__init__()
        self.arg = arg
        self.setupUi(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("./UI/favicon.ico")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
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
        # qrcode.png 的生成位置在当前命令行的位置，不是bbdown的位置 Line 84 附近也要改
        # self.label_QR.setPixmap(QPixmap(os.path.join(workdir, "qrcode.png")))
        self.label_QR.setPixmap(QPixmap(os.path.join(os.getcwd(), "qrcode.png")))
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
            if (((self.arg == "login") and (os.path.exists(os.path.join(workdir, "BBDown.data")))) or
               ((self.arg == "logintv") and (os.path.exists(os.path.join(workdir, "BBDownTV.data"))))):
                self.signal.emit("登录成功")
                time.sleep(1)
                self.signal.emit("0")
                break
            elif os.path.exists(os.path.join(os.getcwd(), "qrcode.png")):
                self.signal.emit("请扫描二维码")
            else:
                self.signal.emit("未获取到信息")

class FormAbout(QMainWindow, Ui_Form_about):
    def __init__(self):
        super(FormAbout, self).__init__()
        self.setupUi(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("./UI/favicon.ico")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        

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
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("./UI/favicon.ico")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_logintv.clicked.connect(self.logintv)
        self.lineEdit_ffmpeg.setText(os.path.join(workdir, "ffmpeg.exe"))
        self.lineEdit_aria2c_path.setText(os.path.join(workdir, "aria2c.exe"))
        self.lineEdit_dir.setText(os.path.join(workdir, "Download"))
        self.lineEdit_bbdown.setText(bbdowndir)
        self.pushButton_ffmpeg.clicked.connect(self.ffmpegpath)
        self.pushButton_dir.clicked.connect(self.downpath)
        self.pushButton_bbdown.clicked.connect(self.bbdownpath)
        self.pushButton_param.clicked.connect(self.param)
        self.pushButton_download.clicked.connect(self.download)
        self.pushButton_advanced.clicked.connect(self.advanced)
        self.advanced = False
        self.pushButton_about.clicked.connect(self.about)
        try:
            Load(self)
        except:
            # 当之前没有保存过任何参数时，界面为默认
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
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(), "ffmpeg (ffmpeg.exe);;All Files (*.*)")
        filepath = filepath.replace("/","\\")
        self.lineEdit_ffmpeg.setText(filepath)

    # 设置下载目录
    def downpath(self):
        downpath = QFileDialog.getExistingDirectory(self, "选择文件夹", os.getcwd())
        downpath = downpath.replace("/","\\")
        self.lineEdit_dir.setText(downpath)

    # 设置BBDown位置
    def bbdownpath(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", os.getcwd(), "BBDown (BBDown.exe);;All Files (*.*)")
        filepath = filepath.replace("/","\\")
        self.lineEdit_bbdown.setText(filepath)
        global bbdowndir
        bbdowndir = self.lineEdit_bbdown.text()

    # 获取下载参数（有返回值）
    def arg(self):
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
            if self.checkBox_skip_ai.isChecked():
                args += ' --skip-ai '

            # MP4box
            if self.checkBox_mp4box.isChecked():
                args += ' --use-mp4box '
            if self.checkBox_mp4box_path.isChecked():
                args += f' --mp4box-path "{self.lineEdit_mp4box_path.text()}" '

            # 其他
            if self.checkBox_mt.isChecked():
                args += ' -mt '
            if self.checkBox_force_http.isChecked():
                args += ' --force-http '
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
            if self.checkBox_aria2c_args.isChecked():
                args += f' --aria2c-args "{self.lineEdit_aria2c_args.text()}" '

            # 文件名选项
            if self.checkBox_F.isChecked():
                args += f' -F "{self.lineEdit_F.text()}" '
            if self.checkBox_M.isChecked():
                args += f' -M "{self.lineEdit_M.text()}" '
            
            # 代理
            if self.checkBox_enable_proxy.isChecked():
                if self.checkBox_host.isChecked():
                    args += f' --host {self.lineEdit_host.text()} '
                if self.checkBox_ep_host.isChecked():
                    args += f' --ep-host {self.lineEdit_ep_host.text()} '
                if self.checkBox_area.isChecked():
                    args += f' --area {self.lineEdit_area.text()} '

        # 下载路径
        args += f' --work-dir "{self.lineEdit_dir.text()}" '

        return args

    def param(self):
        args = self.arg()
        self.lineEdit_param.setText(args)

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
        args = self.arg()

        # 测试专用
        if self.advanced and self.checkBox_debug.isChecked():
            log('BBDown GUI 启动下载任务')
            log(f"运行参数: {args}") 

        try:
            self.job_down = RunBBDown(args)
            self.job_down.start()
            # .wait 会使GUI在下载时卡住，只有在结束或终止了下载过程后才能恢复
            # 但是可以捕获 Ctrl-C 的异常，以便终止下载而不退出程序
            # 后续需要改进
            self.job_down.wait()
        except:
            print('[EXCEPT] Process terminated.')
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

def main():
    app = QApplication(sys.argv)
    win_main = FormMain()
    win_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
