<<<<<<< HEAD
# win-capture-audio
=======
# win-capture-audio-dll
>>>>>>> 8fde96b94b38d5bbc7e1efe53f4c6a764eb870d6

An OBS plugin similar to OBS's win-capture/game-capture that allows for audio capture from a specific application, rather than the system's audio as a whole. This eliminates the need for third-party software or hardware audio mixing tools that introduce complexity, and in the case of software tools, introduce mandatory latency.

<<<<<<< HEAD
Internally it uses [ActivateAudioInterfaceAsync](https://docs.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync) with [AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS](https://docs.microsoft.com/en-us/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_process_loopback_params). This initialization structure is only officially available on Windows 11, however it appears to work additionally on relatively recent versions of Windows 10.

**This plugin is in a BETA state, expect issues - [https://discord.gg/4D5Yk5gFnM](https://discord.gg/4D5Yk5gFnM) for support and updates.**<br/>
**An updated version of Windows 10 2004 (released 2020-05-27) or later is required.**

**Want to support the development of the plugin? [https://ko-fi.com/bozbez](https://ko-fi.com/bozbez)**
=======

其底层基于 Windows 的 [ActivateAudioInterfaceAsync](https://docs.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync) API，结合 [AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS](https://docs.microsoft.com/en-us/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_process_loopback_params) 结构实现，能够直接捕获某一进程的输出音频，而不是系统整体输出。

> ⚠️ 注意：该功能官方仅在 Windows 11 支持，但经测在部分更新后的 Windows 10（如 2004 及以上）中也可以正常使用。
>>>>>>> 8fde96b94b38d5bbc7e1efe53f4c6a764eb870d6

![overview](https://raw.githubusercontent.com/bozbez/win-capture-audio/main/media/overview.png)

<<<<<<< HEAD
## Installation and Usage

1. Head over to the [Releases](https://github.com/bozbez/win-capture-audio/releases) page and download the latest installer (or zip if you are using a portable installation)
2. Run the setup wizard, selecting your root OBS folder (`obs-studio/`, _not_ `obs-studio/obs-plugins/`) when asked (or extract the zip to the portable OBS root directory)
3. Launch OBS and check out the newly available "Application Audio Output Capture" source
=======
- Windows 10 2004（2020 年 5 月）及以上版本（推荐 Windows 11）
- 已编译的 `win-capture-audio-wrapper.dll`
>>>>>>> 8fde96b94b38d5bbc7e1efe53f4c6a764eb870d6

## Troubleshooting

<<<<<<< HEAD
- **Application Audio Output Capture source not showing up after install:** this means that either your OBS is out-of-date (check that it is at least 27.1.x) or you have installed the plugin to the wrong location. To re-install, first uninstall via "Add or remove programs" in the Windows settings, and then run the installer again. Make sure to select the top-level `obs-studio/` folder in (probably) `C:/Program Files/`.

- **Application Audio Output Capture source not picking up any audio:** this happens when your Windows is too old and does not have support for the API. Note that even if you have a more recent major version such as `20H2` you will still need the latest updates for the plugin to work. If you are on a very old version you might need more than one update for this to work, and the second update might not show up for a few days after the first update.
=======
- 低延迟：不依赖 WASAPI Loopback 或虚拟声卡，直接内部环回目标进程音频
- 精准：仅采集指定进程，不影响系统或其他应用
- 可嵌入：适合集成进 Python 应用或 AI 音频分析工具链

## 获取 DLL

前往 [Releases](../../releases) 页面可以获取最新的 `win-capture-audio-wrapper.dll`，与 `samples` 目录中的脚本放在同一位置后即可被 `wca.py` 自动加载。

## Python 用法说明

该仓库还构建了一个轻量级的 DLL，并通过一个精简的 C 接口（C API）对外暴露功能。`samples/wca.py` 模块对这个 DLL 提供了一个简单易用的 Python 封装接口，可以通过进程名解析目标进程，并以实时流的方式捕获音频数据。

```python
from samples.wca import Capture, record_to_wav

# 从指定 PID 的进程中保存 5 秒音频到文件
record_to_wav(pid=1234, seconds=5, filename="capture.wav")

# 或者通过进程名捕获音频
record_to_wav(name="chrome.exe", seconds=5, filename="chrome.wav")

# 也可以直接使用 Capture 类进行更灵活的操作
with Capture(name="notepad.exe") as cap:
    for chunk in cap.stream():
        process(chunk)  # 对音频数据执行处理操作
```

详细实现与更多用法，请参考 [`samples/wca.py`](samples/wca.py)。


>>>>>>> 8fde96b94b38d5bbc7e1efe53f4c6a764eb870d6
