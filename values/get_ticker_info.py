from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from values.conversion import convert

def setupConnection(ticker):
    print("[{:s}] setting connection ...".format(ticker))

    DELAY = 10 # Seconds

    # Chrome Settings
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless=true")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    time.sleep(DELAY)

    driver = webdriver.Chrome(options=options)
    driver.get("https://investidor10.com.br/acoes/"+ticker)

    time.sleep(DELAY)

    print("[{:s}] connected ...".format(ticker))

    return driver

# Table of Indicators Values 
# PL, PVP, DY, PAYOUT...
def getTickerIndicators(ticker, soup):
    print("[{:s}] extracting indicators...".format(ticker))
    
    indicators = {}
    
    html_indicators_section = soup.find(attrs={"id":"table-indicators"})
    html_indicators_cells = html_indicators_section.find_all(attrs={"class":"cell"})

    # Filling dictionary with indicators
    for indicator in html_indicators_cells:
        name = indicator.find(name="span").contents[0]
        value = indicator.find(name="div").find("span").contents[0]

        name = str(name).lower().strip()
        value = str(value).strip()

        value = convert(value)

        indicators.update({name: value})
    
    return indicators

# Table of company numbers
def getCompanyInfo(ticker, soup):
    print("[{:s}] extracting company info...".format(ticker))
    
    company_info = {}
    
    html_info_about_section = soup.find(attrs={"id":"info_about"})
    html_info_about_cells = html_info_about_section.find_all(attrs={"class":"cell"})

    for info in html_info_about_cells:
        name = str(info.find(attrs={"class":"title"}).contents[0]) # It is a string value
        value = info.find(attrs={"class":"value"}) # Can be a <span> with divs or a span with a text value

        if(value.find(attrs={"class":"detail-value"}) == None): # value == <span class="value">""</span>
            value =  str(value.contents[0]).strip()
        else: # value == <span class="value"><div>""</div></span>
            value = str(value.find(attrs={"class":"detail-value"}).contents[0])
            
            startIndex = value.find(">") + 1 # <div>R$ 00.00</div>
            endIndex = value[1:].find("<")
            moneyIndex= value.find("$")

            if(moneyIndex != -1):
                startIndex = moneyIndex + 2

            value = value[startIndex:endIndex].strip()
        # END IF

        name = name.lower().strip()
        value = convert(value)

        company_info.update({name : value})

    return company_info

# Ticker Price 
# Found in a card away from indicators
def getPrice(ticker, soup):
    print("[{:s}] extracting price...".format(ticker))

    html_price = soup.find(attrs={"class":"_card cotacao"})

    value = str(html_price.find(attrs={"class", "value"})) # Format : 'R$ 00.00'
    value = value[value.find("$")+2:value[1:].find("<")+1]
    value = convert(value)
    
    return {"cotação" : value}

# Ticker Dividend Yield
# Found in a card away from indicators
def getDividendYield(ticker, soup):
    print("[{:s}] extracting dividend yield...".format(ticker))

    html_dy = soup.find(attrs={"class": "_card dy"})

    value = str(html_dy.find_all(name="span")[1].contents[0])
    value = convert(value)
    
    return {"dy" : value}

def isTickerValid(soup):

    not_found_html_element = soup.find(attrs={"class" : "antialised"})

    if type(not_found_html_element) == None:
        return False

    return True


def get_ticker_info(ticker):

    driver = setupConnection(ticker)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    isValid = isTickerValid(soup)

    if not isValid:
        raise Exception.with_traceback("Ticker not foud.")

    ticker_info = {}
    
    ticker_info.update(getPrice(ticker, soup))
    ticker_info.update(getDividendYield(ticker, soup))
    ticker_info.update(getTickerIndicators(ticker, soup))
    ticker_info.update(getCompanyInfo(ticker, soup))

    driver.quit()

    print("[{:s}] extraction complete...".format(ticker))

    return ticker_info
# END