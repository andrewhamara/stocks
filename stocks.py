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

    _open_price = driver.find_element(By.XPATH, _OPEN_PRICE_PATH).text
    _high_price = driver.find_element(By.XPATH, _HIGH_PRICE_PATH).text
    _low_price = driver.find_element(By.XPATH, _LOW_PRICE_PATH).text
    _current_price = driver.find_element(By.XPATH, _CURRENT_PRICE_PATH).text

    # Make an asterisk box to format the output with the prices inside the box
    print('------' + '*' * (len(ticker) + 14))
    print('------* %s Prices *' % ticker)
    print('------' + '*' * (len(ticker) + 14))
    print('------ Open: %s' % _open_price)
    print('------ High: %s' % _high_price)
    print('------ Low: %s' % _low_price)
    print('------ Current: %s' % _current_price)
    print('------' + '*' * (len(ticker) + 14))



#### Load url for main site ####
def loadUrl(url):
    driver.get(url)

    print('- Loading landing page')

    # Give 30 seconds to fully load the URL
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

    # Give 30 seconds to fully load the URL
    loadPage()

    print('--- Loading %s' % ticker)

    _REAL_SEARCH_PATH = '/html/body/div[10]/div/div/div[2]/div/div/div[1]/div/div[1]/span/form/input'
    _real_search_bar = driver.find_element(By.XPATH, _REAL_SEARCH_PATH)

    _real_search_bar.send_keys(ticker)
    _real_search_bar.send_keys(Keys.ENTER)

    # Give 30 seconds to fully load the URL
    loadPage()

    print('---- %s fully loaded' % ticker)

def main():

    _TICKER = str(input('Enter ticker: ')).upper()

    # Trading View
    loadUrl('http://www.tradingview.com/screener/')

    loadPage()

    # Ticker
    loadTicker(_TICKER)

    loadPage()

    # Price
    getPrices(_TICKER)

    driver.quit()


if __name__ == "__main__":
    main()
