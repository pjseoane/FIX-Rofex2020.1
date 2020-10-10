import sys
import argparse
import time
import configparser
from threading import Thread
import quickfix as fix
from RofexEngine.RofexEngine import rofexEngine


class main:
    def __init__(self, config_file, usrId, pswd, targetCompID, tickers):

        self.config_file = config_file
        self.usrId = usrId
        self.pswd = pswd
        self.targetCompID = targetCompID
        self.tickers = tickers

        try:
            self.settings = fix.SessionSettings(self.config_file)
            self.myFixApplication = rofexEngine(self.usrId, self.pswd, self.targetCompID, self.tickers)
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

    suscribeTuple = ['RFX20Dic20', 'DODic20']

    fixMain = main(args.file_name, 'pjseoane232', 'AiZkiC5#', 'ROFX', suscribeTuple)

    fixMain.initiator.start()
    fixMain.myFixApplication.run()
    # fixMain.myFixApplication.printAllSecurities()
    fixMain.initiator.stop()
