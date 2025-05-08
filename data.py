from values.get_ticker_info import get_ticker_info

def getInfo(tickerName):
    ticker = get_ticker_info(tickerName)

    VPA = ticker["vpa"]
    LPA = ticker["lpa"]
    DY = ticker["dy"]
    PRICE = ticker["cotação"]
    BAZIN = (PRICE * DY) / 0.07
    BAZIN_MARGIN = ((BAZIN - PRICE) / BAZIN)
    GRAHAM = (LPA * VPA * 22.5) ** 0.5
    GRAHAM_MARGIN = ((GRAHAM - PRICE) / GRAHAM)

    # print(LPA, VPA, GRAHAM, GRAHAM_MARGIN)

    return [str(tickerName).upper(), PRICE, DY, VPA, LPA, BAZIN, GRAHAM, BAZIN_MARGIN, GRAHAM_MARGIN]