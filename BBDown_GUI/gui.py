import sys
from PyQt5.QtWidgets import QApplication
from BBDown_GUI.Form.form_main import FormMain

def main():
    app = QApplication(sys.argv)
    win_main = FormMain()
    win_main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
