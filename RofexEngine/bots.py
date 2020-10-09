import quickfix as fix
import quickfix50sp2 as fix50
#from RofexEngine.RofexEngine import rofexEngine as e


def printRatio(actualMarket):
    keys = self.actualMarket.keys()

    for k in keys:
        bidPrice = self.getBidPx(self.actualMarket[k])
        bidSize = self.getBidSize(self.actualMarket[k])
        offerPrice = self.getOfferPx(self.actualMarket[k])
        offerSize = self.getOfferSize(self.actualMarket[k])
        print(k + "-->" + str(bidPrice) + " / " + str(offerPrice) + "   " + str(bidSize) + " / " + str(offerSize))

        if len(self.actualMarket) == 2:
            bidRF = self.getBidPx(self.actualMarket['RFX20Dic20'])
            offRF = self.getOfferPx(self.actualMarket['RFX20Dic20'])
            bidDO = self.getBidPx(self.actualMarket['DODic20'])
            offDO = self.getOfferPx(self.actualMarket['DODic20'])

            if bidDO != 0 and offDO != 0:
                # print("RFX20Dic20 en USD: " + str(bidRF / offDO)+ " / " + str(offRF/bidDO))
                print(
                    "RFX20Dic20 en USD: " + "{:.2f}".format(bidRF / offDO) + " / " + "{:.2f}".format(offRF / bidDO))
