import time
import pandas as pd
import datetime
from dateutil.parser import parse
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.spatial.distance import euclidean
plt.style.use('ggplot')


def scrape_data(start_date, from_place, to_place, city_name):
    date = str(start_date).split(' ')[0]
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/#explore;li=3;lx=5;d=' + date)
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
    time.sleep(5)

    # if the script breaks at this point, increase the amount of sleep time above to allow the element to stabilize
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
            clean_data.append(
                [(parse(d[1].split('-')[0].strip()) - date).days, float(d[0].replace('$', '').replace(',', ''))])
        except:
            continue
    df = pd.DataFrame(clean_data, columns=['Day_of_Flight', 'Price'])
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

    # if the script breaks at this point, increase the amount of sleep time above to allow the element to stabilize
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for i in range(0, len(results), 1):
        if city_name in str(unidecode(results[i].text)):
            target = results[i]
            index_to_stretch = i + 1
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
            clean_data.append(
                [(parse(d[1].split('-')[0].strip()) - day).days, float(d[0].replace('$', '').replace(',', ''))])
        except:
            continue
    df = pd.DataFrame(clean_data, columns=['Day_of_Flight', 'Price'])
    return df


def task_3_dbscan(d_frame):
    X = StandardScaler().fit_transform(d_frame)
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

    plt.title("Total Cluster: {}".format(clusters), fontsize=14, y=1.01)
    d_frame['Labels'] = db.labels_

    def calculate_cluster_means(X, labels, quiet=False):
        lbls = np.unique(labels)

        cluster_means = [np.mean(X[labels == num, :], axis=0) for num in lbls if num != -1]

        if not quiet:
            print "Cluster labels: {}".format(np.unique(lbls))
            print "Cluster Means: {}".format(cluster_means)

        return cluster_means

    def print_distance(point_of_interest, cluster_means):
        dist = [euclidean(point_of_interest, cm) for cm in cluster_means]
        print "Euclidean distance: {}".format(dist)

    def plot_the_clusters(X, dbscan_model, point_of_interest=None, set_size=True,
                          markersize=14):
        labels = dbscan_model.labels_
        clusters = len(set(labels))
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

        if set_size:
            plt.subplots(figsize=(12, 8))

        for k, c in zip(unique_labels, colors):
            class_member_mask = (labels == k)
            xy = X[class_member_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                     markeredgecolor='k', markersize=markersize)

        if point_of_interest is not None:
            plt.plot(point_of_interest[0], point_of_interest[1], 'xr', markersize=markersize + 3)

        plt.title("Total Clusters: {}".format(clusters), fontsize=14, y=1.01)

        return colors, unique_labels

    def new_dbscan(X, dbscan_model, point_of_interest):
        cluster_means = calculate_cluster_means(X, dbscan_model.labels_)
        print_distance(point_of_interest, cluster_means)
        return plot_the_clusters(X, dbscan_model, point_of_interest)

    plt.savefig('task_3_dbscan.png')


def task_3_IQR(df_frame):
    sorted_frame = df_frame.sort_values(by='Price').reset_index()
    outliers = []
    q1 = sorted_frame['Price'][:(len(sorted_frame)//2)].median()
    q3 = sorted_frame['Price'][(len(sorted_frame)//2):].median()
    iqr = q3 - q1
    for index, value in enumerate(sorted_frame['Price']):
        if value < (q1 - 1.5 * iqr) or value > (q3 + 1.5 * iqr):
            outliers.append((index, value))
    if len(outliers) > 0:
        return outliers
    else:
        print "Sorry, there are no outliers in this dataframe..."
    df_frame['Price'].plot.box()
    plt.savefig('task_3_iqr.png')

flight_df = scrape_data(datetime.datetime(2017, 4, 10), 'NYC', 'France', 'Toulouse')
plot_df = task_3_dbscan(flight_df)

flight90_df = scrape_data_90(datetime.datetime(2017, 4, 10), 'NYC', 'France', 'Toulouse')
plot90_df = task_3_dbscan(flight90_df)

# PyCharm breakpoint
2+2