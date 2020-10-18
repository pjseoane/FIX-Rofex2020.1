from RofexEngine.RofexEngine import rofexEngine


class ratioTest(rofexEngine):
    def __init__(self, usr, pswd, targetCompId, tickers, entries):
        super().__init__(usr, pswd, targetCompId, tickers, entries)

        self.algoName = "2Tickets"
        self.ratioBid = 0
        self.ratioOffer = 0

    def goRobot(self):
        print(self.algoName + "-------------------------------------------")
        # print(self.actualMarket)

        self.ticker = self.getTicker(self.lastMsg)
        self.bidPrice = self.getBidPx(self.lastMsg)
        self.bidSize = self.getBidSize(self.lastMsg)
        self.offerPrice = self.getOfferPx(self.lastMsg)
        self.offerSize = self.getOfferSize(self.lastMsg)
        self.tradeVol = self.getTradeVol(self.lastMsg)
        self.LastPx = self.getLastPx(self.lastMsg)
        self.LastSize = self.getLastSize(self.lastMsg)
        self.ratio2Tickers()

        self.printTickerMkt()
        self.printRatio2Tickers()
        #print(self.lastMsg)

    def printTickerMkt(self):

        print(self.ticker + " bid / ask: " + str(self.bidPrice) + " / " + str(self.offerPrice) + "     " + str(
            self.bidSize) + " / " + str(
            self.offerSize) + " ************Last: " + str(self.LastPx) + " / " + str(self.LastSize) + " " + "Trade Vol: " + str(
            self.tradeVol))

    def printRatio2Tickers(self):
        print("Ratio 2 Tickers " + "{:.2f}".format(self.ratioBid) + " / " + "{:.2f}".format(self.ratioOffer))

    def ratio2Tickers(self):
        if len(self.actualMarket) == 2:
            self.bidt0 = self.getBidPx(self.actualMarket[self.tickers[0]])
            self.offt0 = self.getOfferPx(self.actualMarket[self.tickers[0]])
            self.bidt1 = self.getBidPx(self.actualMarket[self.tickers[1]])
            self.offt1 = self.getOfferPx(self.actualMarket[self.tickers[1]])

            if self.bidt1 != 0 and self.offt1 != 0:
                self.ratioBid = self.bidt0 / self.offt1
                self.ratioOffer = self.offt0 / self.bidt1
