# GUI开坑

很久很久之前就想写一些图形化的程序了，但一直功力不够😂因为最熟悉的语言是python，便一开始就用它来设计了。不过看到网上对python的图形化完全一片不乐观的景象，着实是无从下手，之前也有看过thinker一类的库，不过因为设计界面都是从代码写出来的，着实痛苦。后来因为个人所需，对图形化的要求越来越高，也见识过了 Electron 等一系列优秀的框架，但对我这个新手来说，这些着实不是一个好的选择。（当然，我非常钦佩他们用html，css，js写网页的方案来使得所有平台共用一套代码，这也是我所觉得最好的一套图形化方案）

虽然能力不足，但需求总是存在，所以也要想办法去解决。后来又一次看见了qt的框架，见到他图形化的编程是有图形设计界面的，加上刚好看见一篇基础的博客，于是决定用它来为python建立图形化。

## 开始

先感谢一下这篇入门教程，没有他就没有之后的事了😊

[\[ PyQt入门教程 \] Qt Designer工具的使用 - 锅边糊 - 博客园 (cnblogs.com)](https://www.cnblogs.com/linyfeng/p/11223707.html)

### 安装pyqt5

```bash
pip install pyqt5
```

### 在电脑中搜索 designer.exe 软件并打开设计

还好有一些 VB 的基础（话说现在不会有人用了吧😶），对界面简单的一些设计还是OK的，然后保存。

qt的文件是 .ui 类型的，点开来看应该是 xml 类型的文件

### 将 .ui 转为 .py

```bash
pyuic5 login.ui -o login.py
```

注意一个要点，转出来的 .py 文件就不要改动内部了，界面和逻辑要分离，以后只引用这个包就好

### 逻辑部分

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from login import Ui_Form # 引用之前界面生成的包

class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self) #初始化界面（包里的函数）

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
```

通用模板

通常一个窗口一个类（class），然后创建一个对象是这个类的，然后 .show() 就OK了

```python
self.login_Button.clicked.connect(self.display)
```

这是当某个窗口的 login_Button（按钮） 遇到 clicked（被点击） 的信号时执行这个窗口所属类里的 display 函数（槽）

#### 顺带一提 self. 的使用

当函数名或者变量名是要横跨不同的类或者同一类里不同函数使用时，需要加 self.

## 多线程

在GUI程序里面，能灵活使用多线程是至关重要的，要不然当程序遇到需要长时间的工作或者需要并行的工作时就会假死或者出现奇奇怪怪的问题。

在 BBDown GUI 里，这是我一个比较大的问题，花了我一天时间解决登录二维码的事🤦‍

另外设计一个包含二维码图片和文字的窗口我就不细说了，我主要记录一下 QThread 和信号连接

本部分主要观看了 [[ PyQt入门教程 \] PyQt5中多线程模块QThread使用方法 - 锅边糊 - 博客园 (cnblogs.com) ](https://www.cnblogs.com/linyfeng/p/12239856.html) 的教程（才发现竟然是同一个人😄）



1. 先对所需要进行的线程打包成一个类，将耗时的那部分程序放入 run 函数内

```python
class workthread(QThread):
    signalllll = pyqtSignal(str) # 创建一个信号
    def __init__(self, arg):
        super(workthread, self).__init__()
        self.arg = arg
    def run(self):
        # 长耗时的程序
        while True:
            self.signalllll.emit("abcde")
```

其中创建信号的部分需要指定信号传递的参量的类型，如 str, int 等

在长耗时程序中，需要的值就可以通过 .emit() 传回给槽

当然，别忘记实例化这个需要这两个包

```python
from PyQt5.QtCore import QThread, pyqtSignal
```

2. 通过之前的类新建一个对象，然后启动线程，当线程里有值传回时，就会通过自定义的信号 `signalllll` 传回到 self.display 这个函数上（即作为这个函数的参数）

```
self.work = workthread()
self.work.start()
self.work.signalllll.connect(self.display)
```

3. 然后你就可以在 display 这个函数中操纵界面了，比如更改图片/文字等

## 图片

不是很复杂，快速说一下

库

```python
from PyQt5.QtGui import QPixmap
```

使用label标签设置图片（对，就是文字和图片共用一种widget）

```python
self.label_QR.setPixmap(QPixmap("图片路径"))
```

## 文本/文本框/按钮

设置文本/文本框/按钮内的文本

```python
self.label.setText("要设置的文本")
```

获取 标签/文本框/按钮 上的文本，注意区分大小写

```
self.label.text()
```

## 复选框/单选框

设置复选框/单选框

```python
self.checkBox.setChecked(True/False)
```

获取复选框/单选框当前状态

```python
self.checkBox.isChecked()
```

