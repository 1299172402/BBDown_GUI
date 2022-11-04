from BBDown_GUI import gui

def main():
    gui.main()

if __name__ == '__main__':
    main()

# 打包本文件
# pyinstaller --noconfirm --onefile --console --icon "./BBDown_GUI/UI/favicon.ico" --add-data "./BBDown_GUI/UI/favicon.ico;./UI"  "./build-to-exe.py"