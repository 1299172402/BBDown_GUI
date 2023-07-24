from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow

from BBDown_GUI.tool import resource_path
from BBDown_GUI.UI.ui_about import Ui_Form_about

class FormAbout(QMainWindow, Ui_Form_about):
    def __init__(self):
        super(FormAbout, self).__init__()
        self.setupUi(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("./UI/favicon.ico")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)