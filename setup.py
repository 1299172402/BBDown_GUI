from io import open
from setuptools import setup

setup(
    name='BBDown_GUI',
    version='1.0.4',
    url='https://github.com/1299172402/BBDown_GUI',
    license='MIT',
    author='之雨',
    description='BBDown using the graphical interface.',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['gui', 'bbdown', 'bilibili', 'download'],
    packages=['BBDown_GUI', 'BBDown_GUI.UI'],
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
            'bbdowngui = BBDown_GUI.__main__:main',
            'BBDownGUI = BBDown_GUI.__main__:main',
            'bbdown_gui = BBDown_GUI.__main__:main',
            'BBDown_GUI = BBDown_GUI.__main__:main',
        ],
    },
)
