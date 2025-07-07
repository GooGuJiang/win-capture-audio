# win-capture-audio-dll

这是一个基于 [win-capture-audio](https://github.com/bozbez/win-capture-audio) 项目提取出的 DLL 接口，可用于从指定进程捕获音频流，适用于需要在 Python 中采集特定应用程序音频的场景。

其底层基于 Windows 的 [ActivateAudioInterfaceAsync](https://docs.microsoft.com/en-us/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync) API，结合 [AUDIOCLIENT\_PROCESS\_LOOPBACK\_PARAMS](https://docs.microsoft.com/en-us/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_process_loopback_params) 结构实现，能够直接捕获某一进程的输出音频，而不是系统整体输出。

> ⚠️ 注意：该功能官方仅在 Windows 11 支持，但经测试在部分更新后的 Windows 10（如 2004 及以上）中也可以正常使用。

---

## 环境要求

* Windows 10 2004（2020 年 5 月）及以上版本（推荐 Windows 11）
* 已编译的 `win-capture-audio-wrapper.dll`

---

## 功能特点

* 低延迟：不依赖 WASAPI Loopback 或虚拟声卡，直接内部环回目标进程音频
* 精准：仅采集指定进程，不影响系统或其他应用
* 可嵌入：适合集成进 Python 应用或 AI 音频分析工具链
