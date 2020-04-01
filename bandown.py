import time

import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from storage.release_mongo_storage import MongoReleaseStorage

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# driver = webdriver.Chrome(options=options)


def fetch_releases():
    print('Bandcamp album downloader')

    storage = MongoReleaseStorage()

    album_page = storage.load_downloadable('', 10)  # Load a single batch of releases from a persistence storage
    for album in album_page.page:
        print('\nGetting album %s' % album.tralbum_url)
        navigate_to_download_screen(album.tralbum_url)
    
    print('Done')


def navigate_to_download_screen(album_url, initiate_download=True):
    try:
        options = Options()
        # options.headless = True
        driver = webdriver.Firefox(options=options)

        driver.get(album_url)
        
        buy_now = driver.find_element_by_css_selector('h4 > button.download-link')
        buy_now.click()
        
        price_field = driver.find_element_by_css_selector("input[id='userPrice']")
        price_field.send_keys('0')
    
        time.sleep(1)
        
        dwnld_link = driver.find_element_by_css_selector(
            "a[onclick='TralbumDownload.showButtonsSection(event); return false']")
        dwnld_link.click()
    
        time.sleep(5)
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
        pagesource = driver.page_source
        return pagesource
    except Exception as e:
        print(e.__class__)
        print('Album %s cannot be downloaded: email-based links are not supported' % album_url)
    finally:
        driver.quit()


if __name__ == "__main__":
    fetch_releases()
