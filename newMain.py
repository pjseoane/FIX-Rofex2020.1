import argparse
import quickfix as fix
from RofexEngine.RofexEngine6 import rofexEngine
#from application import Application # Application que vamos a extender
from threading import Thread
from getpass import getpass
import time
import signal
import sys


def signal_handler(sig, frame):
    fixMain.application.logout()
    fixMain.initiator.stop()
    sys.exit(0)


class main(Thread):
    def __init__(self, config_file, market, user, passwd, account):
        Thread.__init__(self)
        self.config_file = config_file
        self.market = market
        self.user = user
        self.passwd = passwd
        self.account = account

        self.settings = fix.SessionSettings(self.config_file)
        self.application = Application(self.market, self.user, self.passwd, self.account)
        self.storefactory = fix.FileStoreFactory(self.settings)
        self.logfactory = fix.FileLogFactory(self.settings)
        self.initiator = fix.SocketInitiator(self.application, self.storefactory,
                                             self.settings, self.logfactory)

    def run(self):
        self.initiator.start() # Inicia la conexión


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()
    market = input('Market (i.e. ROFX, BYMA): ')
    user = input('Username (SenderCompID): ')
    passwd = getpass(prompt="Password: ")
    account = input('Cuenta: ')
    fixMain = main(args.file_name, market, user, passwd, account)

    fixMain.daemon = True
    fixMain.start()

    # Handler of Ctrl+C Event
    signal.signal(signal.SIGINT, signal_handler)

    while 1:
        time.sleep(1)

    fixMain.application.logout()
    fixMain.initiator.stop()