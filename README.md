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

## Python Usage

The repository also builds a lightweight DLL that exposes a minimal C API. The helper module [`samples/wca.py`](samples/wca.py) wraps this DLL with an easy to use interface. It can resolve a process by name and stream audio chunks for real-time processing.

```python
from samples.wca import Capture, record_to_wav

# Save five seconds of audio from the given PID
record_to_wav(pid=1234, seconds=5, filename="capture.wav")

# Or capture by executable name
record_to_wav(name="chrome.exe", seconds=5, filename="chrome.wav")

# Or use the class directly
with Capture(name="notepad.exe") as cap:
    for chunk in cap.stream():
        process(chunk)  # do something with audio data
```

See [`samples/wca.py`](samples/wca.py) for the implementation and additional usage details.
