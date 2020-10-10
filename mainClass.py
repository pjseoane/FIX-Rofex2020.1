import sys
import argparse
import time
import configparser
from threading import Thread
import quickfix as fix
from RofexEngine.RofexEngine import rofexEngine
#from RofexEngine.bots import bots


class main:
    def __init__(self, config_file, usrId, pswd, targetCompID, tickers):
    #def __init__(self, config_file, usrId, pswd, targetCompID):
        self.config_file = config_file
        self.usrId = usrId
        self.pswd = pswd
        self.targetCompID = targetCompID
        self.tickers = tickers

        try:
            self.settings = fix.SessionSettings(self.config_file)
            self.myFixApplication = rofexEngine(self.usrId, self.pswd, self.targetCompID, self.tickers)
            #self.myFixApplication = rofexEngine(self.usrId, self.pswd, self.targetCompID)
            self.storefactory = fix.FileStoreFactory(self.settings)
            self.logfactory = fix.FileLogFactory(self.settings)
            self.initiator = fix.SocketInitiator(self.myFixApplication, self.storefactory, self.settings,self.logfactory)

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


if __name__ == '__main__':
    # rofexLogon('Initiator\configuration\primaryInitiator.cfg','pjseoane232','AiZkiC5#')

    parser = argparse.ArgumentParser(description='FIX Client Configuration')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()

    suscribeTuple = ['RFX20Dic20', 'DODic20','DOOct20']
    entries=['0', '1', '2', '4', '5', '6', '7', '8', 'B', 'C']

    fixMain = main(args.file_name, 'pjseoane232', 'AiZkiC5#', 'ROFX', suscribeTuple)
    #fixMain = main(args.file_name, 'pjseoane232', 'AiZkiC5#', 'ROFX')

    fixMain.initiator.start()
    #fixMain.myFixApplication.suscribeMD(suscribeTuple,entries)
    fixMain.myFixApplication.selectAlgo(rofexEngine.goRobot4)
    fixMain.myFixApplication.run()

    #fixMain.myFixApplication.printActualMKT()
    # fixMain.myFixApplication.printAllSecurities()
    fixMain.initiator.stop()
