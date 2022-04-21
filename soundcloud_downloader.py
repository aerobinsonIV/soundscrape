from distutils.command.upload import upload
import time
from selenium.webdriver.common.by import By
import selenium
import json
import os
import requests
import pydub
import stagger
from stagger.id3 import *

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

# On the first time a user visits one of their own tracks after logging in, there will be a prompt alerting them that they can auto-master their tracks
# Apparently SoundCloud assumes their users are incompetent. Takes one to know one.
# If present, click the button to dismiss the prompt so we can access the rest of the page.
def dismiss_mastering_prompt_if_present(driver):
    # TODO:
    time.sleep(5)

    try:
        mastering_callout_button = driver.find_element(By.CLASS_NAME, "callout__button")
        mastering_callout_button.click()
        time.sleep(0.5)
    except:
        pass

def driver_with_cookies_from_file(input_file):

    with open(input_file,"r") as f:
        cookies_str = f.read()

    cookies_json = json.loads(cookies_str)

    driver = selenium.webdriver.Chrome()

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

def get_direct_download_button(driver):

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

def dl_cover_artwork(driver, filename):

    cover_artwork_thumb = driver.find_element(By.CLASS_NAME, "sc-artwork-40x")
    cover_artwork_thumb.click()

    print(type(driver))

    cover_artwork_full = driver.find_element(By.CLASS_NAME, "sc-artwork-64x")
    
    # Get the style attribute from the cover art and slice the URL out of the background-image field
    style = cover_artwork_full.get_attribute('style')
    cover_artwork_url = style[style.find("(") + 2:style.find(")") - 1]

    print(cover_artwork_url)

    img_data = requests.get(cover_artwork_url).content
    with open(filename, 'wb') as image_file:
        image_file.write(img_data)

def get_upload_year(driver):
    upload_time_div = driver.find_element(By.CLASS_NAME, "fullHero__uploadTime")
    upload_time_time = upload_time_div.find_element(By.TAG_NAME, "time")
    
    # Last 4 chars of title attribute are the year uploaded
    return upload_time_time.get_attribute('title')[-4:]

def get_title_and_artist(driver, artist_from_url):
    result = {}

    # TODO: Add better handling of collabs, record labels, features, etc.

    # Artist (username)
    if artist_from_url:
        url_base = "https://soundcloud.com/"
        url_rel = driver.current_url[len(url_base):]
        result["artist"] = url_rel[:url_rel.find("/")]
        print(url_rel)
    else:
        username_container = driver.find_element(By.CLASS_NAME, "soundTitle__usernameHeroContainer")
        username_h2 = username_container.find_element(By.CLASS_NAME, "soundTitle__username")
        username_anchor =  username_h2.find_element(By.TAG_NAME, "a")
        result["artist"] = username_anchor.text

    # Title
    title_container = driver.find_element(By.CLASS_NAME, "soundTitle__titleHeroContainer")
    title_h1 = title_container.find_element(By.CLASS_NAME, "soundTitle__title")
    title_span =  title_h1.find_element(By.TAG_NAME, "span")
    result["title"] = title_span.text

    return result

def apply_metadata(artist, title, year):
    
    path = os.path.join(os.getcwd(), "temp/")
    files = os.listdir(path)

    # Find song and artwork image files
    image_extensions = [".jpg", ".png"]
    for file in files:
        if file[-4:] == ".mp3":
            song_file = file
        else:
            for ext in image_extensions:
                if file[-len(ext):] == ext:
                    image_file = file
    print("image file is " + image_file)
    print("song file is " + song_file)

    # Open tag on song file
    tag = stagger.read_tag(os.path.join(path, song_file))
    
    # Title, album
    tag[TIT2] = title
    tag[TALB] = title
    
    # Artist, Album Artist
    tag[TPE1] = artist
    tag[TPE2] = artist

    # Year (Date Of Release)
    tag[TDOR] = year

    # Cover artwork (Attached PICture)
    tag[APIC] = APIC(os.path.join(path, image_file))

    tag.write()

    # Rename song file to title of song (might fail because invalid characters)
    try:
        os.rename(os.path.join(path, song_file), os.path.join(path, f"{title}.mp3"))
    except:
        print("Couldn't rename file, invalid chars")

def convert_downloaded_sounds_to_mp3():
    print("here")
    # Get all files in the temp dir

    path = os.path.join(os.getcwd(), "temp/")

    files = os.listdir(path)
    
    # Find sound files of non-mp3 type
    convertable_extensions = [".wav", ".flac", ".ogg", ".m4a"]
    sound_files = []
    for file in files:
        for ext in convertable_extensions:
            if file[-len(ext):] == ext:
                sound_files.append(file)

    for file in sound_files:
        mp3_filename = os.path.splitext(os.path.basename(file))[0] + '.mp3'
        infile = os.path.join(path, file)
        outfile = os.path.join(path, mp3_filename)
        print(f"Converting {file} to mp3...")
        pydub.AudioSegment.from_file(infile).export(outfile, format='mp3', bitrate="320k")

def move_to_done():
    path = os.path.join(os.getcwd(), "temp/")
    files = os.listdir(path)
    
    for file in files:
        if file[-4:] == ".mp3":
            song_file = file
            break
    
    # move song file to done folder
    os.rename(os.path.join(path, song_file), os.path.join(os.path.join(os.getcwd(), "done/"), song_file))

def clear_temp():
    path = os.path.join(os.getcwd(), "temp/")
    files = os.listdir(path)
    
    for file in files:
        os.remove(os.path.join(path, file))

def read_input_file():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    links = []

    for line in lines:
        links.append(line.strip())

    return links

# Stuff that launches undetected_chromedriver has to be in this main thingy to avoid multithreading problems or something
# https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/561
if __name__ == '__main__':

    # sc_login("cookies.json")

    driver = driver_with_cookies_from_file("cookies.json")
    # Set songs to download to /temp
    params = {'behavior': 'allow', 'downloadPath': os.path.join(os.getcwd(), "temp")}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    links = read_input_file()

    for link in links:
        print(f"link is {link}")
        
        driver.get(link)

        # dismiss_mastering_prompt_if_present(driver)
        
        #Wait for page to load a bit
        time.sleep(2)

        try:
            button = get_direct_download_button(driver)
            button.click()
        except:
            print("Failed to get direct download button. Skipping track.")
            continue

        metadata = get_title_and_artist(driver, True)

        year = get_upload_year(driver)

        dl_cover_artwork(driver, os.path.join(os.getcwd(), "temp/cover-front.jpg"))

        print(f"Artist: {metadata['artist']}, title: {metadata['title']}, year: {year}")

        # Wait for song to download
        time.sleep(10)
        try:
            convert_downloaded_sounds_to_mp3()
            apply_metadata(metadata['artist'], metadata['title'], year)
            move_to_done()
        except:
            # Restart driver
            driver.close()

            driver = driver_with_cookies_from_file("cookies.json")
            # Set songs to download to /temp
            params = {'behavior': 'allow', 'downloadPath': os.path.join(os.getcwd(), "temp")}
            driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

        clear_temp()
