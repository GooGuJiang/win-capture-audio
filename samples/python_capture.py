"""Example script using the simple Python wrapper."""

from wca import record_to_wav


def main():
    import sys
    if len(sys.argv) < 2:
        print('Usage: python python_capture.py <pid>')
        return

    pid = int(sys.argv[1])
    record_to_wav(pid, 5, 'capture.wav')
    print('Wrote capture.wav')


if __name__ == '__main__':
    main()
