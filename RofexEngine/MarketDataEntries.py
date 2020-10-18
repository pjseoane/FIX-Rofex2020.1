import enum


class MarketEntries(enum.Enum):
    Bid = '0'
    Offer = '1'
    Trade = '2'
    Index = '3'
    Open = '4'
    Close = '5'
    Settlement = '6'
    High = '7'
    Low = '8'
    Vol = 'x'
    CashVol = 'w'
    TradeVol = 'B'
    OpInt = 'C'
    AuctionPrice = 'Q'
    RefPrice = 'W'
