import ctypes
from ctypes import wintypes
import os
import wave
import struct


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
    """Capture audio from a specific process ID."""

    def __init__(self, pid, sample_rate=48000, channels=2, dll_path=None):
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

    def close(self):
        if self.handle:
            self._dll.sca_destroy_capture(self.handle)
            self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def record_to_wav(pid, seconds, filename, sample_rate=48000, channels=2, dll_path=None):
    """Record audio from the given process and write it to a WAV file."""
    frames = sample_rate * seconds
    with Capture(pid, sample_rate, channels, dll_path) as cap:
        data = cap.read(frames)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(4)
        wf.setframerate(sample_rate)
        for sample in data:
            wf.writeframes(struct.pack('<f', sample))


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python wca.py <pid> <seconds> [output.wav]')
        sys.exit(1)
    pid = int(sys.argv[1])
    seconds = int(sys.argv[2])
    out = sys.argv[3] if len(sys.argv) > 3 else 'capture.wav'
    record_to_wav(pid, seconds, out)
    print('Wrote', out)
