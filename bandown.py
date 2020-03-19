import json
import os
import tempfile
import time

import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Firefox()


def fetch_releases():
    print('Bandcamp album downloader')
    album_data_files = os.listdir(tempfile.gettempdir() + '/freeband.py')
    jsons = [tempfile.gettempdir() + '/freeband.py/' + f for f in album_data_files if f.endswith('.json')]

    for json_file in jsons:
        with open(json_file, 'r') as infile:
            json_data = infile.read()
            album = json.loads(json_data)
            
            url = album['url']
            
            print('\nGetting album %s' % url)
            navigate_to_download_screen(url)
    
    driver.quit()
    print('Done')


def navigate_to_download_screen(album_url, initiate_download=True):
    try:
        driver.get(album_url)
        
        buy_now = driver.find_element_by_css_selector('h4 > button.download-link')
        buy_now.click()
        
        price_field = driver.find_element_by_css_selector("input[id='userPrice']")
        price_field.send_keys('0')
    
        time.sleep(1)
        
        dwnld_link = driver.find_element_by_css_selector(
            "a[onclick='TralbumDownload.showButtonsSection(event); return false']")
        dwnld_link.click()
    
        time.sleep(1)
        dnow = driver.find_elements_by_css_selector("button[onclick='TralbumDownload.checkout(); return false']")[1]
        dnow.click()

        if initiate_download:
            go = WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".item-button:last-of-type"))
            )
            # Downloads a zip file to current directory
            wget.download(go.get_attribute('href'))
        else:
            time.sleep(2)
    except:
        print('Album %s cannot be downloaded: email-based links are not supported' % album_url)
    return driver


if __name__ == "__main__":
    fetch_releases()
