class algos:
    def __init__(self, actualMarket, tickers):
        self.actualMarket = actualMarket
        self.tickers=tickers

    def goRobot(self):
        print(self.actualMarket)
        self.ratio2Tickers()

    def printFormatedMsg(self,last):
        actual=last
        ticker=self.getTicker(actual)
        bidPrice = self.getBidPx(actual)
        bidSize = self.getBidSize(actual)
        offerPrice = self.getOfferPx(actual)
        offerSize = self.getOfferSize(actual)
        last=self.getLast(actual)
        print(ticker + " Bid / Ask / Last-->  " + str(bidPrice) + " / " + str(offerPrice) + "   " + str(bidSize) + " / " + str(offerSize) + " Last "+ str(last))

    def ratio2Tickers(self):

        keys = self.actualMarket.keys()

        print('-------------------------------------------------')
        for k in keys:
            self.printFormatedMsg(self.actualMarket[k])

            if len(self.actualMarket) == 2:

                bidt0 = self.getBidPx(self.actualMarket[self.tickers[0]])
                offt0 = self.getOfferPx(self.actualMarket[self.tickers[0]])
                bidt1 = self.getBidPx(self.actualMarket[self.tickers[1]])
                offt1 = self.getOfferPx(self.actualMarket[self.tickers[1]])

                if bidt1 != 0 and offt1 != 0:
                    # print("RFX20Dic20 en USD: " + str(bidRF / offDO)+ " / " + str(offRF/bidDO))
                    print(
                        "**********RFX20Dic20 en USD: " + "{:.2f}".format(bidt0 / offt1) + " / " + "{:.2f}".format(
                            offt0 / bidt1))



    ### msg parser
    @staticmethod
    def getTicker(msg):
        return msg['instrumentId']['symbol']
        #return msg['instrumentId']
    @staticmethod
    def getBidPx(msg):
        if len((msg['marketData']['BI'])) > 0:
            return msg['marketData']['BI'][0]['price']
        else:
            return 0

    @staticmethod
    def getOfferPx(msg):
        if len((msg['marketData']['OF'])) > 0:
            return msg['marketData']['OF'][0]['price']
        else:
            return 0


    @staticmethod
    def getBidSize(msg):
        if len((msg['marketData']['BI'])) > 0:
            return msg['marketData']['BI'][0]['size']
        else:
            return 0

    @staticmethod
    def getOfferSize(msg):
        if len((msg['marketData']['OF'])) > 0:
            return msg['marketData']['OF'][0]['size']
        else:
            return 0

    @staticmethod
    def getLast(msg):
        """
        if len((msg['marketData']['TV'])) > 0:
            return msg['marketData']['TV'][0]['price']
        else:
            return 0
        """
        return 0


    def getBidDictActualMkt(self, ticker):
        return self.getBidPx(self.actualMarket[ticker])

    def getBidSizeDictActualMkt(self, ticker):
        return self.getBidSize(self.actualMarket[ticker])
