from values.get_ticker_info import get_ticker_info

def getInfo(tickerName):
    print("\n[{:s}] initiating data extraction...".format(tickerName))

    try:
        ticker = get_ticker_info(tickerName)

        VPA = ticker["vpa"]
        LPA = ticker["lpa"]
        DY = ticker["dy"]
        PRICE = ticker["cotação"]
        BAZIN = (PRICE * DY) / 0.07
        BAZIN_MARGIN = ((BAZIN - PRICE) / BAZIN)
        GRAHAM = (LPA * VPA * 22.5) ** 0.5
        GRAHAM_MARGIN = ((GRAHAM - PRICE) / GRAHAM)

        return [str(tickerName).upper(), PRICE, DY, VPA, LPA, BAZIN, GRAHAM, BAZIN_MARGIN, GRAHAM_MARGIN]

    except Exception as e:
        print("[{:s}] aborting data extraction - ".format(tickerName), end="")
        print(e)