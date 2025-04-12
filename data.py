import yfinance as yf

def getInfo(tickerName):
    ticker = yf.Ticker(str(tickerName)+".SA").info

    VPA = ticker["bookValue"]
    LPA = ticker["trailingEps"]
    DY = ticker["dividendYield"] / 100
    PRICE = ticker["currentPrice"]
    BAZIN = (PRICE * DY) / 0.07
    BAZIN_MARGIN = ((BAZIN - PRICE) / BAZIN)
    GRAHAM = (LPA * VPA * 22.5) ** 0.5
    GRAHAM_MARGIN = ((GRAHAM - PRICE) / GRAHAM)

    # print(LPA, VPA, GRAHAM, GRAHAM_MARGIN)

    return [str(tickerName).upper(), PRICE, DY, VPA, LPA, BAZIN, GRAHAM, BAZIN_MARGIN, GRAHAM_MARGIN]