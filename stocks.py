###################################################################
                                                                  #
from selenium import webdriver                                    #
from selenium.webdriver.chrome.service import Service             #
from selenium.webdriver.support.ui import WebDriverWait           #
from selenium.webdriver.support import expected_conditions as EC  #
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
from funPrints import *                                           #
                                                                  #
# Don't need all that noise :)                                    #
logging.basicConfig(level=logging.CRITICAL)                       #
                                                                  #
###################################################################


###################################################################
                                                                  #
UP_STOCKS_COUNT, DOWN_STOCKS_COUNT = 0, 0                         #
                                                                  #
###################################################################

#### Get price of ticker ####
def getPrices(ticker):
    _OPEN_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]'
    _HIGH_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[3]/div[2]'
    _LOW_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[4]/div[2]'
    _CURRENT_PRICE_PATH = '/html/body/div[2]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[5]/div[2]'

    print('--- Getting price of %s' % ticker)

    # Assume that if one price loads, they all did
    #WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, _OPEN_PRICE_PATH)))
    time.sleep(3)
    _open_price = driver.find_element(By.XPATH, _OPEN_PRICE_PATH).text

    _high_price = driver.find_element(By.XPATH, _HIGH_PRICE_PATH).text

    _low_price = driver.find_element(By.XPATH, _LOW_PRICE_PATH).text

    _current_price = driver.find_element(By.XPATH, _CURRENT_PRICE_PATH).text

    print('---- %s price found\n' % ticker)

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
    print('------+' + '*' * longest_line + '+\n')

    _FLOAT_OPEN_PRICE = float(_open_price)
    _FLOAT_CURRENT_PRICE = float(_current_price)

    global UP_STOCKS_COUNT, DOWN_STOCKS_COUNT

    if _FLOAT_OPEN_PRICE > _FLOAT_CURRENT_PRICE:
        _DIFFERENCE = _FLOAT_OPEN_PRICE - _FLOAT_CURRENT_PRICE
        _PERCENT = (_DIFFERENCE) / _FLOAT_OPEN_PRICE * 100
        _diff_line = f" {ticker} is down by ${_DIFFERENCE:.2f} (-{_PERCENT:.2f}%) "
        DOWN_STOCKS_COUNT += 1
    elif _FLOAT_CURRENT_PRICE > _FLOAT_OPEN_PRICE:
        _DIFFERENCE = _FLOAT_CURRENT_PRICE - _FLOAT_OPEN_PRICE
        _PERCENT = (_DIFFERENCE) / _FLOAT_OPEN_PRICE * 100
        _diff_line = f" {ticker} is up by ${_DIFFERENCE:.2f} (+{_PERCENT:.2f}%) "
        UP_STOCKS_COUNT += 1
    else:
        _diff_line = f" {ticker} is unchanged "

    # Taking no credit or blame for this chatGPT magic
    _diff_line_len = len(_diff_line)
    print('------+' + '*' * _diff_line_len + '+')
    print('------|' + _diff_line.center(_diff_line_len) + '|')
    print('------+' + '*' * _diff_line_len + '+\n')


#### Load ticker ####
def loadTicker(ticker):
    _INITIAL_SEARCH_PATH = '/html/body/div[3]/div[3]/div[2]/div[2]/div/div/div/button[1]/span'

    time.sleep(2)
    driver.find_element(By.XPATH, _INITIAL_SEARCH_PATH).click()

    print('- Loading %s' % ticker)

    _REAL_SEARCH_PATH = '/html/body/div[10]/div/div/div[2]/div/div/div[1]/div/div[1]/span/form/input'

    time.sleep(2)
    _real_search_bar = driver.find_element(By.XPATH, _REAL_SEARCH_PATH)
    _real_search_bar.send_keys(ticker)
    _real_search_bar.send_keys(Keys.ENTER)

    print('-- %s fully loaded' % ticker)


#### Check input ####
def getInput() -> str:

    while True:
        _TICKER = str(input('Enter ticker (q to exit): ')).upper()

        if len(_TICKER) > 5:
            print('Ticker is too long')

        elif len(_TICKER) < 1:
            print('Ticker is too short')
        else:
            return _TICKER

def main():
    try:
        driver.get('http://www.tradingview.com/screener')
        _TICKER = ''
        while _TICKER != 'Q':
            _TICKER = getInput()
            if _TICKER != 'Q':
                loadTicker(_TICKER)
                getPrices(_TICKER)
    except Exception as e:
        print(f"An error has occured: {e}")
    finally:
        driver.quit()
        if UP_STOCKS_COUNT > DOWN_STOCKS_COUNT:
            stocksUpMessage()
        elif DOWN_STOCKS_COUNT > UP_STOCKS_COUNT:
            stocksDownMessage()
        else:
            stocksEvenMessage()

if __name__ == "__main__":
    main()
