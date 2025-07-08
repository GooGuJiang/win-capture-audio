"""Thin Python wrapper for win-capture-audio-wrapper.dll"""
import ctypes
from ctypes import wintypes
import os
import wave
import struct
import time

_kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

TH32CS_SNAPPROCESS = 0x00000002

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', wintypes.DWORD),
        ('cntUsage', wintypes.DWORD),
        ('th32ProcessID', wintypes.DWORD),
        ('th32DefaultHeapID', ctypes.POINTER(ctypes.c_ulong)),
        ('th32ModuleID', wintypes.DWORD),
        ('cntThreads', wintypes.DWORD),
        ('th32ParentProcessID', wintypes.DWORD),
        ('pcPriClassBase', ctypes.c_long),
        ('dwFlags', wintypes.DWORD),
        ('szExeFile', wintypes.WCHAR * wintypes.MAX_PATH),
    ]

_kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
_kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
_kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
_kernel32.Process32FirstW.restype = wintypes.BOOL
_kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
_kernel32.Process32NextW.restype = wintypes.BOOL
_kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
_kernel32.CloseHandle.restype = wintypes.BOOL


def _find_pid_by_name(name):
    snapshot = _kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    entry = PROCESSENTRY32()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
    pid = None
    if _kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
        while True:
            if entry.szExeFile.lower() == name.lower():
                pid = entry.th32ProcessID
                break
            if not _kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                break
    _kernel32.CloseHandle(snapshot)
    return pid


_DLL = None


def _load_dll(path=None):
    global _DLL
    if _DLL is None:
        if path is None:
            path = os.path.join(os.path.dirname(__file__), 'win-capture-audio-wrapper.dll')
        _DLL = ctypes.WinDLL(path)
        _DLL.sca_create_capture.argtypes = [wintypes.DWORD, wintypes.UINT, wintypes.USHORT]
        _DLL.sca_create_capture.restype = ctypes.c_void_p
        _DLL.sca_read_audio_frames.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), wintypes.UINT]
        _DLL.sca_read_audio_frames.restype = wintypes.UINT
        _DLL.sca_destroy_capture.argtypes = [ctypes.c_void_p]
        _DLL.sca_destroy_capture.restype = None
    return _DLL


class Capture:
    """Capture audio from a specific process."""

    def __init__(self, pid=None, name=None, sample_rate=48000, channels=2, dll_path=None):
        if pid is None:
            if name is None:
                raise ValueError('pid or name required')
            pid = _find_pid_by_name(name)
            if pid is None:
                raise RuntimeError(f'process {name} not found')
        self._dll = _load_dll(dll_path)
        self.handle = self._dll.sca_create_capture(pid, sample_rate, channels)
        if not self.handle:
            raise RuntimeError('failed to create capture helper')
        self.rate = sample_rate
        self.channels = channels

    def read(self, frames):
        buf = (ctypes.c_float * (frames * self.channels))()
        got = self._dll.sca_read_audio_frames(self.handle, buf, frames)
        return list(buf[:got * self.channels])

    def stream(self, frames_per_buffer=1024):
        """Yield chunks of audio in real time."""
        while self.handle:
            data = self.read(frames_per_buffer)
            if data:
                yield data
            else:
                time.sleep(frames_per_buffer / self.rate)

    def close(self):
        if self.handle:
            self._dll.sca_destroy_capture(self.handle)
            self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def record_to_wav(pid=None, name=None, seconds=5, filename='capture.wav', sample_rate=48000, channels=2, dll_path=None):
    """Record audio from the given process and write it to a WAV file."""
    frames = sample_rate * seconds
    with Capture(pid=pid, name=name, sample_rate=sample_rate, channels=channels, dll_path=dll_path) as cap:
        data = []
        remaining = frames
        while remaining > 0:
            chunk = cap.read(min(1024, remaining))
            if not chunk:
                break
            data.extend(chunk)
            remaining -= len(chunk) // channels
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(4)
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(struct.pack('<f', s) for s in data))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python wca.py <pid|process.exe> <seconds> [output.wav]')
        sys.exit(1)
    target = sys.argv[1]
    try:
        pid = int(target)
        name = None
    except ValueError:
        pid = None
        name = target
    seconds = int(sys.argv[2])
    out = sys.argv[3] if len(sys.argv) > 3 else 'capture.wav'
    record_to_wav(pid=pid, name=name, seconds=seconds, filename=out)
    print('Wrote', out)
