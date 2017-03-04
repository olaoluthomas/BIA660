import time
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('http://stackoverflow.com')
elem = driver.find_element_by_name('q')
elem.clear()
elem.send_keys('python')
elem.send_keys(Keys.RETURN)

questions_link = driver.find_elements_by_class_name('question-hyperlink')

time.sleep(5)
driver.close()

2+2