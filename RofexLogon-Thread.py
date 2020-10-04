
import sys
import argparse
import configparser
import signal
import quickfix as fix
import time
from threading import Thread
from RofexEngine.RofexEngine6 import rofexEngine


def signal_handler(sig, frame):
    fixMain.application.logout()
    fixMain.initiator.stop()
    sys.exit(0)


class RofexLogon(Thread):

    def __init__(self, config_file, usrId, pswd):
        Thread.__init__(self)

        self.config_file=config_file

        self.settings = fix.SessionSettings(config_file)
        self.myFixApplication = rofexEngine(usrId, pswd)

        self.storefactory = fix.FileStoreFactory(self.settings)
        self.logfactory = fix.FileLogFactory(self.settings)
        self.initiator = fix.SocketInitiator(self.myFixApplication, self.storefactory, self.settings, self.logfactory)

    def run(self):
        self.initiator.start()
        self.myFixApplication.run()  #--> ver esto
        self.initiator.stop()

        sys.exit(0)
        return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()

    fixMain = RofexLogon(args.file_name, 'pjseoane232', 'AiZkiC5#')
    #fixMain=RofexLogon('Initiator\configuration\primaryInitiator.cfg','pjseoane232','AiZkiC5#')
    # Handler of Ctrl+C Event
    signal.signal(signal.SIGINT, signal_handler)

    fixMain.daemon=True
    fixMain.start()


    while 1:
        time.sleep(1)

    fixMain.application.logout()
    fixMain.initiator.stop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
