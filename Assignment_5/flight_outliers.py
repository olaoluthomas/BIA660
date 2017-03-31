import time
import pandas as pd
import datetime
from dateutil.parser import parse
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np


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
    time.sleep(2)

    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for i in range(0, len(results), 1):
        if city_name in str(unidecode(results[i].text)):
            target = results[i]

    if target:
        bars = target.find_elements_by_class_name('LJTSM3-w-x')
        data = []
        for bar in bars:
            ActionChains(driver).move_to_element(bar).perform()
            time.sleep(0.001)
            data.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                        target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
    else:
        raise Exception("No relevant results found. Sorry...")

    clean_data = []
    for d in data:
        try:
            clean_data.append([datetime.datetime.date(parse(d[1].split('-')[0].strip())),
                               (parse(d[1].split('-')[0].strip()) - start_date).days,
                               float(d[0].replace('$', '').replace(',', ''))])
        except:
            continue

    df = pd.DataFrame(clean_data, columns=['Day_of_Flight', 'Days_to_date', 'Price'])
    return df

def scrape_data_90(start_date, from_place, to_place, city_name):
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
    time.sleep(2)

    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for i in range(0, len(results), 1):
        if city_name in str(unidecode(results[i].text)):
            target = results[i]
            index_to_stretch = i + 1

    time.sleep(2)
    if target:
        bars = target.find_elements_by_class_name('LJTSM3-w-x')
        data1 = []
        for bar in bars:
            ActionChains(driver).move_to_element(bar).perform()
            time.sleep(0.001)
            data1.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                        target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
    else:
        raise Exception("No relevant results found. Sorry...")

    ActionChains(driver).move_to_element(bars[0]).perform()
    time.sleep(0.5)
    stretch_bar = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[4]/div/div[2]/div[' + str(index_to_stretch)
                                               + ']/div/div[2]/div[2]/div/div[2]/div[5]/div')
    stretch_bar.click()

    time.sleep(2)
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for i in range(0, len(results), 1):
        if city_name in str(unidecode(results[i].text)):
            target = results[i]

    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    data2 = []
    for bar in bars:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.001)
        data2.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                      target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))

    data = data1 + data2[30:]
    clean_data = []
    for d in data:
        try:
            clean_data.append([datetime.datetime.date(parse(d[1].split('-')[0].strip())),
                               (parse(d[1].split('-')[0].strip()) - start_date).days,
                               float(d[0].replace('$', '').replace(',', ''))])
        except:
            continue

    df = pd.DataFrame(clean_data, columns=['Day_of_Flight', 'Days_to_date', 'Price'])
    return df

def task_3_dbscan(d_frame):
    prices = [x for x in d_frame['Price']]
    pr_frame = pd.DataFrame(prices, columns=['Price']).reset_index()

    X = StandardScaler().fit_transform(pr_frame)
    db = DBSCAN(eps=.45, min_samples=3).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    plt.subplots(figsize=(9,6))
    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                markeredgecolor='k', markersize=14)

    plt.title("Total Cluster 60 days: {}".format(clusters), fontsize=14, y=1.01)
    plt.savefig('plot.png')
    d_frame['Labels'] = db.labels_
    return d_frame

def task_3_dbscan90(d_frame):
    prices = [x for x in d_frame['Price']]
    pr_frame = pd.DataFrame(prices, columns=['Price']).reset_index()

    X = StandardScaler().fit_transform(pr_frame)
    db = DBSCAN(eps=.25, min_samples=3).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    plt.subplots(figsize=(9,6))
    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                markeredgecolor='k', markersize=14)

    plt.title("Total Cluster 90 days: {}".format(clusters), fontsize=14, y=1.01)
    plt.savefig('plot90.png')
    d_frame['Labels'] = db.labels_
    return d_frame

flight_df = scrape_data(datetime.datetime(2017, 4, 1), 'NYC', 'France', 'Toulouse')
plot_df = task_3_dbscan(flight_df)

flight90_df = scrape_data_90(datetime.datetime(2017, 4, 1), 'NYC', 'France', 'Toulouse')
plot90_df = task_3_dbscan90(flight90_df)

2+2