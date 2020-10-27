#!/usr/bin/env python
# coding: utf-8

import quickfix as fix
import quickfix50sp2 as fix50
import logging

from RofexEngine.onMessage import onMessage
from Algos.algosClass import algos

logfix = logging.getLogger('FIX')  # 'FIX'
from Logger.logger import setup_logger2

setup_logger2('FIX', 'Logs/message.log', logging.CRITICAL, logging.DEBUG)  # ,logging.DEBUG,logging.DEBUG)

__SOH__ = chr(1)


def formatMsg(message):
    return message.toString().replace(__SOH__, "|")


class rofexEngine(fix.Application):

    def __init__(self, usr, pswd, targetCompId, tickers, entries):
        super().__init__()
        self.sessionID = None
        self.session_off = True
        # self.contractList = None
        self.secStatus = "secStatus"

        self.usrID = usr
        self.password = pswd
        self.targetCompID = targetCompId
        self.tickers = tickers
        self.entries = entries

        self.allSecurities = {}
        self.actualMarket = {}
        self.lastMsg = None
        self.previousMsg=None
        self.algoTEST = None
        # self.algoTEST = algos(self.actualMarket, tickers)  # crea el objeto Algos con el diccionario de datos de las cotiz actuales

        self.tag35 = None
        # print("rofexEngineee")

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
        self.sessionID=sessionID
        logfix.critical("Logged OK, sessionID >> (%s)" % self.sessionID)

        self.getSecuritiesList()

        self.suscribeMD3()

        logfix.critical("onLogon, securitiesList Requested..., sessionID >> (%s)" % self.sessionID)
        logfix.critical("onLogon, suscribeMD3() Requested..., sessionID >> (%s)" % self.sessionID)

    def onLogout(self, sessionID):
        # onLogout notifies you when an FIX session is no longer online. This could happen during a normal logout
        # exchange or because of a forced termination or a loss of network connection.
        self.session_off = True
        self.sessionID=sessionID
        logfix.critical("onLogout OK, bye Rofex >> (%s)" % self.sessionID)

    def toAdmin(self, message, sessionID):
        # toAdmin provides you with a peek at the administrative messages that are being sent from your FIX engine
        # to the counter party. This is normally not useful for an application however it is provided for any logging
        # you may wish to do. Notice that the FIX::Message is not const.
        # This allows you to add fields to an adminstrative message before it is sent out.
        msg = formatMsg(message)
        #self.sessionID=sessionID
        # tag35 = self.getTag35(message)
        tag35 = onMessage(message).getTag35()

        if tag35 == fix.MsgType_Logon:  # 'A':
            message.getHeader().setField(553, self.usrID)
            message.getHeader().setField(554, self.password)
            logfix.warning("toAdmin ->Logon>> (%s)" % msg)

        elif tag35 == '3':
            logfix.critical("toAdmin ->Logon Rejected>> (%s)" % msg)

        elif tag35 == '5':
            logfix.warning("Log OUT -> toAdmin>> (%s)" % msg)

        elif tag35 == '0':
            logfix.info("->heartbeat>> (%s)" % msg)

        else:
            logfix.warning("toAdmin-> sin detectar>> (%s)" % msg)

    def fromAdmin(self, message, sessionID):
        # fromAdmin notifies you when an administrative message is sent from a counterparty to your FIX engine. This
        # can be usefull for doing extra validation on logon messages like validating passwords. Throwing a
        # RejectLogon exception will disconnect the counterparty.
        msg = formatMsg(message)
        self.sessionID=sessionID
        # tag35 = self.getTag35(message)
        tag35 = onMessage(message).getTag35()

        if tag35 == '0':  # Heartbeat
            logfix.info("<-heartbeat>> (%s)" % msg)

        elif tag35 == 'A':
            logfix.warning("Log OK <- fromAdmin (%s)" % msg)

        elif tag35 == '5':
            logfix.warning("Log OUT <- fromAdmin (%s)" % msg)
            self.session_off = True
        else:
            logfix.warning("fromAdmin-> (%s)" % msg)

    def toApp(self, message, sessionID):
        # toApp is a callback for application messages that are being sent to a counterparty. If you throw a
        # DoNotSend exception in this function, the application will not send the message. This is mostly useful if
        # the application has been asked to resend a message such as an order that is no longer relevant for the
        # current market. Messages that are being resent are marked with the PossDupFlag in the header set to true;
        # If a DoNotSend exception is thrown and the flag is set to true, a sequence reset will be sent in place of
        # the message. If it is set to false, the message will simply not be sent. Notice that the FIX::Message is
        # not const. This allows you to add fields to an application message before it is sent out.
        msg = formatMsg(message)
        # tag35 = self.getTag35(message)
        tag35 = onMessage(message).getTag35()

        if tag35 == 'j':  # Business Message Reject
            logfix.warning("toApp -> Reject >> (%s)" % msg)
        else:
            logfix.warning("toApp -> >> (%s)" % msg)

    def fromApp(self, message, sessionID):
        # fromApp receives application level request. If your application is a sell-side OMS, this is where you will
        # get your new order requests. If you were a buy side, you would get your execution reports here. If a
        # FieldNotFound exception is thrown, the counterparty will receive a reject indicating a conditionally
        # required field is missing. The Message class will throw this exception when trying to retrieve a missing
        # field, so you will rarely need the throw this explicitly. You can also throw an UnsupportedMessageType
        # exception. This will result in the counterparty getting a reject informing them your application cannot
        # process those types of messages. An IncorrectTagValue can also be thrown if a field contains a value you do
        # not support.
        # ACA SE PROCESAN LOS MENSAJES QUE ENTRAN
        msg = formatMsg(message)
        self.sessionID=sessionID
        # tag35 = self.getTag35(message)
        tag35 = onMessage(message).getTag35()

        if tag35 == 'B':  # News
            #logfix.warning("News <-- fromApp >> (%s) " % msg)
            pass
        elif tag35 == 'h':  # Trading Session Status
            logfix.info("Trading Session Status <-- fromApp >> (%s) " % msg)

        elif tag35 == 'y':  # Security List

            securities = onMessage(message).onMessage_SecurityList()
            keys = securities.keys()
            for k in keys:
                self.allSecurities[k] = securities

            logfix.info("Securities List: allSecurities{} <-- fromApp >> (%s) " % msg)
            # print(self.allSecurities)

        elif tag35 == 'W':  # MktData
            # print(self.getValue(message, fix.Symbol()))
            # print("mensaje W")
            logfix.warning("MD <-- fromApp >> (%s) " % msg)

            self.lastMsg = onMessage(message).onMessage_MarketDataSnapshotFullRefresh()
            #self.actualMarket[self.lastMsg['instrumentId']['symbol']] = self.lastMsg
            self.goRobot2()

        else:
            logfix.warning("Response <-- fromApp >> (%s) " % msg)

        ## Broadcast JSON to WebSocket

    def getSecuritiesList(self):
        msg = fix50.SecurityListRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.usrID))
        header.setField(fix.TargetCompID(self.targetCompID))
        msg.setField(fix.SecurityReqID('ListRequest1'))
        msg.setField(fix.SecurityListRequestType(4))

        fix.Session.sendToTarget(msg)

    def suscribeMD3(self):

        print("SUSCRIBE MD3***************************************************************************")

        msg = fix50.MarketDataRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.usrID))
        header.setField(fix.TargetCompID(self.targetCompID))
        # ---------------------
        msg.setField(fix.MDReqID("ListaMktData"))
        msg.setField(fix.SubscriptionRequestType('1'))
        msg.setField(fix.MarketDepth(1))
        msg.setField(fix.MDUpdateType(0))
        msg.setField(fix.AggregatedBook(True))

        # BlockMDReqGrp
        group = fix50.MarketDataRequest().NoMDEntryTypes()
        for field in self.entries:
            group.setField(fix.MDEntryType(str(field)))
            msg.addGroup(group)

        # Symbols
        norelatedsym = fix50.MarketDataRequest().NoRelatedSym()
        for ticker in self.tickers:
            norelatedsym.setField(fix.Symbol(ticker))
            logfix.warning("--> Suscribe Ticker >> (%s)" % ticker)
            msg.addGroup(norelatedsym)

        fix.Session.sendToTarget(msg)


    def testRequest(self):  # , message):
        """
        Test Request

        Message Type = '1'.
        The test request message forces a heartbeat from the opposing application. The test request message
        checks sequence numbers or verifies communication line status. The opposite application responds to
        the Test Request with a Heartbeat containing the TestReqID.
        """
        msg = self.buildMsgHeader("1")
        msg.setField(fix.TestReqID(str('TEST')))

        fix.Session.sendToTarget(msg)

    def buildMsgHeader(self, msgType):
        """
        Message Header Builder
        """
        msg = fix.Message()
        header = self.msg.getHeader()
        header.setField(fix.BeginString(fix.BeginString_FIXT11))
        header.setField(fix.MsgType(msgType))
        header.setField(fix.SenderCompID(self.usrID))
        header.setField(fix.TargetCompID(self.targetCompID))
        return msg

    """
    def run(self):

    """

    def printAllSecurities(self):
        print(self.allSecurities)

    #def goRobot(self):
    #    pass
        #algoTEST = algos(self.actualMarket, self.tickers, self.lastMsg)  # crea el objeto Algos con el diccionario de datos de las cotiz actuales
        #algoTEST.goRobot()
        # print(self.lastMsg)
        # self.actualMarket[self.lastMsg['instrumentId']['symbol']] = self.lastMsg

    def getActualMktDict(self):
        return self.actualMarket

    def printActualMktDict(self):
        print(self.getActualMktDict())

    def printLastMsg(self):
        print(self.lastMsg)



