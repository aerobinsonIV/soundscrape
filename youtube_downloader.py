import argparse
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

sys.path.insert(0, os.path.join(os.getcwd(), "stagger"))
import stagger
from stagger.id3 import *

def get_yt_music_metadata(link: str):
    
    TITLE_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/yt-formatted-string"
    ARTIST_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[1]"
    ALBUM_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/a[2]"
    YEAR_XPATH = "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[2]/span/span[2]/yt-formatted-string/span[3]"

    driver = webdriver.Firefox()
    
    ublock_origin_path = "../ublock_origin-1.43.0.xpi"
    driver.install_addon(ublock_origin_path)
    
    driver.get(link)

    wait_for_section = WebDriverWait(driver, 180)
    wait_for_section.until(expected_conditions.presence_of_element_located((By.XPATH, ARTIST_XPATH)))
    
    title_tag = driver.find_element(By.XPATH, TITLE_XPATH)
    artist_tag = driver.find_element(By.XPATH, ARTIST_XPATH)
    title = title_tag.get_attribute("innerHTML")
    artist = artist_tag.get_attribute("innerHTML")

    # For singles, finding album will fail. 
    # And also year for some reason, I guess it displays year for albums only
    try:
        album_tag = driver.find_element(By.XPATH, ALBUM_XPATH)
        year_tag = driver.find_element(By.XPATH, YEAR_XPATH)
        album = album_tag.get_attribute("innerHTML")
        year = year_tag.get_attribute("innerHTML")
    except:
        album = title
        year = None

    driver.close()
    
    return title, artist, album, year

def process_link(link: str, cover_artwork: bool = False, music: bool = False):
    
    listdir_before = os.listdir()
    
    args = "--extract-audio "
    args += "--audio-format mp3 --audio-quality 256k"
    
    if cover_artwork:
        args += "--embed-thumbnail "

    os.system("youtube-dl" + " " + args + " " + link)

    listdir_after = os.listdir()
    newly_downloaded_file = None
    for file in listdir_after:
        if file not in listdir_before:
            newly_downloaded_file = file            

    if newly_downloaded_file == None:
        raise Exception(f"Couldn't identify downloaded file for {link}")

    if music:
        print("Got music param")
        
        # Back out of temp
        # TODO: Is there a way to write this so this func doesn't have to trust main to cd,
        # and so that the metadata function doesn't have to trust this one? Unintuitive code flow
        title, artist, album, year = get_yt_music_metadata(link)

        # Open tag on song file
        tag = stagger.default_tag()
        
        tag['TIT2'] = title
        tag['TPE1'] = artist # Artist
        tag['TPE2'] = artist # Album artist
        tag['TALB'] = album
        tag['TYER'] = year # TODO: It's complaining about this one

        tag.write(newly_downloaded_file)

        # Rename file to title of song but keep extension
        os.rename(newly_downloaded_file, title + newly_downloaded_file[newly_downloaded_file.find("."):])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="YouTube link or path of a file containing a list of YouTube links")
    parser.add_argument("-c", "--cover-artwork", help="Embed video thumbnail as cover artwork", action='store_true')
    parser.add_argument("-m", "--music", help="Treat this as a YouTube music link (rather than e.g. a music video) and get the title, artist, and year from the webpage.", action='store_true')
    
    args = parser.parse_args()

    print(args.target)

    # Download songs to the temp folder
    os.chdir("./temp")

    if args.target[:7] == "http://" or args.target[:8] == "https://" or args.target[:4] == "www.":
        # URL
        process_link(args.target, args.cover_artwork, args.music)
    else:
        # Path to file containing list of links
        with open(os.path.join(os.getcwd(), args.target), 'r') as f:
            lines = f.readlines()

        for line in lines:
                print(f"Downloading {line}", end="")
                process_link(line, args.cover_artwork, args.music)
