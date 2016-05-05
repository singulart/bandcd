import sys, os
import json
import tempfile
import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print 'Bandcamp album downloader'
album_data_files = os.listdir(tempfile.gettempdir() + '/freeband.py')
driver = webdriver.Firefox()
jsons = (f for f in album_data_files if f.endswith('.json'))
for json_file in jsons:
	with open(json_file, 'r') as infile:
		json_data = infile.read()
		album = json.loads(json_data)

		url = album['url']

		print '\nGetting album %s' % url
		driver.get(url)
		buy_now = driver.find_element_by_css_selector('h4 > button.download-link')
		buy_now.click()

		price_field = driver.find_element_by_css_selector("input[id='userPrice']")
		price_field.send_keys('0')

		dnow = driver.find_element_by_css_selector("button[onclick='TralbumDownload.checkout(); return false']")
		dnow.click()

		try:
			format_drop_down = driver.find_element_by_id('downloadFormatMenu0')
			format_drop_down.click()
			flac = driver.find_element_by_css_selector("li[data-value='flac']")
			flac.click()

			go = WebDriverWait(driver, 60).until(
					EC.presence_of_element_located((By.CSS_SELECTOR, "a.downloadGo"))
			)

			wget.download(go.get_attribute('href'))
		except:
			print 'Album %s cannot be downloaded: email-based links are not supported' % url

driver.quit()
print 'Done'
