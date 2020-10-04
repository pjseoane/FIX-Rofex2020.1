#!/usr/bin/env python
# coding: utf-8


import quickfix as fix
import quickfix50sp2 as fix50


tickers='RFX20Dic20'
    
class rofexMsg:
    def __init__(self,usrId):
        super().__init__()
        #self.messageType=messageType
        self.usrId=usrId
        
      
    def suscribeMD(self, ticker):
        self.ticker=ticker
  
        # pag 63
        msg = fix50.MarketDataRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.usrId))
        header.setField(fix.TargetCompID(targetComp))

       
        msg.setField(fix.MDReqID("ListaMktData"))
        msg.setField(fix.SubscriptionRequestType('1'))
        msg.setField(fix.MarketDepth(1))
        msg.setField(fix.MDUpdateType(0))
        msg.setField(fix.AggregatedBook(True))
        
        #BlockMDReqGrp
        group=fix50.MarketDataRequest().NoMDEntryTypes()
        group.setField(fix.MDEntryType('0'))
        msg.addGroup(group)
        group.setField(fix.MDEntryType('1'))
        msg.addGroup(group)

        #BlockInstrumentMDReqGrp
        msg.setField(fix.NoRelatedSym(1))
        
        #Block Instrument
        group = fix50.MarketDataRequest().NoRelatedSym()
        group.setField(fix.Symbol(ticker))
        group.setField(fix.SecurityExchange('ROFX')) #test
        msg.addGroup(group)

        #fix.Session.sendToTarget(msg)
        return msg
    
    



    def secList2(self):
        msg = fix50.SecurityListRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.usrId))
        header.setField(fix.TargetCompID(targetComp))
        msg.setField(fix.SecurityReqID('ListRequest2'))
        msg.setField(fix.SecurityListRequestType(1))
        #msg.setField(fix.MarketID('ROFX'))
        msg.setField(fix.CFICode("FXXXSX"))
        
        #group=fix50.SecurityListRequest()
        #group.setField(fix.CFICode("FXXXSX"))
        #msg.addGroup(group)
        #msg.setField(fix.SubscriptionRequestType(1))
        #msg.setField(fix.SubscriptionRequestType('1'))
        return msg
        
   

         
        #group
        #group = fix50.SecurityListRequest()
        #group.setField(fix.Symbol('RFX20Sep20'))
        #group.setField(fix.SecurityExchange('ROFX')) #test
        #group1=fix50.SecurityListRequest()
        #msg.setField(fix.CFICode("FXXXSX"))
        #msg.addGroup(group)
        
        #msg.setField(fix.)
        
        #fix.Session.sendToTarget(msg)
        
       
    def securityStatusRequest(self):
        # pag 80

        msg=self.buildMsgHeader("e")

        msg.setField(fix.SecurityStatusReqID("securityR"))
        msg.setField(fix.SubscriptionRequestType("2"))
        # Block Instrument

        # msg.setField(fix.NoRelatedSym(1))
        msg.setField(fix.Symbol(tickers))
        msg.setField((fix.SecurityExchange("ROFX")))

        #fix.Session.sendToTarget(msg)
        return msg


    def newOrder(self):

        # trade = fix.Message()
        # trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))  #
        # trade.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))  # 39=D
        # trade.setField(fix.ClOrdID(self.genExecID()))  # 11=Unique order
        #
        # trade.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))  # 21=3 (Manual order, best executiona)
        # trade.setField(fix.Symbol('SMBL'))  # 55=SMBL ?
        # trade.setField(fix.Side(fix.Side_BUY))  # 43=1 Buy
        # trade.setField(fix.OrdType(fix.OrdType_LIMIT))  # 40=2 Limit order
        # trade.setField(fix.OrderQty(100))  # 38=100
        # trade.setField(fix.Price(10))
        # trade.setField(fix.TransactTime(int(datetime.utcnow().strftime("%s"))))
        # print
        # trade.toString()
        # fix.Session.sendToTarget(trade, self.sessionID)
        pass


    def testRequest(self, message):

        msg=self.buildMsgHeader("1")
        msg.setField(fix.TestReqID(str(message)))

        fix.Session.sendToTarget(msg)


    def marketDataRequest(self, entries, symbols, subscription=fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES, depth=5):

        if len(entries) == 0 or len(symbols) == 0:
            return

        posibles_entries = [0,1,2,4,5,6,7,8,'B','C']

        if not all(elem in posibles_entries for elem in entries):
            return

        # ---- Header

        msg = fix50.MarketDataRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.senderCompID))
        header.setField(fix.TargetCompID(self.targetCompID))

        # ---- Body

        msg.setField(fix.MDReqID('ListaMD')) # Unique ID
        msg.setField(fix.SubscriptionRequestType(subscription))
        msg.setField(fix.MarketDepth(depth))
        msg.setField(fix.MDUpdateType(0))
        msg.setField(fix.AggregatedBook(True))

        # ---- MDEntries

        group=fix50.MarketDataRequest().NoMDEntryTypes()

        for entry in entries:
            group.setField(fix.MDEntryType(str(entry)))
            msg.addGroup(group)

        # ---- Symbols

        norelatedsym = fix50.MarketDataRequest().NoRelatedSym()

        for symbol in symbols:
            print(symbol)
            norelatedsym.setField(fix.Symbol(str(symbol)))
            msg.addGroup(norelatedsym)

        # -----------------------------------------

        fix.Session.sendToTarget(msg)


    def onMessage_MarketDataSnapshotFullRefresh(self, message, session):

        msg = message.toString().replace(__SOH__, "|")
        logfix.info("onMessage, R app (%s)" % msg)

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

        MDEntryType = fix.MDEntryType() # Identifies the type of entry (Bid, Offer, etc)
        MDEntryPx = fix.MDEntryPx()
        MDEntrySize = fix.MDEntrySize()
        MDEntryPositionNo = fix.MDEntryPositionNo() # Display position of a bid or offer, numbered from most competitive to least competitive

        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.BORDER|texttable.Texttable.HEADER)
        table.header(['Ticker','Tipo','Precio','Size','Posicion'])
        table.set_cols_width([12,20,8,8,8])
        table.set_cols_align(['c','c','c','c','c'])

        for entry in range(1,int(noMDEntries)+1):
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


    def newOrderSingle(self, symbol, side, quantity, price, orderType):

        clOrdId = self.getNextOrderID()
        details = {'clOrdId'  : clOrdId,
                   'symbol'   : symbol,
                   'side'     : side,
                   'quantity' : quantity,
                   'price'    : price,
                   'ordType'  : orderType
                   }

        # ---- Header

        msg = fix50.NewOrderSingle()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.senderCompID))
        header.setField(fix.TargetCompID(self.targetCompID))

        # ---- Body

        msg.setField(fix.Account(self.account))
        msg.setField(fix.ClOrdID(str(details['clOrdId'])))
        msg.setField(fix.OrderQty(details['quantity']))
        msg.setField(fix.OrdType(details['ordType']))
        msg.setField(fix.Price(details['price']))
        msg.setField(fix.Side(details['side']))
        msg.setField(fix.TransactTime())
        msg.setField(fix.Symbol(details['symbol']))

        fix.Session.sendToTarget(msg)


    def orderCancelRequest(self, orderId, side, quantity, symbol):

        clOrdId = self.getNextOrderID()
        details = {'clOrdId'  : clOrdId,
                   'symbol'   : symbol,
                   'side'     : side,
                   'quantity' : quantity ,
                   'orderId'  : orderId
                   }

        # ---- Header

        msg = fix50.OrderCancelRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.senderCompID))
        header.setField(fix.TargetCompID(self.targetCompID))

        # ---- Body

        msg.setField(fix.ClOrdID(str(details['clOrdId'])))
        msg.setField(fix.OrderID(str(details['orderId'])))
        msg.setField(fix.Side(details['side']))
        msg.setField(fix.TransactTime())
        msg.setField(fix.Account(self.account))
        msg.setField(fix.OrderQty(details['quantity']))
        msg.setField(fix.Symbol(details['symbol']))
        msg.setField(fix.SecurityExchange(self.targetCompID))

        fix.Session.sendToTarget(msg)


    def orderStatusRequest(self, orderId, symbol, side):

        details = {'symbol'         : symbol,
                   'side'           : side,
                   'orderId'        : orderId
                   }

        # ---- Header

        msg = fix50.OrderStatusRequest()
        header = msg.getHeader()
        header.setField(fix.SenderCompID(self.senderCompID))
        header.setField(fix.TargetCompID(self.targetCompID))

        # ---- Body

        msg.setField(fix.OrderID(str(details['orderId'])))
        msg.setField(fix.Symbol(details['symbol']))
        msg.setField(fix.Side(details['side']))

        fix.Session.sendToTarget(msg)


    def onMessage_ExecutionReport_New(self, message, session):

        clientOrderID = self.getValue(message, fix.ClOrdID())
        targetCompID  = session.getTargetCompID().getValue()
        senderCompID  = session.getSenderCompID().getValue()
        details       = {'targetCompId'     : targetCompID,
                         'clOrdId'          : clientOrderID,
                         'execId'           : self.getValue(message, fix.ExecID()),
                         'symbol'           : self.getValue(message, fix.Symbol()),
                         'side'             : self.getSide(self.getValue(message, fix.Side())),
                         'securityExchange' : self.getValue(message, fix.SecurityExchange()),
                         'transactTime'     : self.getString(message, fix.TransactTime()),
                         'ordStatus'        : self.getOrdStatus(self.getValue(message, fix.OrdStatus())),
                         'ordType'          : self.getOrdType(self.getValue(message, fix.OrdType())),
                         'price'            : self.getValue(message, fix.Price()),
                         'avgPx'            : self.getValue(message, fix.AvgPx()),
                         'lastPx'           : self.getValue(message, fix.LastPx()),
                         'orderQty'         : self.getValue(message, fix.OrderQty()),
                         'leavesQty'        : self.getValue(message, fix.LeavesQty()),
                         'cumQty'           : self.getValue(message, fix.CumQty()),
                         'lastQty'          : self.getValue(message, fix.LastQty()),
                         'text'             : self.getValue(message, fix.Text())
                         }

        orderID = self.getValue(message, fix.OrderID())

        data = {}
        data['type']  = 'or'
        data['senderCompID'] = senderCompID
        data['orderReport'] = {'accountId'    : {'id' : self.account},
                               'clOrdId'      : details['clOrdId'],
                               'cumQty'       : details['cumQty'],
                               'execId'       : details['execId'],
                               'instrumentId' : {'marketId' : details['securityExchange'], 'symbol' : details['symbol']},
                               'leavesQty'    : details['leavesQty'],
                               'ordType'      : details['ordType'],
                               'orderId'      : orderID,
                               'orderQty'     : details['orderQty'],
                               'price'        : details['price'],
                               'side'         : details['side'],
                               'status'       : details['ordStatus'],
                               'transactTime' : details['transactTime'],
                               'text'         : details['text']
                               }



        self.orders[orderID] = details
        self.sessions[targetCompID][clientOrderID] = orderID


    def onMessage_ExecutionReport_OrderCanceledResponse(self, message, session):

        clientOrderID = self.getValue(message, fix.ClOrdID())
        targetCompID  = session.getTargetCompID().getValue()
        senderCompID  = session.getSenderCompID().getValue()
        details       = {'targetCompId'     : targetCompID,
                         'clOrdId'          : clientOrderID,
                         'execId'           : self.getValue(message, fix.ExecID()),
                         'origClOrdId'      : self.getValue(message, fix.OrigClOrdID()),
                         'symbol'           : self.getValue(message, fix.Symbol()),
                         'side'             : self.getSide(self.getValue(message, fix.Side())),
                         'securityExchange' : self.getValue(message, fix.SecurityExchange()),
                         'transactTime'     : self.getString(message, fix.TransactTime()),
                         'ordStatus'        : self.getOrdStatus(self.getValue(message, fix.OrdStatus())),
                         'ordType'          : self.getOrdType(self.getValue(message, fix.OrdType())),
                         'price'            : self.getValue(message, fix.Price()),
                         'avgPx'            : self.getValue(message, fix.AvgPx()),
                         'lastPx'           : self.getValue(message, fix.LastPx()),
                         'orderQty'         : self.getValue(message, fix.OrderQty()),
                         'leavesQty'        : self.getValue(message, fix.LeavesQty()),
                         'cumQty'           : self.getValue(message, fix.CumQty()),
                         'lastQty'          : self.getValue(message, fix.LastQty()),
                         'text'             : self.getValue(message, fix.Text())
                         }

        orderID = self.getValue(message, fix.OrderID())

        data = {}
        data['type']  = 'or'
        data['senderCompID'] = senderCompID
        data['orderReport'] = {'accountId'    : {'id' : self.account},
                               'avgPx'        : details['avgPx'],
                               'clOrdId'      : details['clOrdId'],
                               'origClOrdId'  : details['origClOrdId'],
                               'cumQty'       : details['cumQty'],
                               'execId'       : details['execId'],
                               'lastPx'       : details['lastPx'],
                               'lastQty'      : details['lastQty'],
                               'instrumentId' : {'marketId' : details['securityExchange'], 'symbol' : details['symbol']},
                               'leavesQty'    : details['leavesQty'],
                               'ordType'      : details['ordType'],
                               'orderId'      : orderID,
                               'orderQty'     : details['orderQty'],
                               'price'        : details['price'],
                               'side'         : details['side'],
                               'status'       : details['ordStatus'],
                               'transactTime' : details['transactTime'],
                               'text'         : details['text']
                               }



        self.orders[orderID] = details
        self.sessions[targetCompID][clientOrderID] = orderID


    def onMessage_ExecutionReport_OrderStatusResponse(self, message, session):

        targetCompID  = session.getTargetCompID().getValue()
        senderCompID  = session.getSenderCompID().getValue()

        try:
            totNumReports = self.getValue(message, fix.TotNumReports())
            details       = {'targetCompId'     : targetCompID,
                             'totNumReports'    : totNumReports,
                             'massStatusReqId'  : self.getValue(message, fix.MassStatusReqID()),
                             'lastRptRequested' : self.getValue(message, fix.LastRptRequested()),
                             'avgPx'            : self.getValue(message, fix.AvgPx()),
                             'cumQty'           : self.getValue(message, fix.CumQty()),
                             'execId'           : self.getValue(message, fix.ExecID()),
                             'orderId'          : self.getValue(message, fix.OrderID()),
                             'ordStatus'        : self.getOrdStatus(self.getValue(message, fix.OrdStatus())),
                             'symbol'           : self.getValue(message, fix.Symbol()),
                             'side'             : self.getSide(self.getValue(message, fix.Side())),
                             'transactTime'     : self.getString(message, fix.TransactTime()),
                             'leavesQty'        : self.getValue(message, fix.LeavesQty()),
                             'text'             : self.getValue(message, fix.Text())
                             }

            data = {}
            data['type']  = 'os'
            data['senderCompID'] = senderCompID
            data['statusReport'] = details

            if totNumReports > 0:

                details_with_orders = {'account'        : self.getValue(message, fix.Account()),
                                       'clOrdId'        : self.getValue(message, fix.ClOrdID()),
                                       'lastPx'         : self.getValue(message, fix.LastPx()),
                                       'lastQty'        : self.getValue(message, fix.LastQty()),
                                       'orderQty'       : self.getValue(message, fix.OrderQty()),
                                       'ordType'        : self.getOrdType(self.getValue(message, fix.OrdType())),
                                       'price'          : self.getValue(message, fix.Price())
                                       }

                details.update(details_with_orders)
                data['statusReport'].update(details_with_orders)
        except:
            details       = {'targetCompId'     : targetCompID,
                             'account'          : self.getValue(message, fix.Account()),
                             'avgPx'            : self.getValue(message, fix.AvgPx()),
                             'clOrdId'          : self.getValue(message, fix.ClOrdID()),
                             'cumQty'           : self.getValue(message, fix.CumQty()),
                             'execId'           : self.getValue(message, fix.ExecID()),
                             'lastPx'           : self.getValue(message, fix.LastPx()),
                             'lastQty'          : self.getValue(message, fix.LastQty()),
                             'orderId'          : self.getValue(message, fix.OrderID()),
                             'orderQty'         : self.getValue(message, fix.OrderQty()),
                             'ordStatus'        : self.getOrdStatus(self.getValue(message, fix.OrdStatus())),
                             'ordType'          : self.getOrdType(self.getValue(message, fix.OrdType())),
                             'price'            : self.getValue(message, fix.Price()),
                             'symbol'           : self.getValue(message, fix.Symbol()),
                             'side'             : self.getSide(self.getValue(message, fix.Side())),
                             'transactTime'     : self.getString(message, fix.TransactTime()),
                             'leavesQty'        : self.getValue(message, fix.LeavesQty()),
                             'text'             : self.getValue(message, fix.Text()),
                             'securityExchange' : self.getValue(message, fix.SecurityExchange())
                             }

            data = {}
            data['type']  = 'os'
            data['senderCompID'] = senderCompID
            data['statusReport'] = details
