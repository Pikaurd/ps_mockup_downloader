from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
# options.add_argument('--proxy-server http://127.0.0.1:8001')
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

driver = webdriver.Chrome(
    executable_path='/usr/local/bin/chromedriver', options=options)
# driver.get('https://mrmockup.com/freebies/')
driver.get('https://cn.bing.com/')

content = driver.find_elements_by_css_selector(
    '#b_footerItems li.b_footerItems_icp')
anchor = driver.find_element_by_css_selector('#scpl4')
print(f"a.href: {anchor.get_attribute('href')}")

# print(driver.page_source)
