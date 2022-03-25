import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc


def has_direct_download(link):
    
    driver = uc.Chrome()
    driver.get(link)

    time.sleep(3)

    three_dots_button = driver.find_element(By.CLASS_NAME, "sc-button-more")

    three_dots_button.click()
    
    time.sleep(0.5)
    try:
        download_button = driver.find_element(By.CLASS_NAME, "sc-button-download")
        print("Found download button")
    except:
        print("Didn't find download button")
        return -1

    download_button.click()

# Stuff that launches undetected_chromedriver has to be in this main thingy to avoid multithreading problems or something
# https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/561
if __name__ == '__main__':
    has_direct_download("https://soundcloud.com/jousboxx/time")
    # has_direct_download("https://soundcloud.com/zensupremacy/frij-trajectory")
    time.sleep(99999)

