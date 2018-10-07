# All the Required Imports

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import requests
import re
import time
import csv

# Custom Made Scroller

def scroll_shim(passed_in_driver, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        passed_in_driver.execute_script(scroll_by_coord)
        passed_in_driver.execute_script(scroll_nav_out_of_way)

# Creating a Firefox instance and navigating to the McD's listings page.
       
binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
caps = DesiredCapabilities().FIREFOX
caps["marionette"] = True
driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary, executable_path ='C:\\Users\\samue\\Anaconda3\\Menu\\geckodriver')
driver.get("https://www.zomato.com")
driver.implicitly_wait(10)
assert "Zomato" in driver.title
time.sleep(5)

elem1 = driver.find_element_by_xpath('//*[@id="location_pretext"]')
elem1.click()
elem2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="location_input"]')))
try:
    elem2.send_keys("Pune")
finally:
    dropdown = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/ul[3]/div[1]')
    dropdown.click()
elem3 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="keywords_input"]')))
time.sleep(5)
try:
    elem3.clear()
    elem3.send_keys("McDonald's")
finally:
    elem3.send_keys(Keys.ARROW_DOWN)
    elem3.send_keys(Keys.ENTER)
time.sleep(2)
# Collecting the URLs for listings pages 
link1 = driver.current_url
elem4 = driver.find_element_by_css_selector('a.paginator_item:nth-child(4)')
if 'firefox' in driver.capabilities['browserName']:
    scroll_shim(driver, elem4)
actions = ActionChains(driver)
actions.move_to_element(elem4)
actions.perform()
try:
    elem4.click()
except StaleElementReferenceException:
    pass
link2 = driver.current_url
driver.quit()

# Scrapping the URLs of all the listings of McD in Pune.
agent = {"User-Agent":"Mozilla/5.0"}
page1_html = requests.get(link1, headers=agent)
page1_data = page1_html.content
soup1 = BeautifulSoup(page1_data, "lxml")
page2_html = requests.get(link2, headers=agent)
page2_data = page2_html.content
soup2 = BeautifulSoup(page2_data, "lxml")

links1 = soup1.find_all("a", class_=re.compile("result-title"))
links2 = soup2.find_all("a", class_=re.compile("result-title"))

links = []
for y in links1:
    links.append(y['href'])
time.sleep(1)
for i in links2:
    links.append(i['href'])

print(links)
#Capturing the values from the resulting pages.
Name = []
Phone = []
Address = []
Reviewer_Name = []
Review_Score = []
Review_Text1 = []
Link = []

for link in range(len(links)):
    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
    caps = DesiredCapabilities().FIREFOX
    caps["marionette"] = True
    driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary, executable_path ='C:\\Users\\samue\\Anaconda3\\Menu\\geckodriver')
    driver.get(links[link])
    Name.append(driver.find_element_by_css_selector('a.header').text)
    Phone.append(driver.find_element_by_css_selector('span.tel:nth-child(1)').text)
    Address.append(driver.find_element_by_css_selector('.resinfo-icon > span:nth-child(1)').text)
    Reviewer_Name.append(driver.find_element_by_css_selector('div.item:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)').text)
    Review_Score.append(driver.find_element_by_css_selector('div.rev-text:nth-child(4) > div:nth-child(1)').get_attribute('aria-label'))
    Review_Text1.append(driver.find_element_by_css_selector('div.rev-text:nth-child(4)').text)
    Link.append(links[link])
    driver.quit()

# Processing the captured data.
Review_Text = []
for i in range(len(Review_Text1)):
    x = Review_Text1[i][8:]
    y = x.replace('\n', ' ')
    Review_Text.append(y)

#Storing the values in a CSV File.
fieldnames = ['Name','Phone', 'Address', 'Reviewer_Name', 'Review_Score', 'Review_Text', 'Link'] 
with open('output.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    writer.writerows(zip(Name, Phone, Address, Reviewer_Name, Review_Score, Review_Text, Link))

# THE END




















    
