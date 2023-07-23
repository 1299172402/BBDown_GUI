# BBDown_GUI
BBDown的图形化版本，亦保留有命令行

## 特性

- [x] 记忆下载参数
- [x] 下载剧集选项（当前剧集、全部剧集、最新剧集）
- [x] 优先显示常用选项，亦保留有所有功能
- [x] 在命令行中仅按一次 Ctrl-C 可以中断本次下载

## 使用方法

将 BBDown 的可执行程序与本 UI 程序置于同一文件夹中，直接运行即可。这样以后 BBDown 主程序更新也可以直接替换使用

## 下载

### 从 [Releases](https://github.com/1299172402/BBDown_GUI/releases) 中下载使用 [![img](https://img.shields.io/github/v/release/1299172402/BBDown_GUI?label=%E7%89%88%E6%9C%AC)](https://github.com/1299172402/BBDown_GUI/releases) 

预打包好的二进制文件，包括
- BBDown - GUI
- BBDown
- FFmpeg
- Aria2c

### 从 [PyPI](https://pypi.org/project/BBDown-GUI/) 安装使用  [![](https://img.shields.io/pypi/v/BBDown_GUI)](https://pypi.org/project/BBDown-GUI/) 

安装

```
pip install BBDown-GUI
```

运行（不区分大小写，下划线可省略）
```
BBDown_GUI
```

### 从源码运行使用
```
pip install -r requirements.txt
python -m BBDown_GUI
```

### 从[持续集成](https://github.com/1299172402/BBDown_GUI/actions/workflows/build.yml)中下载(beta version) [![Pack Python application](https://github.com/1299172402/BBDown_GUI/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/1299172402/BBDown_GUI/actions/workflows/build.yml)
进入Actions，选择Pack Python application，进入需要下载的工作流
![image](https://github.com/1299172402/BBDown_GUI/assets/29673994/d7944b79-ae96-4c6a-9892-f8e7d3238a61)
到下方Artifacts下载BBDown_GUI
![image](https://github.com/1299172402/BBDown_GUI/assets/29673994/45c92ba5-80cc-47db-b5cc-8abe23de2078)



## 屏幕截图

### 简易模式

<img src="https://user-images.githubusercontent.com/29673994/169644975-066c4ac5-7fb1-4361-8c62-bb1e5aba4381.png" height="50%" width="50%" >

### 高级模式

<img src="https://user-images.githubusercontent.com/29673994/200099369-51250aa4-bd7f-4547-864c-f552143adcc1.png">


## 致谢&License

 - https://github.com/nilaoda/BBDown (MIT License)

## 相关Repository

 - [BBDown_hk](https://github.com/1299172402/BBDown_hk)

## 更新日志

添加以下参数的支持(BBDown v1.5.4)：

| 参数                        | 功能                                                         |
| --------------------------- | ------------------------------------------------------------ |
| --force-http                | 下载音视频时强制使用HTTP协议替换HTTPS(默认开启)              |
| --skip-ai                   | 跳过AI字幕下载                                               |
| --aria2c-args <aria2c-args> | 调用aria2c的附加参数(默认参数包含"-x16 -s16 -j16 -k 5M") |
| --host <host>               | 指定BiliPlus host(**解析服务器能够获取你账号的大部分权限!**)     |
| --ep-host <ep-host>         | 指定BiliPlus EP host                                         |
| --area <area>               | 指定BiliPlus area 例: hk(使用BiliPlus需要access_token, 不需要cookie) |

<!-- | [未添加]--bandwith-ascending        | 比特率升序(最小体积优先)                                     | -->


