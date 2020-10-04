from RofexEngine.RofexEngine8 import rofexEngine

class suscribeMD(rofexEngine):
    def __init__(self, ticker):
        super().__init__()

        self.ticker=ticker

    def goRobot(self):
        super().goRobot()

