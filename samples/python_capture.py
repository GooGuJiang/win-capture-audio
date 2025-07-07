import ctypes
from ctypes import wintypes
import wave

# Load the DLL built from this repository
wca = ctypes.WinDLL('win-capture-audio-wrapper.dll')

# Function prototypes
wca.sca_create_capture.argtypes = [wintypes.DWORD, wintypes.UINT, wintypes.USHORT]
wca.sca_create_capture.restype = ctypes.c_void_p

wca.sca_read_audio_frames.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), wintypes.UINT]
wca.sca_read_audio_frames.restype = wintypes.UINT

wca.sca_destroy_capture.argtypes = [ctypes.c_void_p]
wca.sca_destroy_capture.restype = None

class Capture:
    def __init__(self, pid, sample_rate=48000, channels=2):
        self.handle = wca.sca_create_capture(pid, sample_rate, channels)
        if not self.handle:
            raise RuntimeError('failed to create capture helper')
        self.rate = sample_rate
        self.channels = channels

    def read(self, frames):
        buf = (ctypes.c_float * (frames * self.channels))()
        got = wca.sca_read_audio_frames(self.handle, buf, frames)
        return buf[:got * self.channels]

    def close(self):
        if self.handle:
            wca.sca_destroy_capture(self.handle)
            self.handle = None

if __name__ == '__main__':
    import sys, time, struct
    if len(sys.argv) < 2:
        print('Usage: python python_capture.py <pid>')
        sys.exit(1)
    pid = int(sys.argv[1])
    cap = Capture(pid)
    seconds = 5
    total_frames = cap.rate * seconds
    data = cap.read(total_frames)
    cap.close()

    with wave.open('capture.wav', 'wb') as wf:
        wf.setnchannels(cap.channels)
        wf.setsampwidth(4)
        wf.setframerate(cap.rate)
        wf.writeframes(b''.join(struct.pack('<f', s) for s in data))
    print('Wrote capture.wav')
