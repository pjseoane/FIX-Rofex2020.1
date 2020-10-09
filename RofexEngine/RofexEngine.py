#!/usr/bin/env python
# coding: utf-8


import quickfix as fix
import quickfix50sp2 as fix50
import logging
import texttable
from RofexEngine import bots as bt

logfix = logging.getLogger('FIX')  # 'FIX'
from Logger.logger import setup_logger2

# from Logger.logger import setup_logger
setup_logger2('FIX', 'Logs/message.log', logging.CRITICAL, logging.DEBUG)  # ,logging.DEBUG,logging.DEBUG)

# setup_logger('FIX', 'Logs/message.log')


__SOH__ = chr(1)


class rofexEngine(fix.Application):
    def __init__(self, usr, pswd, targetCompId, tickers):
        super().__init__()
        self.sessionID = None
        self.session_off = True
        self.contractList = None
        self.secStatus = "secStatus"

        self.usrID = usr
        self.password = pswd
        self.targetCompID = targetCompId
        self.tickers = tickers

        self.allSecurities = {}
        self.actualMarket = {}
        # self.msgToRofex = armarMensajes(self.usrID, self.targetCompID,self.allSecurities)
        self.tag35 = None
        # todo crear un diccionario que tenga el ultimo dato vio de un md

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

        self.secList()
        self.suscribeMD(self.tickers, ['0', '1', '2', '4', '5', '6', '7', '8', 'B', 'C'])

        logfix.critical("onLogon, securitiesList Requested..., sessionID >> (%s)" % self.sessionID)

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
        tag35 = self.getTag35(message)

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
        msg = self.formatMsg(message)
        tag35 = self.getTag35(message)

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
        msg = self.formatMsg(message)
        tag35 = self.getTag35(message)

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
        msg = self.formatMsg(message)
        tag35 = self.getTag35(message)

        if tag35 == 'B':  # News
            logfix.warning("News <-- fromApp >> (%s) " % msg)

        elif tag35 == 'h':  # Trading Session Status
            logfix.info("Trading Session Status <-- fromApp >> (%s) " % msg)

        elif tag35 == 'y':  # Security List
            self.allSecurities = self.onMessage_SecurityList(message)
            # self.allSecurities=msgProcessing.onMessage_SecurityListTEST(message, self.allSecurities)

            logfix.info("Securities List: allSecurities{} <-- fromApp >> (%s) " % msg)
            # print(self.allSecurities)

        elif tag35 == 'W':  # MktData
            # print(self.getValue(message, fix.Symbol()))
            logfix.warning("MD <-- fromApp >> (%s) " % msg)
            # self.onMessage_MarketDataSnapshotFullRefresh(message)
            self.onMessage_MarketDataSnapshotFullRefreshToDict(message)
            self.goRobot2()

        else:
            logfix.warning("Response <-- fromApp >> (%s) " % msg)

    ### msg parser
    def getTicker(self, msg):
        return msg['instrumentId']['symbol']

    def getBidPx(self, msg):
        if len((msg['marketData']['BI'])) > 0:
            return msg['marketData']['BI'][0]['price']
        else:
            return 0

    def getOfferPx(self, msg):
        if len((msg['marketData']['OF'])) > 0:
            return msg['marketData']['OF'][0]['price']
        else:
            return 0

    def getBidSize(self, msg):
        if len((msg['marketData']['BI'])) > 0:
            return msg['marketData']['BI'][0]['size']
        else:
            return 0

    def getOfferSize(self, msg):
        if len((msg['marketData']['OF'])) > 0:
            return msg['marketData']['OF'][0]['size']
        else:
            return 0

    def getBidDictActualMkt(self, ticker):
        return self.getBid(self.actualMarket[ticker])

    def getBidSizeDictActualMkt(self, ticker):
        return self.getBidSize(self.actualMarket[ticker])

    ###
    def onMessage_MarketDataSnapshotFullRefreshTable(self, message):
        """
        onMessage - Market Data - Snapshot / Full Refresh

        Message Type = 'W'.
        The Market Data Snapshot/Full Refresh messages are sent as the response to a Market Data Request
        message. The message refers to only one Market Data Request. It will contain the appropiate MDReqID
        tag value to correlate the request with the response.

        Fields:
            - (35) MsgType = W
            - (262) MDReqID = (string)
            - Block Instrument:
                - (55) Symbol = (string - Ticker)
            - Block MDfullGrp:
                - (268) NoMDEntries = (Int - number of Entries)
                    - (269) MDEntryType = 0 (Bid) / 1 (Offer) / 2 (Trade) / 4 (Opening price) / 5 (Closing Price) / 6 (Settlement Price) /
                                            7 (Trading Session High Price) / 8 (Trading Session Low Price) / B (Trade Volume) / C (Open Interest) /
                                            x (Nominal Volume) / w (Cash Volume)
                    - (270) MDEntryPx = (float - Conditional field when MDEntryType is 0-1-2-4-5-6-7-8-w)
                    - (271) MDEntrySize = (int - Conditional field when MDEntryType is 0-1-2-B-C-x)
                    - (290) MDEntryPositionNo = (int)
        """

        # msg = message.toString().replace(__SOH__, "|")
        # logfix.info("onMessage, R app (%s)" % msg)

        data = {}

        ## Number of entries following (Bid, Offer, etc)
        noMDEntries = self.getValue(message, fix.NoMDEntries())

        symbol = self.getValue(message, fix.Symbol())

        ## Market ID (ROFX, BYMA)
        marketId = self.getValue(message, fix.SecurityExchange())

        instrumentId = {"symbol": symbol, "marketId": marketId}
        data["instrumentId"] = instrumentId
        data["marketData"] = {"BI": [], "OF": []}

        group = fix50.MarketDataSnapshotFullRefresh().NoMDEntries()

        MDEntryType = fix.MDEntryType()  # Identifies the type of entry (Bid, Offer, etc)
        MDEntryPx = fix.MDEntryPx()
        MDEntrySize = fix.MDEntrySize()
        MDEntryPositionNo = fix.MDEntryPositionNo()  # Display position of a bid or offer, numbered from most competitive to least competitive

        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.BORDER | texttable.Texttable.HEADER)
        table.header(['Ticker', 'Tipo', 'Precio', 'Size', 'Posicion'])
        table.set_cols_width([12, 20, 8, 8, 8])
        table.set_cols_align(['c', 'c', 'c', 'c', 'c'])

        for entry in range(1, int(noMDEntries) + 1):
            try:

                md = {}
                price, size, position = None, None, None

                message.getGroup(entry, group)
                entry_type = group.getField(MDEntryType).getString()

                if entry_type in list('01245678w'):
                    price = group.getField(MDEntryPx).getString()
                    md['price'] = float(price)
                if entry_type in list('012BCx'):
                    size = group.getField(MDEntrySize).getString()
                    md['size'] = int(size)
                if entry_type in list('01'):
                    position = group.getField(MDEntryPositionNo).getString()
                    md['position'] = int(position)

                if entry_type == '0':
                    data["marketData"]["BI"].append(md)
                    tipo = 'BID'
                elif entry_type == '1':
                    data["marketData"]["OF"].append(md)
                    tipo = 'OFFER'
                elif entry_type == 'B':
                    data["marketData"]["TV"] = md
                    tipo = 'TRADE VOLUME'
                else:
                    tipo = entry_type

                table.add_row([symbol, tipo, price, size, position])
            except:
                pass

        print(table.draw())

        ## Broadcast JSON to WebSocket

    def onMessage_MarketDataSnapshotFullRefreshToDict(self, message):
        #cada vez que entra un mensaje se procesa y se carga en el dict
        mDict = (self.onMessage_MarketDataSnapshotFullRefresh(message))
        self.actualMarket[self.getTicker(mDict)] = mDict
        #print(mDict)



    def onMessage_MarketDataSnapshotFullRefresh(self, message):
        """
        onMessage - Market Data - Snapshot / Full Refresh

        Message Type = 'W'.
        The Market Data Snapshot/Full Refresh messages are sent as the response to a Market Data Request
        message. The message refers to only one Market Data Request. It will contain the appropiate MDReqID
        tag value to correlate the request with the response.

        Fields:
            - (35) MsgType = W
            - (262) MDReqID = (string)
            - Block Instrument:
                - (55) Symbol = (string - Ticker)
            - Block MDfullGrp:
                - (268) NoMDEntries = (Int - number of Entries)
                    - (269) MDEntryType = 0 (Bid) / 1 (Offer) / 2 (Trade) / 4 (Opening price) / 5 (Closing Price) / 6 (Settlement Price) /
                                            7 (Trading Session High Price) / 8 (Trading Session Low Price) / B (Trade Volume) / C (Open Interest) /
                                            x (Nominal Volume) / w (Cash Volume)
                    - (270) MDEntryPx = (float - Conditional field when MDEntryType is 0-1-2-4-5-6-7-8-w)
                    - (271) MDEntrySize = (int - Conditional field when MDEntryType is 0-1-2-B-C-x)
                    - (290) MDEntryPositionNo = (int)
        """

        # msg = message.toString().replace(__SOH__, "|")
        # logfix.info("onMessage, R app (%s)" % msg)

        data = {}

        ## Number of entries following (Bid, Offer, etc)
        noMDEntries = self.getValue(message, fix.NoMDEntries())

        symbol = self.getValue(message, fix.Symbol())

        ## Market ID (ROFX, BYMA)
        marketId = self.getValue(message, fix.SecurityExchange())

        instrumentId = {"symbol": symbol, "marketId": marketId}
        data["instrumentId"] = instrumentId
        data["marketData"] = {"BI": [], "OF": []}

        group = fix50.MarketDataSnapshotFullRefresh().NoMDEntries()

        MDEntryType = fix.MDEntryType()  # Identifies the type of entry (Bid, Offer, etc)
        MDEntryPx = fix.MDEntryPx()
        MDEntrySize = fix.MDEntrySize()
        MDEntryPositionNo = fix.MDEntryPositionNo()  # Display position of a bid or offer, numbered from most competitive to least competitive

        """
        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.BORDER|texttable.Texttable.HEADER)
        table.header(['Ticker','Tipo','Precio','Size','Posicion'])
        table.set_cols_width([12,20,8,8,8])
        table.set_cols_align(['c','c','c','c','c'])
        """

        for entry in range(1, int(noMDEntries) + 1):
            try:

                md = {}
                price, size, position = None, None, None

                message.getGroup(entry, group)
                entry_type = group.getField(MDEntryType).getString()

                if entry_type in list('01245678w'):
                    # campos que tienen precio
                    price = group.getField(MDEntryPx).getString()
                    md['price'] = float(price)

                if entry_type in list('012BCx'):
                    # campos que tienen size
                    size = group.getField(MDEntrySize).getString()
                    md['size'] = int(size)

                if entry_type in list('01'):
                    # campos que tienen orden
                    position = group.getField(MDEntryPositionNo).getString()
                    md['position'] = int(position)

                if entry_type == '0':
                    data["marketData"]["BI"].append(md)
                    tipo = 'BID'

                elif entry_type == '1':
                    data["marketData"]["OF"].append(md)
                    tipo = 'OFFER'

                elif entry_type == 'B':
                    data["marketData"]["TV"] = md
                    tipo = 'TRADE VOLUME'

                else:
                    tipo = entry_type

                # table.add_row([symbol, tipo, price, size, position])
            except:
                pass
        # Aca antes de devolver se puede mandar a una cola o algo
        return (data)

        ## Broadcast JSON to WebSocket
        # self.server_md.broadcast(str(data))

    def secList(self):
        msg = fix50.SecurityListRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.usrID))
        header.setField(fix.TargetCompID(self.targetCompID))
        msg.setField(fix.SecurityReqID('ListRequest1'))
        msg.setField(fix.SecurityListRequestType(4))

        fix.Session.sendToTarget(msg)

    def onMessage_SecurityList(self, message):
        group = fix50.SecurityList().NoRelatedSym()
        # print(group)

        mktSegmentID = self.getValue(message, fix.MarketSegmentID())
        noRelatedSym = self.getValue(message, fix.NoRelatedSym())

        mktSegment = {}
        tickerData = {}

        for tickers in range(1, noRelatedSym + 1):
            message.getGroup(tickers, group)
            aux = {'symbol': self.getValueGroup(group, fix.Symbol()),
                   'factor': self.getValueGroup(group, fix.Factor()),
                   'securityDesc': self.getValueGroup(group, fix.SecurityDesc()),
                   'cfiCode': self.getValueGroup(group, fix.CFICode()),
                   'contractMultiplier': self.getValueGroup(group, fix.ContractMultiplier()),
                   'minPriceIncrement': self.getValueGroup(group, fix.MinPriceIncrement()),
                   'tickSize': group.getField(5023),
                   'instrumentPricePrecision': group.getField(5514),
                   'instrumentSizePrecision': group.getField(7117),
                   'currency': self.getValueGroup(group, fix.Currency()),
                   'maxTradeVol': self.getValueGroup(group, fix.MaxTradeVol()),
                   'minTradeVol': self.getValueGroup(group, fix.MinTradeVol()),
                   'lowLimitPrice': self.getValueGroup(group, fix.LowLimitPrice()),
                   'highLimitPrice': self.getValueGroup(group, fix.HighLimitPrice())
                   }
            tickerData[self.getValueGroup(group, fix.Symbol())] = aux
        mktSegment[mktSegmentID] = tickerData

        # para unir todos los diccionarios en 1
        self.allSecurities[mktSegmentID] = mktSegment
        return self.allSecurities

    # Wrappers for get(Field)

    def getValue(self, message, field):
        key = field
        message.getField(key)
        return key.getValue()

    def getString(self, message, field):
        key = field
        message.getField(key)
        return key.getString()

    def getHeaderValue(self, message, field):
        key = field
        message.getHeader().getField(key)
        return key.getValue()

    def getFooterValue(self, message, field):
        key = field
        message.getTrailer().getField(key)
        return key.getValue()

    def getStringGroup(self, group, field):
        key = field
        group.getField(key)
        return key.getString()

    def getValueGroup(self, group, field):
        key = field
        group.getField(key)
        return key.getValue()

    def suscribeMD(self, tickers, entries):

        if len(tickers) == 0 or len(entries) == 0:
            return

        allowed_entries = ['0', '1', '2', '4', '5', '6', '7', '8', 'B', 'C']
        if not all(elem in allowed_entries for elem in entries):
            return

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
        for field in entries:
            group.setField(fix.MDEntryType(str(field)))
            msg.addGroup(group)

        # Symbols
        norelatedsym = fix50.MarketDataRequest().NoRelatedSym()
        for ticker in tickers:
            norelatedsym.setField(fix.Symbol(ticker))
            logfix.warning("--> Suscribe Ticker >> (%s)" % ticker)
            msg.addGroup(norelatedsym)
        fix.Session.sendToTarget(msg)

    def getTag35(self, message):
        return message.getHeader().getField(35)

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
        self.msg = msg = fix.Message()
        header = msg.getHeader()
        header.setField(fix.BeginString(fix.BeginString_FIXT11))
        header.setField(fix.MsgType(msgType))
        header.setField(fix.SenderCompID(self.usrID))
        header.setField(fix.TargetCompID(self.targetCompID))
        return self.msg

    def run(self):
        
        print("Paso x run")
        while 1:
            # time.sleep(2)
            action = self.queryAction()
            if action == '1':
                self.goRobot(self.tickers, ['0', '1', '2', '4', '5', '6', '7', '8', 'B', 'C'])
                print(action)
                # self.suscribeMD("RFX20Dic20")
                # msg = rofexMsg(self.usrId).suscribeMD("RFX20Sep20")


            elif action == '2':
                print(action)
                # msg = msgToRofex.secList()

            elif action == '3':
                print(self.allSecurities)
                print(action)
            elif action == '4':
                print(self.actualMarket)
                print(action)

            elif action == '5':
                print(action)
                break

            # elif action == '6':
            #     print( self.sessionID.getSenderCompID() )

    def queryAction(self):
        print("1) Suscribir MD\n2) SecList\n3) Print allSecuritiesList\n4) Actual Market\n5) Quit")
        action = input("Action: ")
        return action

    def printAllSecurities(self):
        print(self.allSecurities)

    #def goRobot(self, ticker, entries):
    def goRobot2(self):

        logfix.info("goRobot: >> (%s)" % self.sessionID)
        self.session_off = False

        #self.suscribeMD(ticker, entries)

        keys = self.actualMarket.keys()

        for k in keys:
            bidPrice = self.getBidPx(self.actualMarket[k])
            bidSize = self.getBidSize(self.actualMarket[k])
            offerPrice = self.getOfferPx(self.actualMarket[k])
            offerSize = self.getOfferSize(self.actualMarket[k])
            print(k + "-->" + str(bidPrice) + " / " + str(offerPrice) + "   " + str(bidSize) + " / " + str(offerSize))

            if len(self.actualMarket) == 2:
                bidRF = self.getBidPx(self.actualMarket['RFX20Dic20'])
                offRF = self.getOfferPx(self.actualMarket['RFX20Dic20'])
                bidDO = self.getBidPx(self.actualMarket['DODic20'])
                offDO = self.getOfferPx(self.actualMarket['DODic20'])

                if bidDO != 0 and offDO != 0:
                    # print("RFX20Dic20 en USD: " + str(bidRF / offDO)+ " / " + str(offRF/bidDO))
                    print(
                        "*RFX20Dic20 en USD: " + "{:.2f}".format(bidRF / offDO) + " / " + "{:.2f}".format(offRF / bidDO))


