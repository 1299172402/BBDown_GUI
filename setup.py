from io import open
from setuptools import setup

setup(
    name='BBDown_GUI',
    version='$pypi-version$',
    url='https://github.com/1299172402/BBDown_GUI',
    license='MIT',
    author='之雨',
    description='BBDown using the graphical interface.',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['gui', 'bbdown', 'bilibili', 'download'],
    packages=['BBDown_GUI', 'BBDown_GUI.UI', 'BBDown_GUI.Form'],
    include_package_data=True,
    install_requires=['PyQt5==5.15.6'],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    entry_points={
        'console_scripts': [
            'bbdowngui = BBDown_GUI.gui:main',
            'BBDownGUI = BBDown_GUI.gui:main',
            'bbdown_gui = BBDown_GUI.gui:main',
            'BBDown_GUI = BBDown_GUI.gui:main',
        ],
    },
)

# 更改version
# 清空dist文件夹内容
# py -m pip install --upgrade build
# py -m build
# py -m pip install --upgrade twine
# # 测试服务器
# # py -m twine upload --repository testpypi dist/*
# # py -m pip install --index-url https://test.pypi.org/simple/ --no-deps BBDown-GUI
# 真实服务器
# py -m twine upload dist/* -u __token__ -p <your_token>
