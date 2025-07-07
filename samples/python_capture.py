"""Example script using the simple Python wrapper."""

from wca import record_to_wav


def main():
    import sys
    if len(sys.argv) < 2:
        print('Usage: python python_capture.py <pid|process.exe>')
        return

    target = sys.argv[1]
    try:
        pid = int(target)
        name = None
    except ValueError:
        pid = None
        name = target

    record_to_wav(pid=pid, name=name, seconds=5, filename='capture.wav')
    print('Wrote capture.wav')


if __name__ == '__main__':
    main()
