import quickfix as fix
import quickfix50sp2 as fix50
import texttable


class onMessage:
    def __init__(self, msg):
        self.message = msg

    def onMessage_SecurityList(self) -> dict:
        group = fix50.SecurityList().NoRelatedSym()
        # print(group)

        mktSegmentID = self.getValue(fix.MarketSegmentID())
        noRelatedSym = self.getValue(fix.NoRelatedSym())

        mktSegment = {}
        tickerData = {}
        #allSecurities = {}

        for tickers in range(1, noRelatedSym + 1):
            self.message.getGroup(tickers, group)
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
        #allSecurities[mktSegmentID] = mktSegment
        return mktSegment

    def onMessage_MarketDataSnapshotFullRefresh(self):
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

        data = {}

        ## Number of entries following (Bid, Offer, etc)
        noMDEntries = self.getValue(fix.NoMDEntries())

        symbol = self.getValue(fix.Symbol())

        ## Market ID (ROFX, BYMA)
        marketId = self.getValue(fix.SecurityExchange())

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

                self.message.getGroup(entry, group)
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
        return data

        ## Broadcast JSON to WebSocket
        # self.server_md.broadcast(str(data))

    def onMessage_MarketDataSnapshotFullRefreshTable(self):
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
        noMDEntries = self.getValue(fix.NoMDEntries())

        symbol = self.getValue(fix.Symbol())

        ## Market ID (ROFX, BYMA)
        marketId = self.getValue(fix.SecurityExchange())

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

                self.message.getGroup(entry, group)
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

    # Wrappers for get(Field)

    def getValue(self, field):
        key = field
        self.message.getField(key)
        return key.getValue()

    def getString(self, field):
        key = field
        self.message.getField(key)
        return key.getString()

    def getHeaderValue(self, field):
        key = field
        self.message.getHeader().getField(key)
        return key.getValue()

    def getFooterValue(self, field):
        key = field
        self.message.getTrailer().getField(key)
        return key.getValue()

    def getStringGroup(self, group, field):
        key = field
        group.getField(key)
        return key.getString()

    def getValueGroup(self, group, field):
        key = field
        group.getField(key)
        return key.getValue()
