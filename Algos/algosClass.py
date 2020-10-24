class algos:
    def __init__(self, actualMarket, tickers, lastMsg):
        self.actualMarket = actualMarket
        self.tickers = tickers
        self.lastMsg = lastMsg

        self.ratioBid = 0
        self.ratioOffer = 0

    def goRobot(self):

        # self.printTickerMkt()
        self.printActualMkt()
        self.ratio2Tickers()
        self.printRatio2Tickers()

    def printActualMkt(self):
        keys = self.actualMarket.keys()
        for k in keys:
            print(k + "   " + str(self.getFieldValue(k, 'BI', 'price')) + " / " + str(
                self.getFieldValue(k, 'OF', 'price')) + "   " +
                  str(self.getFieldValue(k, 'BI', 'size')) + " /  " +
                  str(self.getFieldValue(k, 'OF', 'size')) + "     " + "Last :" +
                  str(self.getFieldValue(k, 'LA', 'price')) + "    " +
                  str(self.getFieldValue(k, 'LA', 'size')))
        # print("***********************  *********** ************* ************ *********** ")

    def printRatio2Tickers(self):
        print("Ratio 2 Tickers: " + "{:.2f}".format(self.ratioBid) + " / " + "{:.2f}".format(self.ratioOffer))
        print("--------------------------------------------------")

    def ratio2Tickers(self):

       # keys = self.actualMarket.keys()

        # print('-------------------------------------------------')
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
