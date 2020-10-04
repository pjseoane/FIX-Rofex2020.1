#!/usr/bin/env python
# coding: utf-8


import quickfix as fix
import quickfix50sp2 as fix50
import logging
from RofexEngine.RofexMsgClass import rofexMsg

from RofexEngine.FixMsgClass import FixMsg

logfix = logging.getLogger(__name__)
from Logger.logger import setup_logger2

# from Logger.logger import setup_logger
setup_logger2('FIX', 'Logs/message.log', logging.DEBUG, logging.DEBUG)  # ,logging.DEBUG,logging.DEBUG)

# setup_logger('FIX', 'Logs/message.log')


__SOH__ = chr(1)


class rofexEngine(fix.Application):
    def __init__(self, usr, pswd):
        super().__init__()
        self.sessionID = None
        self.session_off = True
        self.contractList = None
        self.secStatus = "secStatus"
        # self.ListaContratos="ListaContratos"

        self.usrId = usr
        self.password = pswd
        # self.onMessage2 = FixMsg()

    def formatMsg(self, message):
        return message.toString().replace(__SOH__, "|")

    def onCreate(self, sessionID):
        # onCreate is called when quickfix creates a new session. A session comes into and remains in existence for
        # the life of the application. Sessions exist whether or not a counter party is connected to it. As soon as a
        # session is created, you can begin sending messages to it. If no one is logged on, the messages will be sent
        # at the time a connection is established with the counterparty.

        self.sessionID = sessionID
        logfix.warning("onCreate session OK, sessionID >> (%s)" % self.sessionID)

    def onLogon(self, sessionID):
        # onLogon notifies you when a valid logon has been established with a counter party. This is called when a
        # connection has been established and the FIX logon process has completed with both parties exchanging valid
        # logon messages.
        self.session_off = False

        logfix.critical("Logged OK, sessionID >> (%s)" % self.sessionID)

    def onLogout(self, sessionID):
        # onLogout notifies you when an FIX session is no longer online. This could happen during a normal logout
        # exchange or because of a forced termination or a loss of network connection.

        self.session_off = True
        logfix.critical("onLogout OK, bye Rofex >> (%s)" % self.sessionID)

    def toAdmin(self, message, sessionID):
        # toAdmin provides you with a peek at the administrative messages that are being sent from your FIX engine
        # to the counter party. This is normally not useful for an application however it is provided for any logging
        # you may wish to do. Notice that the FIX::Message is not const.
        # This allows you to add fields to an adminstrative message before it is sent out.
        msg = self.formatMsg(message)
        #self.onMessage(message, 'toAdmin')

        if self.getTag35(message) == fix.MsgType_Logon:  # 'A':
            message.getHeader().setField(553, self.usrId)
            message.getHeader().setField(554, self.password)
            # message.getHeader().setField(336, '1')

            logfix.warning("toAdmin ->Logon>> (%s)" % msg)

        elif self.getTag35(message) == "3":
            logfix.warning("toAdmin ->Logon Rejected>> (%s)" % msg)

        elif self.getTag35(message) == "0":

            logfix.warning("toAdmin->heartbeat>> (%s)" % msg)

        else:
            logfix.warning("toAdmin-> sin detectar>> (%s)" % msg)

    def fromAdmin(self, message, sessionID):
        # fromAdmin notifies you when an administrative message is sent from a counterparty to your FIX engine. This
        # can be usefull for doing extra validation on logon messages like validating passwords. Throwing a
        # RejectLogon exception will disconnect the counterparty.

        msg = self.formatMsg(message)

        if self.getTag35(message) == "0":

            logfix.warning("heartbeat <-fromAdmin>> (%s)" % msg)

        elif self.getTag35(message) == "A":
            logfix.warning("fromAdmin <- Log OK (%s)" % msg)

        else:
            logfix.warning("Received from adm>> ??? (%s)" % msg)

    def toApp(self, message, sessionID):
        # toApp is a callback for application messages that are being sent to a counterparty.
        # If you throw a DoNotSend exception in this function, the application will not send the message.
        # This is mostly useful if the application has been asked to resend a message such as an order that is no longer relevant for the current market.
        # Messages that are being resent are marked with the PossDupFlag in the header set to true;
        # If a DoNotSend exception is thrown and the flag is set to true, a sequence reset will be sent in place of the message.
        # If it is set to false, the message will simply not be sent. Notice that the FIX::Message is not const.
        # This allows you to add fields to an application message before it is sent out.
        msg = self.formatMsg(message)

        logfix.warning("msg --> toApp >> (%s)" % msg)

    def fromApp(self, message, sessionID):
        # fromApp receives application level request.
        # If your application is a sell-side OMS, this is where you will get your new order requests.
        # If you were a buy side, you would get your execution reports here.
        # If a FieldNotFound exception is thrown,
        # the counterparty will receive a reject indicating a conditionally required field is missing.
        # The Message class will throw this exception when trying to retrieve a missing field, so you will rarely need the throw this explicitly.
        # You can also throw an UnsupportedMessageType exception.
        # This will result in the counterparty getting a reject informing them your application cannot process those types of messages.
        # An IncorrectTagValue can also be thrown if a field contains a value you do not support.

        # ACA OCURRE LA MAGIA DE LO MENSAJES QUE ENTRAN
        msg = self.formatMsg(message)

        # self.onMessage(message)
        logfix.warning("Response <-- fromApp >> (%s) " % msg)

    """
    def onMessage(self, message, function):

        msg = self.formatMsg(message)
        

        if self.getTag35(message) == fix.MsgType_Logon:  # 'A':
            message.getHeader().setField(553, self.usrId)
            message.getHeader().setField(554, self.password)
            # message.getHeader().setField(336, '1')

            logfix.warning(function+",->Logon>> (%s)" % msg)

        elif self.getTag35(message) == "3":
            logfix.warning(function+", Logon Rejected>> (%s)" % msg)

        elif self.getTag35(message) == "0":

            logfix.info("toAdmin->heartbeat>> (%s)" % msg)

        else:
            logfix.warning("toAdmin-> sin detectar>> (%s)" % msg)

    """

    def run(self):

        msgToRofex = rofexMsg(self.usrId)

        while 1:
            # time.sleep(2)
            action = self.queryAction()
            if action == '1':
                # self.goRobot()
                print(action)
                msg = msgToRofex.suscribeMD("RFX20Dic20")
                # msg = rofexMsg(self.usrId).suscribeMD("RFX20Sep20")
                fix.Session.sendToTarget(msg)

            elif action == '2':
                print(action)
                msg = msgToRofex.secList()
                fix.Session.sendToTarget(msg)

            elif action == '3':
                msg = msgToRofex.secList2()
                fix.Session.sendToTarget(msg)
                # self.queryReplaceOrder()
                print(action)

            elif action == '4':
                # self.queryMarketDataRequest()
                print(action)

            elif action == '5':
                print(action)
                break

            # elif action == '6':
            #     print( self.sessionID.getSenderCompID() )

    def queryAction(self):
        print("1) Suscribir MD\n2) SecList\n3) SecList2\n4) Market data test\n5) Quit")
        action = input("Action: ")
        return action

    def goRobot(self):
        # Overridable Method

        logfix.info("goRobot: >> (%s)" % self.sessionID)
        self.session_off = False

        msg = rofexMsg(self.usrId).suscribeMD("RFX20Sep20")
        fix.Session.sendToTarget(msg)

    def getHeaderValue(self, message, field):
        key = field
        message.getHeader().getField(key)
        return key.getValue()

    def getTag35(self, message):
        return message.getHeader().getField(35)
