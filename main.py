
import sys
import argparse
import configparser
import quickfix as fix
from RofexEngine.RofexEngine8 import rofexEngine


def mainLogon(config_file, usrId, pswd, targetCompID):

    try:
        settings = fix.SessionSettings(config_file)
        myFixApplication = rofexEngine(usrId, pswd, targetCompID)

        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(myFixApplication, storefactory, settings, logfactory)

        initiator.start()
        myFixApplication.run('DODic20')
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

    fixMain = mainLogon(args.file_name, 'pjseoane232', 'AiZkiC5#', 'ROFX')
    #main('Initiator\configuration\primaryInitiator.cfg')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
