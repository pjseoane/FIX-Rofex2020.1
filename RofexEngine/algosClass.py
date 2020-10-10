class algos:
    def __init__(self, actualMarket):
        self.actualMarket = actualMarket

    def goRobot(self):
        self.printMktDict()

    def printMktDict(self):
        keys = self.actualMarket.keys()

        for k in keys:
            actual=self.actualMarket[k]
            bidPrice = self.getBidPx(actual)
            bidSize = self.getBidSize(actual)
            offerPrice = self.getOfferPx(actual)
            offerSize = self.getOfferSize(actual)
            print(k + "-->" + str(bidPrice) + " / " + str(offerPrice) + "   " + str(bidSize) + " / " + str(offerSize))

            if len(self.actualMarket) == 2:
                bidRF = self.getBidPx(self.actualMarket['RFX20Dic20'])
                offRF = self.getOfferPx(self.actualMarket['RFX20Dic20'])
                bidDO = self.getBidPx(self.actualMarket['DODic20'])
                offDO = self.getOfferPx(self.actualMarket['DODic20'])

                if bidDO != 0 and offDO != 0:
                    # print("RFX20Dic20 en USD: " + str(bidRF / offDO)+ " / " + str(offRF/bidDO))
                    print(
                        "*RFX20Dic20 en USD: " + "{:.2f}".format(bidRF / offDO) + " / " + "{:.2f}".format(
                            offRF / bidDO))

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
