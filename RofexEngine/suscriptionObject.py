class suscriptionObjet:
    def __init__(self, tickers, entries):
        self.__entries = entries
        self.__tickers = tickers
        # self.__entries = entries
        self.setEntries(entries)

    def getTickers(self) -> tuple:
        return self.__tickers

    def getEntries(self) -> tuple:
        return self.__entries

    def setTickers(self, tickers):
        self.__tickers = tickers

    def setEntries(self, entries):
        allowed_entries = ['0', '1', '2', '3','4', '5', '6', '7', '8', 'x','w','B', 'C','Q','W']
        entries2 = []
        for e in entries:
            entries2.append(e.value)

        if not all(elem in allowed_entries for elem in entries):
            self.__entries = allowed_entries
        else:
            pass

    entries = property(getEntries, setEntries)
