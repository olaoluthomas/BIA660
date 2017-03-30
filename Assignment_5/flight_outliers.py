import time
import pandas as pd
import datetime
from dateutil.parser import parse
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def scrape_data(start_date, from_place, to_place, city_name):
    date = str(start_date).split(" ")[0]
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/#explore;li=3;lx=5;d=' + str(date))
    from_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div')
    from_input.click()
    action1 = ActionChains(driver)
    action1.send_keys(from_place)
    action1.send_keys(Keys.ENTER)
    action1.perform()
    time.sleep(0.05)

    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_input.click()
    action2 = ActionChains(driver)
    action2.send_keys(to_place)
    action2.send_keys(Keys.ENTER)
    action2.perform()
    time.sleep(0.5)

    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for i in range(0, len(results), 1):
        if city_name in str(unidecode(results[i].text)):
            target = results[i]

    time.sleep(7)
    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    data = []
    for bar in bars:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.001)
        data.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                     target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))

    clean_data = []
    for d in data:
        clean_data.append((parse(d[1].split('-')[0].strip()), float(d[0].replace('$', '').replace(',', ''))))

    df = pd.DataFrame(clean_data, columns=['Day_of_Flight', 'Price($)'])
    return df

flight_df = scrape_data(datetime.datetime(2017, 4, 17), 'Florida', 'South Africa', 'Johannesburg')

2+2
