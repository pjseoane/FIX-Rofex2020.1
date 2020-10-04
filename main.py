
import sys
import argparse
import configparser
import quickfix as fix
from RofexEngine.RofexEngine7 import rofexEngine


def rofexLogon(config_file, usrId, pswd):

    try:
        settings = fix.SessionSettings(config_file)
        myFixApplication = rofexEngine(usrId, pswd)

        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(myFixApplication, storefactory, settings, logfactory)

        initiator.start()
        myFixApplication.run()
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        initiator.stop()
        sys.exit()


if __name__ == '__main__':

    #rofexLogon('Initiator\configuration\primaryInitiator.cfg','pjseoane232','AiZkiC5#')


    parser = argparse.ArgumentParser(description='FIX Client Configuration')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()

    fixMain = rofexLogon(args.file_name, 'pjseoane232', 'AiZkiC5#')
    #main('Initiator\configuration\primaryInitiator.cfg')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
