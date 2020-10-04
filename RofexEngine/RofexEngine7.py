#!/usr/bin/env python
# coding: utf-8


import quickfix as fix
import quickfix50sp2 as fix50
import logging
import texttable
from RofexEngine.RofexMsgClass import rofexMsg

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
        self.targetComp='ROFX'
        # self.onMessage2 = FixMsg()
        self.allSecurities={}

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
        logfix.critical("All Securities data Loaded..., sessionID >> (%s)" % self.sessionID)

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
            message.getHeader().setField(553, self.usrId)
            message.getHeader().setField(554, self.password)
            logfix.warning("toAdmin ->Logon>> (%s)" % msg)

        elif tag35 == "3":
            logfix.warning("toAdmin ->Logon Rejected>> (%s)" % msg)

        elif tag35 == "0":
            logfix.warning("->heartbeat>> (%s)" % msg)

        else:
            logfix.warning("toAdmin-> sin detectar>> (%s)" % msg)

    def fromAdmin(self, message, sessionID):
        # fromAdmin notifies you when an administrative message is sent from a counterparty to your FIX engine. This
        # can be usefull for doing extra validation on logon messages like validating passwords. Throwing a
        # RejectLogon exception will disconnect the counterparty.
        msg = self.formatMsg(message)
        tag35 = self.getTag35(message)

        if tag35 == '0':  # Heartbeat
            logfix.warning("<-heartbeat>> (%s)" % msg)

        elif tag35 == 'A':
            logfix.warning("fromAdmin <- Log OK (%s)" % msg)

        elif tag35 == '5':
            logfix.warning("fromAdmin <- Log OUT (%s)" % msg)
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
        # tag35=self.getTag35(message)

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
        # ACA SE PEOCESA LOS MENSAJES QUE ENTRAN
        msg = self.formatMsg(message)
        tag35 = self.getTag35(message)

        if tag35 == 'B':  # News
            logfix.warning("News <-- fromApp >> (%s) " % msg)

        elif tag35 == 'h':  # Trading Session Status
            logfix.warning("Trading Session Status <-- fromApp >> (%s) " % msg)

        elif tag35 == 'y':  # Security List
            self.onMessage_SecurityList(message)
            logfix.warning("Securities List <-- fromApp >> (%s) " % msg)
        else:
            logfix.warning("Response <-- fromApp >> (%s) " % msg)

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
                #msg = msgToRofex.secList()


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

    def getTag35(self, message):
        # key=tag
        return message.getHeader().getField(35)

    def secList(self):
        msg = fix50.SecurityListRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.usrId))
        header.setField(fix.TargetCompID(self.targetComp))
        msg.setField(fix.SecurityReqID('ListRequest1'))
        msg.setField(fix.SecurityListRequestType(4))
        #msg.setField(fix.MarketID('ROFX'))
        #msg.setField(fix.Symbol('RFX20Dic20'))
        #msg.setField(fix.MarketSegmentID('DDF'))
        fix.Session.sendToTarget(msg)

    def onMessage_SecurityList(self, message):
        group = fix50.SecurityList().NoRelatedSym()
        # print(group)

        mktSegmentID = self.getValue(message, fix.MarketSegmentID())
        noRelatedSym = self.getValue(message, fix.NoRelatedSym())
        #print("Mkt Segment ID " + mktSegmentID + " tickers " + str(noRelatedSym))
        logfix.warning("Mkt Segment, Tickers>>(%s) " % mktSegmentID+ str(noRelatedSym))
        #self.allData[mktSegmentID]=noRelatedSym
        #print(self.allData)

        mktSegment={}
        tickerData={}

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
            tickerData[self.getValueGroup(group, fix.Symbol())]=aux
        mktSegment[mktSegmentID]=tickerData
        #print(mktSegment)

        # para unir todos los diccionarios en 1
        self.allSecurities[mktSegmentID]=mktSegment
        #print(self.allData)



    def onMessage_SecurityList2(self, message):
        """
        onMessage - Security List

        Message Type = 'y'.
        The Security List message is used to return a list of securities that matches the criteria specified
        in a Security List Request.

        Fields:
            - (35) - MsgType = y
            - (320) - SecurityReqID = (string)
            - (322) - SecurityResponseID = (string)
            - (560) - SecurityRequestResult = (int)
            - (559) - SecurityListRequestType = 4 (All Securities)
            - (393) - TotNoRelatedSym = (int)
            - Block SecListGrp:
                - (146) - NoRelatedSym = (Int - number of repeating symbols specified)
                    - Block Instrument:
                        - (55) - Symbol = (string - Ticker)
                        - (107) - SecurityDesc = (string)
                        - (228) - Factor = (float)
                        - (461) - CFICode = (string)
                        - (231) - ContractMultiplier = (float)
                        - (200) - MaturityMonthYear = ('YYYYMM')
                        - (541) - MaturityDate = ('YYYYMMDD')
                        - (202) - StrikePrice = (float)
                        - (947) - StrikeCurrency = (string)
                        - (969) - MinPriceIncrement = (float)
                        - (5023) - TickSize = (int)
                        - (5514) - InstrumentPricePrecision = (int)
                        - (7117) - InstrumentSizePrecision = (int)
                    - (15) - Currency = (string)
                    - Block FinancingDetails:
                        - (917) - EndDate = (Date)
                    - Block UndInstrmtGrp:
                        - (711) - NoUnderlyings = (int)
                         - Block UnderlyingSymbol:
                             - (311) - UnderlyingSymbol = (string)
                    - Block SecurityTradingRules:
                        - Block BaseTradingRules:
                            - (1140) - MaxTradeVol = (float)
                            - (562) - MinTradeVol = (float)
                            - Block LotTypeRules:
                                - (1234) - NoLotTypeRules = (int)
                                    - (1093) - LotType = (char)
                                    - (1231) - MinLotSize = (int)
                                    - (5515) - MaxLotSize = (int)
                            - Block PriceLimits:
                                - (1148) - LowLimitPrice = (float)
                                - (1149) - HighLimitPrice = (float)
                        - Block TradingSessionRulesGrp:
                            - (1309) - NoTradingSessionRules = (int)
                                - (336) - TradingSessionID = (string)
                                - Block TradingSessionRules:
                                    - Block OrdTypeRules:
                                        - (1237) - NoOrdTypeRules = (int)
                                            - (40) - OrdType = (char)
                                    - Block TimeInForceRules:
                                        - (1239) - NoTimeInForceRules = (int)
                                            - (59) - TimeInForce = (char)
                                    - Block ExecInstRules:
                                        - (1232) - NoExecInstRules = (int)
                                            - (1308) - ExecInstValue = (char)
        """

        details = {'securityReqId': self.getValue(message, fix.SecurityReqID()),
                   'securityResponseId': self.getValue(message, fix.SecurityResponseID()),
                   'totNoRelatedSym': self.getValue(message, fix.TotNoRelatedSym()),
                   'securityListRequestType': self.getValue(message, fix.SecurityListRequestType()),
                   'securityRequestResult': self.getValue(message, fix.SecurityRequestResult()),
                   'marketSegmentId': self.getValue(message, fix.MarketSegmentID()),
                   'noRelatedSym': self.getValue(message, fix.NoRelatedSym())
                   }

        data = {}
        data['details'] = details
        data['tickers'] = []

        group = fix50.SecurityList().NoRelatedSym()

        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.BORDER | texttable.Texttable.HEADER)
        table.header(['Symbol', 'Min Price Increment', 'Tick Size', 'Price Precision', 'Size Precision', 'Currency',
                      'Underlying', 'Low Limit Price', 'High Limit Price'])
        table.set_cols_width([35, 15, 10, 10, 10, 10, 45, 10, 10])
        table.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])

        for relatedSym in range(1, details['noRelatedSym'] + 1):

            message.getGroup(relatedSym, group)

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
            try:
                aux['strikePrice'] = self.getValueGroup(group, fix.StrikePrice())
            except:
                pass
            try:
                aux['strikeCurrency'] = self.getValueGroup(group, fix.StrikeCurrency())
            except:
                pass
            try:
                aux['maturityMonthYear'] = self.getValueGroup(group, fix.MaturityMonthYear())
            except:
                pass
            try:
                aux['maturityDate'] = self.getValueGroup(group, fix.MaturityDate())
            except:
                pass

            ## Block UndInstrmtGrp
            groupUnderlyings = fix50.SecurityList().NoRelatedSym().NoUnderlyings()
            try:
                noUnderlyings = group.getField(711)
                for underlying in range(1, int(noUnderlyings) + 1):
                    group.getGroup(underlying, groupUnderlyings)
                    try:
                        aux['underlyingSymbol'] = self.getValueGroup(groupUnderlyings, fix.UnderlyingSymbol()).encode(
                            sys.getfilesystemencoding(), 'surrogateescape').decode('latin1', 'replace')
                    except:
                        pass
            except:
                pass

            ## Block LotTypeRules
            groupLotTypeRules = fix50.SecurityList().NoRelatedSym().NoLotTypeRules()
            try:
                noLotTypeRules = group.getField(1234)
                for typeRule in range(1, int(noLotTypeRules) + 1):
                    group.getGroup(typeRule, groupLotTypeRules)
                    try:
                        aux['lotType'] = self.getValueGroup(groupLotTypeRules, fix.LotType())
                        aux['minLotSize'] = self.getValueGroup(groupLotTypeRules, fix.MinLotSize())
                        aux['maxLotSize'] = groupLotTypeRules.getField(5515)
                    except:
                        pass
            except:
                pass

            ## Block TradingSessionRulesGrp
            groupTradingSessionRules = fix50.SecurityList().NoRelatedSym().NoTradingSessionRules()
            try:
                noTradingSessionRules = group.getField(1309)
                for sessionRule in range(1, int(noTradingSessionRules) + 1):
                    group.getGroup(sessionRule, groupTradingSessionRules)
                    try:
                        aux['tradingSessionId'] = self.getValueGroup(groupTradingSessionRules, fix.TradingSessionID())

                        ## Block TradingSessionRules

                        ### Block OrdTypeRules
                        groupOrdTypeRules = fix50.SecurityList().NoRelatedSym().NoTradingSessionRules().NoOrdTypeRules()
                        try:
                            noOrdTypeRules = groupTradingSessionRules.getField(1237)
                            aux['ordType'] = []
                            for typeRule in range(1, int(noOrdTypeRules) + 1):
                                groupTradingSessionRules.getGroup(typeRule, groupOrdTypeRules)
                                try:
                                    aux['ordType'].append(
                                        self.getOrdType(self.getValueGroup(groupOrdTypeRules, fix.OrdType())))
                                except:
                                    pass
                        except:
                            pass

                        ### Block TimeInForceRules
                        groupTimeInForceRules = fix50.SecurityList().NoRelatedSym().NoTradingSessionRules().NoTimeInForceRules()
                        try:
                            noTimeInForceRules = groupTradingSessionRules.getField(1239)
                            aux['timeInForce'] = []
                            for forceRule in range(1, int(noTimeInForceRules) + 1):
                                groupTradingSessionRules.getGroup(forceRule, groupTimeInForceRules)
                                try:
                                    aux['timeInForce'].append(self.getTimeInForce(
                                        self.getValueGroup(groupTimeInForceRules, fix.TimeInForce())))
                                except:
                                    pass
                        except:
                            pass

                        ### Block ExecInstRules
                        groupExecInstRules = fix50.SecurityList().NoRelatedSym().NoTradingSessionRules().NoExecInstRules()
                        try:
                            noExecInstRules = groupTradingSessionRules.getField(1232)
                            aux['execInstValue'] = []
                            for instRule in range(1, int(noExecInstRules) + 1):
                                groupTradingSessionRules.getGroup(instRule, groupExecInstRules)
                                try:
                                    aux['execInstValue'].append(self.getExecInstValue(
                                        self.getValueGroup(groupExecInstRules, fix.ExecInstValue())))
                                except:
                                    pass
                        except:
                            pass

                    except:
                        pass
            except:
                pass

            data['tickers'].append(aux)

            # table.add_row([aux['symbol'],aux['minPriceIncrement'],aux['tickSize'],aux['instrumentPricePrecision'],aux['instrumentSizePrecision'],aux['currency'],
            #         aux['underlyingSymbol'],aux['lowLimitPrice'],aux['highLimitPrice']])

        print(table.draw())

    """
    Wrappers for get(Field)
    """

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
