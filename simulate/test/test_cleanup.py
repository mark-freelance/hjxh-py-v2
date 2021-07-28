import atexit
import signal
import time


def f1():
    print('hello')


def f2(code, frame):
    print("code", code)
    print("frame", frame)
    print('bye')


class A:
    def __init__(self):
        self.name = 'xxx'
        atexit.register(self.cleanup)
    
    def cleanup(self):
        print(self.name + ' exited')


if __name__ == '__main__':
    atexit.register(f1)
    print('=== start ===')
    a = A()
    # signal.signal(signal.SIGINT, a.cleanup)
    signal.signal(signal.SIGINT, f2)
    time.sleep(10)
