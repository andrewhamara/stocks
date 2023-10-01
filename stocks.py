###################################################################
                                                                  #
from selenium import webdriver                                    #
from selenium.webdriver.chrome.service import Service             #
from selenium.webdriver.support.ui import WebDriverWait           #
from selenium.webdriver.common.by import By                       #
from selenium.webdriver.common.keys import Keys                   #
                                                                  #
_service = Service()                                              #
_options = webdriver.ChromeOptions()                              #
_options.add_argument('--headless')                               #
_options.add_argument("--window-size=1920,1080")                  #
driver = webdriver.Chrome(service=_service, options=_options)     #
                                                                  #
###################################################################


###################################################################
                                                                  #
import time                                                       #
import logging                                                    #
import sys                                                        #
                                                                  #
# Don't need all that noise :)                                    #
logging.basicConfig(level=logging.CRITICAL)                       #
                                                                  #
###################################################################


#### Get price of ticker ####
def getPrices(ticker):
    _OPEN_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]'
    _HIGH_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[3]/div[2]'
    _LOW_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[4]/div[2]'
    _CURRENT_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[5]/div[2]'

    print('----- Getting price of %s' % ticker)


    ##########################################################################################

    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element(By.XPATH, _OPEN_PRICE_PATH).is_displayed()
    )
    _open_price = driver.find_element(By.XPATH, _OPEN_PRICE_PATH).text

    ##########################################################################################

    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element(By.XPATH, _HIGH_PRICE_PATH).is_displayed()
    )
    _high_price = driver.find_element(By.XPATH, _HIGH_PRICE_PATH).text

    ##########################################################################################

    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element(By.XPATH, _LOW_PRICE_PATH).is_displayed()
    )
    _low_price = driver.find_element(By.XPATH, _LOW_PRICE_PATH).text

    ##########################################################################################

    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element(By.XPATH, _CURRENT_PRICE_PATH).is_displayed()
    )
    _current_price = driver.find_element(By.XPATH, _CURRENT_PRICE_PATH).text

    ##########################################################################################

    print('------ %s price found' % ticker)

    printMenu(ticker, _open_price, _high_price, _low_price, _current_price)


#### Print menu ####
def printMenu(ticker : str, _open_price : str, _high_price : str, _low_price : str, _current_price: str):
    header = f" {ticker} Prices "
    header_line = '*' * len(header)

    open_line = f" Open: {_open_price} "
    high_line = f" High: {_high_price} "
    low_line = f" Low: {_low_price} "
    current_line = f" Current: {_current_price} "

    # Find the longest line to adjust the width of the box
    longest_line = max(len(open_line), len(high_line), len(low_line), len(current_line), len(header_line))

    print('------+' + '*' * longest_line + '+')
    print('------|' + header.center(longest_line) + '|')
    print('------+' + '-' * longest_line + '+')
    print('------|' + open_line.ljust(longest_line) + '|')
    print('------|' + high_line.ljust(longest_line) + '|')
    print('------|' + low_line.ljust(longest_line) + '|')
    print('------|' + current_line.ljust(longest_line) + '|')
    print('------+' + '*' * longest_line + '+')

    main()


#### Load url for main site ####
def loadUrl(url):
    driver.get(url)

    print('- Loading landing page')

    loadPage()

    print('-- Landing page fully loaded')


#### Let page fully load ####
def loadPage():
    # Give 30 seconds to fully load the URL
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


#### Load ticker ####
def loadTicker(ticker):
    _INITIAL_SEARCH_PATH = '/html/body/div[3]/div[3]/div[2]/div[2]/div/div/div/button[1]/span'
    _initial_search_bar = driver.find_element(By.XPATH, _INITIAL_SEARCH_PATH)

    _initial_search_bar.click()

    loadPage()

    print('--- Loading %s' % ticker)

    _REAL_SEARCH_PATH = '/html/body/div[10]/div/div/div[2]/div/div/div[1]/div/div[1]/span/form/input'

    # Wait until the search bar is visible
    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element(By.XPATH, _REAL_SEARCH_PATH).is_displayed()
    )

    _real_search_bar = driver.find_element(By.XPATH, _REAL_SEARCH_PATH)

    _real_search_bar.send_keys(ticker)
    _real_search_bar.send_keys(Keys.ENTER)

    loadPage()

    print('---- %s fully loaded' % ticker)


#### Check input ####
def getInput() -> str:

    while True:
        _TICKER = str(input('Enter ticker (q to exit): ')).upper()

        if _TICKER.upper() == 'Q':
            sys.exit()

        if len(_TICKER) > 5:
            print('Ticker is too long')

        elif len(_TICKER) < 1:
            print('Ticker is too short')
        else:
            return _TICKER


def main():
    _TICKER = getInput()
    loadUrl('http://www.tradingview.com/screener/')
    loadPage()
    loadTicker(_TICKER)
    loadPage()
    getPrices(_TICKER)
    driver.quit()

if __name__ == "__main__":
    main()
