import sys
import os
import time

def get_workdir():
    if getattr(sys, "frozen", False):
        workdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        workdir = os.path.dirname(os.path.abspath(__file__))
    return workdir

def get_bbdowndir():
    bbdowndir = os.path.join(get_workdir(), "BBDown.exe")
    return bbdowndir

# 显示图标
# 单文件打包引入外部资源
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = get_workdir()
    return os.path.join(base_path, relative_path)

def log(message=''):
    t = time.time()
    return f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))}.{int(t * 1000) % 1000}] - {message}'
