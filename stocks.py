###################################################################
                                                                  #
from selenium import webdriver                                    #
from selenium.webdriver.chrome.service import Service             #
from selenium.webdriver.support.ui import WebDriverWait           #
from selenium.webdriver.common.by import By                       #
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


def loadUrl(url):
    driver.get(url)

    print('---- loading URL      ----')

    # Give 30 seconds to fully load the URL
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    print('---- URL fully loaded ----')


def main():
    loadUrl('http://www.google.com')

    driver.quit()


if __name__ == "__main__":
    main()
