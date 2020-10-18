import sys
import argparse
import quickfix as fix


from RofexEngine.MarketDataEntries import MarketEntries
from Initiator.algos.ratioTest import ratioTest
from RofexEngine.suscriptionObject import suscriptionObjet
from RofexEngine.usrPswd import userID


class main:

    def __init__(self, config_file, usr1, targetCompID, suscribeObj):
        self.config_file = config_file
        self.targetCompID = targetCompID

        self.usrId = userID.getUsr(usr1)
        self.pswd = userID.getPswd(usr1)

        self.tickers = suscriptionObjet.getTickers(suscribeObj)
        self.entries = suscriptionObjet.getEntries(suscribeObj)

        try:
            self.settings = fix.SessionSettings(self.config_file)
            # self.myFixApplication = rofexEngine(self.usrId, self.pswd, self.targetCompID, self.tickers, self.entries)
            self.myFixApplication = ratioTest(self.usrId, self.pswd, self.targetCompID, self.tickers, self.entries)
            self.storefactory = fix.FileStoreFactory(self.settings)
            self.logfactory = fix.FileLogFactory(self.settings)
            self.initiator = fix.SocketInitiator(self.myFixApplication, self.storefactory, self.settings,
                                                 self.logfactory)

            """
            * Se puede iniciar desde aca
            
            self.initiator.start()
            self.myFixApplication.run()
            self.initiator.stop()
            """
        except (fix.ConfigError, fix.RuntimeError) as e:

            print(e)
            self.initiator.stop()
            sys.exit()

    def run(self):

        while 1:
            # time.sleep(2)
            action = self.queryAction()
            if action == '1':
                print(action)
                self.myFixApplication.suscribeMD()

            elif action == '2':
                print(action)
                # msg = msgToRofex.secList()

            elif action == '3':
                self.myFixApplication.printAllSecurities()
                print(action)
            elif action == '4':
                # print(self.actualMarket)
                print(action)

            elif action == '5':
                print(action)
                break

        fixMain.initiator.stop()

    def queryAction(self):
        print("1) -----\n2) SecList\n3) Print allSecuritiesList\n4) Actual Market\n5) Quit")
        action = input("Action:\n")
        return action


if __name__ == '__main__':
    # rofexLogon('Initiator\configuration\primaryInitiator.cfg','pjseoane232','AiZkiC5#')

    parser = argparse.ArgumentParser(description='FIX Client Configuration')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()

    user = userID('pjseoane232', 'AiZkiC5#')
    suscribeTuple = ['RFX20Dic20', 'DODic20']

    entries = [MarketEntries.Bid,
               MarketEntries.Offer,
               MarketEntries.Trade,
               MarketEntries.Index,
               MarketEntries.Open,
               MarketEntries.Close,
               MarketEntries.Settlement,
               MarketEntries.High,
               MarketEntries.Low,
               MarketEntries.Vol,
               MarketEntries.CashVol,
               MarketEntries.TradeVol,
               MarketEntries.OpInt,
               MarketEntries.AuctionPrice,
               MarketEntries.RefPrice
               ]

    suscribe = suscriptionObjet(suscribeTuple, entries)

    fixMain = main(args.file_name, user, 'ROFX', suscribe)

    # time.sleep(3)
    # fixMain.myFixApplication.suscribeMD2(suscribeTuple, entries)

    # fixMain.suscribeMD3(suscribeTuple, entries2)
    fixMain.initiator.start()

    fixMain.run()
