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



#### Load url for main site ####
def loadUrl(url):
    driver.get(url)

    print('---- loading URL         ----')

    # Give 30 seconds to fully load the URL
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    print('---- URL fully loaded    ----')


#### Load ticker ####
def loadTicker(ticker):
    _initial_search_bar = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/div[2]/div/div/button[1]/span')

    _initial_search_bar.click()

    time.sleep(2)

    print('---- loading ticker      ----')

    _real_search_bar = driver.find_element(By.XPATH, '//*[@id="overlap-manager-root"]/div/div/div[2]/div/div/div[1]/div/div[1]/span/form/input')

    _real_search_bar.send_keys(ticker)

    time.sleep(2)

    _real_search_bar.send_keys(Keys.ENTER)

    # Give 30 seconds to fully load the URL
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    print('---- ticker fully loaded ----')

    time.sleep(3)

def main():

    # Trading View
    loadUrl('http://www.tradingview.com/screener/')

    # Ticker
    loadTicker('AAPL')

    driver.quit()


if __name__ == "__main__":
    main()
