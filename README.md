# win-capture-audio-dll

这是一个基于 [win-capture-audio](https://github.com/bozbez/win-capture-audio) 项目提取出的 DLL 接口，可用于从指定进程捕获音频流，适用于需要在 Python 中采集特定应用程序音频的场景。


其底层基于 Windows 的 [ActivateAudioInterfaceAsync](https://docs.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync) API，结合 [AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS](https://docs.microsoft.com/en-us/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_process_loopback_params) 结构实现，能够直接捕获某一进程的输出音频，而不是系统整体输出。

> ⚠️ 注意：该功能官方仅在 Windows 11 支持，但经测在部分更新后的 Windows 10（如 2004 及以上）中也可以正常使用。

## 环境要求

- Windows 10 2004（2020 年 5 月）及以上版本（推荐 Windows 11）
- 已编译的 `win-capture-audio-wrapper.dll`

## 功能特点

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

