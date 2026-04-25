class AlertLogic:
    def __init__(self, threshold):
        self.threshold = threshold

    def check(self, count):
        if count > self.threshold:
            return "OVERLOAD"
        return "NORMAL"
