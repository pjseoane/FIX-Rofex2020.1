import os

from RofexEngine.RofexEngine import rofexEngine


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


class myApplication(rofexEngine):

    def __init__(self, usr, pswd, targetCompId, tickers, entries):
        super().__init__(usr, pswd, targetCompId, tickers, entries)
        self.previousLast = None
        self.Last = None

        self.ratioBid = 0
        self.ratioOffer = 0

    def goRobot2(self):
        # clear()
        # os.system('clear')
       #self.getPreviousLast()
        #
        self.updateActualMktDict()
        # self.printActualMktDict()
        # self.processTick()
        self.printActualMkt()
        self.ratio2Tickers()
        self.printRatio2Tickers()

    def updateActualMktDict(self):
        ticker = self.lastMsg['instrumentId']['symbol']
        #self.previousLast = self.getPreviousLast()
        self.actualMarket[self.lastMsg['instrumentId']['symbol']] = self.lastMsg

        self.actualMarket[ticker] = self.lastMsg
        self.Last = self.getFieldValue(ticker, 'LA', 'price')
        print("+++++++++ PLast:" + str(self.previousLast))
        print("+++++++++ Last :" + str(self.Last))
        self.previousLast=self.Last
    def getPreviousLast(self):
        if len(self.actualMarket) > 2:
            ticker = self.lastMsg['instrumentId']['symbol']
            return self.getFieldValue(ticker, 'LA', 'price')
        else:
            return 0


    def processTick(self):
        # toma el precio del dict antes de actualizar
        ticker = self.actualMarket['instrumentId']['symbol']
        # previousLast= self.getFieldValue(ticker,)

        pass

    def printActualMkt(self):
        # clear()
        # os.system('cls')
        keys = self.actualMarket.keys()
        for k in keys:
            print(k + "   " +
                  str(self.getFieldValue(k, 'BI', 'price')) + " / " +
                  str(self.getFieldValue(k, 'OF', 'price')) + "   " +
                  str(self.getFieldValue(k, 'BI', 'size')) + " / " +
                  str(self.getFieldValue(k, 'OF', 'size')) + "     " + "Last :" +
                  str(self.getFieldValue(k, 'LA', 'price')) + "     " +
                  str(self.getFieldValue(k, 'LA', 'size')) + "     " + "Previous Last :" +
                  str(self.previousLast) + "   " + " Close :" +
                  str(self.getFieldValue(k, 'CL', 'price')))
        # print("***********************  *********** ************* ************ *********** ")

    def printRatio2Tickers(self):
        print("Ratio 2 Tickers: " + "{:.2f}".format(self.ratioBid) + " / " + "{:.2f}".format(self.ratioOffer))
        print("--------------------------------------------------")

    def ratio2Tickers(self):

        if len(self.actualMarket) == 2:

            bidt0 = self.getFieldValue(self.tickers[0], 'BI', 'price')
            offt0 = self.getFieldValue(self.tickers[0], 'OF', 'price')

            bidt1 = self.getFieldValue(self.tickers[1], 'BI', 'price')
            offt1 = self.getFieldValue(self.tickers[1], 'OF', 'price')

            if offt1 != 0:
                self.ratioBid = bidt0 / offt1

            if bidt1 != 0:
                self.ratioOffer = offt0 / bidt1

    def getFieldValue(self, ticker, field, value) -> object:
        return self.getFieldValueByMsg(self.actualMarket[ticker], field, value)

    @staticmethod
    def getFieldValueByMsg(msg, Field, Value):
        if len((msg['marketData'][Field])) > 0:
            return msg['marketData'][Field][0][Value]
        else:
            return 0
