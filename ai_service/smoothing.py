from collections import deque

class Smoother:
    def __init__(self, window_size=5):
        self.window = deque(maxlen=window_size)

    def smooth(self, count):
        self.window.append(count)
        return sum(self.window) / len(self.window)
