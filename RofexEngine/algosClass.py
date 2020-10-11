class algos:
    def __init__(self, actualMarket, tickers):
        self.actualMarket = actualMarket
        self.tickers=tickers

    def goRobot(self):
        #print(self.actualMarket)
        self.ratio2Tickers()

    def addMsgToDict(self, lastMsg):
        self.actualMarket[lastMsg['instrumentId']['symbol']] = lastMsg
        #self.printFormatedMsg(lastMsg)

    def printFormatedMsg(self,last):
        actual=last
        ticker=self.getTicker(actual)
        bidPrice = self.getBidPx(actual)
        bidSize = self.getBidSize(actual)
        offerPrice = self.getOfferPx(actual)
        offerSize = self.getOfferSize(actual)
        print(ticker + "line-->  " + str(bidPrice) + " / " + str(offerPrice) + "   " + str(bidSize) + " / " + str(offerSize))

    def ratio2Tickers(self):

        keys = self.actualMarket.keys()

        for k in keys:
            actual=self.actualMarket[k]
            bidPrice = self.getBidPx(actual)
            bidSize = self.getBidSize(actual)
            offerPrice = self.getOfferPx(actual)
            offerSize = self.getOfferSize(actual)
            print(k + "--->  " + str(bidPrice) + " / " + str(offerPrice) + "   " + str(bidSize) + " / " + str(offerSize))

            if len(self.actualMarket) == 2:

                bidRF = self.getBidPx(self.actualMarket[self.tickers[0]])
                offRF = self.getOfferPx(self.actualMarket[self.tickers[0]])
                bidDO = self.getBidPx(self.actualMarket[self.tickers[1]])
                offDO = self.getOfferPx(self.actualMarket[self.tickers[0]])

                if bidDO != 0 and offDO != 0:
                    # print("RFX20Dic20 en USD: " + str(bidRF / offDO)+ " / " + str(offRF/bidDO))
                    print(
                        "**********RFX20Dic20 en USD: " + "{:.2f}".format(bidRF / offDO) + " / " + "{:.2f}".format(
                            offRF / bidDO))



    ### msg parser
    @staticmethod
    def getTicker(msg):
        return msg['instrumentId']['symbol']

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

    def getBidDictActualMkt(self, ticker):
        return self.getBidPx(self.actualMarket[ticker])

    def getBidSizeDictActualMkt(self, ticker):
        return self.getBidSize(self.actualMarket[ticker])
