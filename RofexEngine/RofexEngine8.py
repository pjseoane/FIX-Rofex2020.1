#!/usr/bin/env python
# coding: utf-8

import sys
import quickfix as fix
import quickfix50sp2 as fix50
import logging
from Logger.logger import setup_logger2
from Logger.logger import setup_logger
#from RofexEngine.RofexMsgClass import rofexMsg

sys.path.insert(0, '.\FIX\model')

setup_logger('FIX', 'Logs/message.log')
logfix = logging.getLogger('FIX')

#logfix = logging.getLogger(__name__)
#setup_logger2(logfix , 'Logs/message.log', logging.DEBUG, logging.DEBUG) #,logging.DEBUG,logging.DEBUG)
#setup_logger2(__name__ , 'Logs/message.log', logging.DEBUG, logging.DEBUG) #,logging.DEBUG,logging.DEBUG)

__SOH__ = chr(1)


class rofexEngine(fix.Application):
    def __init__(self,usr,pswd):
        super().__init__()
        self.sessionID = None
        self.session_off = True
        self.contractList=None
        self.secStatus = "secStatus"
        #self.ListaContratos="ListaContratos"

        self.senderCompID = usr
        self.password = pswd


    def formatMsg(self, message):
        return message.toString().replace(__SOH__, "|")

    def onCreate(self, session):
        # onCreate is called when quickfix creates a new session.
        # A session comes into and remains in existence for the life of the application.
        # Sessions exist whether or not a counter party is connected to it.
        # As soon as a session is created, you can begin sending messages to it.
        # If no one is logged on, the messages will be sent at the time a connection is established with the counterparty.

        targetCompID = session.getTargetCompID().getValue()
        try:
            self.sessions[targetCompID] = {}
        except AttributeError:
            self.lastOrderID            = self.account + '-00000000'
            self.orderID                = 0
            self.sessions               = {}
            self.orders                 = {}
            self.sessions[targetCompID] = {}

            self.tradeReports           = {}

        self.sessions[targetCompID]['session']   = session
        self.sessions[targetCompID]['connected'] = False
        self.sessions[targetCompID]['exchID']    = 0
        self.sessions[targetCompID]['execID']    = 0

        logfix.info("onCreate, sessionID >> (%s)" %self.sessions[targetCompID]['session'])

        #logfix.warning("onCreate session OK, sessionID >> (%s)" %self.sessionID)


    def onLogon(self, session):
        # onLogon notifies you when a valid logon has been established with a counter party.
        # This is called when a connection has been established and the FIX logon process has completed with both parties exchanging valid logon messages.
        # logger.info(
        #     f'onLogon sessionID: [{sessionID.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')
        logfix.critical("Logged OK, sessionID >> (%s)" %self.sessionID)
        targetCompID = session.getTargetCompID().getValue()
        self.sessions[targetCompID]['connected'] = True

        logfix.info("Client (%s) has logged in >>" % targetCompID)

    def onLogout(self, session):
        # onLogout notifies you when an FIX session is no longer online.
        # This could happen during a normal logout exchange or because of a forced termination or a loss of network connection.
        # logger.info(
        #     f'onLogout sessionID: [{sessionID.toString()}], main: [{threading.main_thread().ident}], current[{threading.current_thread().ident}]')
        #self.session_off = True
        #logfix.critical("onLogout OK, bye Rofex >> (%s)" % self.sessionID)

        targetCompID = session.getTargetCompID().getValue()
        self.sessions[targetCompID]['connected'] = False

        logfix.info("Client (%s) has logged out >>" % targetCompID)

    def toAdmin(self, message, session):
        # toAdmin provides you with a peek at the administrative messages that are being sent from your FIX engine
        # to the counter party. This is normally not useful for an application however it is provided for any logging
        # you may wish to do. Notice that the FIX::Message is not const.
        # This allows you to add fields to an adminstrative message before it is sent out.

        msg = self.formatMsg(message)
        logfix.info("S toAdmin>> (%s)" % msg)

        if self.getHeaderValue(message, fix.MsgType()) == fix.MsgType_Logon:
            message.getHeader().setField(553, self.senderCompID)
            message.getHeader().setField(554, self.password)
            msg = self.formatMsg(message)
            logfix.info("S Logon>> (%s)" % msg)

        elif message.getHeader().getField(35) == "0":
            msg = self.formatMsg(message)
            logfix.info("Send heartbeat>> (%s)" % msg)


    def fromAdmin(self, message, session):
        # fromAdmin notifies you when an administrative message is sent from a counterparty to your FIX engine. This can be usefull for doing extra validation on logon messages like validating passwords.
        # Throwing a RejectLogon exception will disconnect the counterparty.

        msg = self.formatMsg(message)

        if message.getHeader().getField(35) == "0":

            logfix.info("fromAdmin, Received heartbeat>> (%s)" % msg)
        else:

            #msg=self.formatMsg(message)
            logfix.warning("Received from adm>> (%s)" % msg)


    def toApp(self, message, session):
        # toApp is a callback for application messages that are being sent to a counterparty.
        # If you throw a DoNotSend exception in this function, the application will not send the message.
        # This is mostly useful if the application has been asked to resend a message such as an order that is no longer relevant for the current market.
        # Messages that are being resent are marked with the PossDupFlag in the header set to true;
        # If a DoNotSend exception is thrown and the flag is set to true, a sequence reset will be sent in place of the message.
        # If it is set to false, the message will simply not be sent. Notice that the FIX::Message is not const.
        # This allows you to add fields to an application message before it is sent out.
        msg = self.formatMsg(message)

        logfix.critical("Send toApp>> (%s)" % msg)

    def fromApp(self, message, session):
        # fromApp receives application level request.
        # If your application is a sell-side OMS, this is where you will get your new order requests.
        # If you were a buy side, you would get your execution reports here.
        # If a FieldNotFound exception is thrown,
        # the counterparty will receive a reject indicating a conditionally required field is missing.
        # The Message class will throw this exception when trying to retrieve a missing field, so you will rarely need the throw this explicitly.
        # You can also throw an UnsupportedMessageType exception.
        # This will result in the counterparty getting a reject informing them your application cannot process those types of messages.
        # An IncorrectTagValue can also be thrown if a field contains a value you do not support.
        msg = self.formatMsg(message)
        logfix.critical("Send toApp>> (%s)" % msg)


    def buildMsgHeader(self, msgType):
        """
        Message Header Builder
        """
        self.msg=msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.BeginString(fix.BeginString_FIXT11))
        header.setField(fix.MsgType(msgType))
        header.setField(fix.SenderCompID(self.senderCompID))
        header.setField(fix.TargetCompID(self.targetCompID))
        return self.msg


