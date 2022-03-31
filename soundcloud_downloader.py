import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import os

import undetected_chromedriver as uc

def sc_login(output_file):

    driver = uc.Chrome()
    driver.get("https://soundcloud.com/signin")
    
    time.sleep(20)
    print("Getting cookies")

    cookies = driver.get_cookies()
    
    # Save cookies to file
    cookies_json = json.dumps(cookies)
    with open(output_file,"w") as f:
        f.write(cookies_json)

def driver_with_cookies_from_file(input_file):

    with open(input_file,"r") as f:
        cookies_str = f.read()

    cookies_json = json.loads(cookies_str)

    driver = webdriver.Chrome()

    # We first have to navigate to the domain we want to set cookies for, otherwise the browser won't let us set them
    driver.get("https://soundcloud.com/")

    for cookie in cookies_json:
        driver.add_cookie(cookie)
    
    # # TODO:
    # time.sleep(3)

    # TODO: For an unknown reason, the page loads indefintely when we try to fresh soundcloud after loading the cookies. Going to google and back fixes it.
    # Find a less gross fix to this issue
    driver.get("https://google.com/")
    # time.sleep(3)
    driver.get("https://soundcloud.com/")

    return driver

def get_direct_download_button(driver, link):
    
    driver.get(link)

    # TODO:
    time.sleep(5)

    # On the first time a user visits one of their own tracks after logging in, there will be a prompt alerting them that they can auto-master their tracks
    # Apparently SoundCloud assumes their users are incompetent. Takes one to know one.
    # If present, click the button to dismiss the prompt so we can access the rest of the page.
    try:
        mastering_callout_button = driver.find_element(By.CLASS_NAME, "callout__button")
        mastering_callout_button.click()
        time.sleep(0.5)
    except:
        pass

    three_dots_button = driver.find_element(By.CLASS_NAME, "sc-button-more")

    three_dots_button.click()
    
    # TODO:
    time.sleep(0.5)
    try:
        download_button = driver.find_element(By.CLASS_NAME, "sc-button-download")
        print("Found download button")
        return download_button
    except:
        print("Didn't find download button")
        return None

# Stuff that launches undetected_chromedriver has to be in this main thingy to avoid multithreading problems or something
# https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/561
if __name__ == '__main__':
    # sc_login("cookies.json")

    driver = driver_with_cookies_from_file("cookies.json")
    
    # Set songs to download to /temp
    params = {'behavior': 'allow', 'downloadPath': os.path.join(os.getcwd(), "temp")}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    
    dl_button = get_direct_download_button(driver, "https://soundcloud.com/jousboxx/time")
    dl_button.click()

    time.sleep(5)