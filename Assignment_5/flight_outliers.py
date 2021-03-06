import time
import pandas as pd
import datetime
from dateutil.parser import parse
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urlparse import urlparse, urlunparse
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
from scipy.spatial.distance import euclidean
plt.style.use('ggplot')

def scrape_data(start_date, from_place, to_place, city_name):
    date = str(start_date).split(' ')[0]
    driver = webdriver.Chrome()
    url = 'https://www.google.com/flights/explore/#explore;li=3;lx=5;d=' + date
    driver.get(url)
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

    url = driver.current_url
    parsed_url = urlparse(url)
    # url.replace(url[url.find('d='):], 'd={}'.format(date))
    for param in parsed_url.fragment.split(';'):
        if 'd=' in param:
            url = url.replace(param, 'd={}'.format(date))
    driver.get(url)
    time.sleep(5)

    # if the script breaks at this point, increase the amount of sleep time above to allow the element to stabilize
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for i in range(len(results)):
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
                [(parse(d[1].split('-')[0].strip()) - start_date).days, float(d[0].replace('$', '').replace(',', ''))])
        except Exception as e:
            print "Something's broken..."
    df = pd.DataFrame(clean_data, columns=['Day', 'Price'])
    df.to_csv('Munich.csv')
    return df

def scrape_data_90(start_date, from_place, to_place, city_name):
    date = str(start_date).split(" ")[0]
    driver = webdriver.Chrome()
    url = 'https://www.google.com/flights/explore/#explore;li=3;lx=5;d=' + date
    driver.get(url)
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

    url = driver.current_url
    parsed_url = urlparse(url)
    for param in parsed_url.fragment.split(';'):
        if 'd=' in param:
            url = url.replace(param, 'd={}'.format(date))
    driver.get(url)
    time.sleep(5)

    # if the script breaks at this point, increase the amount of sleep time above to allow the element to stabilize
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for i in range(len(results)):
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
    for i in range(len(results)):
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
                [(parse(d[1].split('-')[0].strip()) - start_date).days, float(d[0].replace('$', '').replace(',', ''))])
        except:
            continue
    df = pd.DataFrame(clean_data, columns=['Day', 'Price'])
    return df


def task_3_dbscan(d_frame):
    scaler = StandardScaler()
    X = scaler.fit_transform(d_frame)
    db = DBSCAN(eps=0.27, min_samples=3).fit(X)
    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    plt.subplots(figsize=(9,6))
    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                markeredgecolor='k', markersize=10)

    plt.title("Total Cluster: {}".format(clusters), fontsize=14, y=1.01)
    plt.savefig('task_3_dbscan.png')
    d_frame['Labels'] = db.labels_

    lbls = np.unique(labels)
    cluster_means = [np.mean(X[labels == num, :], axis=0) for num in lbls if num != -1]
    cluster_sds = [X[labels == num, :1].std() for num in lbls if num != -1]
    outliers = [x for x in X[db.labels_ == -1]]
    nrst_clstr = []
    for x in outliers:
        min_dist = min([(euclidean(x, cm), cm) for cm in cluster_means])
        for i in range(len(cluster_means)):
            if np.array_equal(min_dist[1], cluster_means[i]):
                nrst_clstr.append(i)

    gd_outliers = []
    def xform(arr):
        flt_price = scaler.inverse_transform(arr)[1]
        return flt_price

    for i in range(len(outliers)):
        if scaler.inverse_transform(cluster_means[nrst_clstr[i]] - 2 * cluster_sds[nrst_clstr[i]])[1] > 50:
            spread = xform((cluster_means[nrst_clstr[i]] - 2 * cluster_sds[nrst_clstr[i]]))
            mn_price = xform(cluster_means[nrst_clstr[i]])
            outlier_price = xform(outliers[i])
            if mn_price - outlier_price >= spread:
                gd_outliers.append(outliers[i])
        else:
            if cluster_means[nrst_clstr[i]][1] - 2 * cluster_sds[nrst_clstr[i]] > outliers[i][1]:
                gd_outliers.append(outliers[i])
    if len(gd_outliers) > 0:
        gd_flights = scaler.inverse_transform(gd_outliers)
        df_new = pd.DataFrame(gd_flights, columns= ['Day', 'Price'])
        return df_new
    else:
        print "No points satisfy the conditions set."

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

def task_4_dbscan(d_frame):
    scaler = MinMaxScaler()
    X = scaler.fit_transform(d_frame)
    db = DBSCAN(eps=0.105, min_samples=5).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    plt.subplots(figsize=(9, 6))
    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                 markeredgecolor='k', markersize=10)

    plt.title("Total Cluster: {}".format(clusters), fontsize=14, y=1.01)
    plt.savefig('task_4_dbscan.png')
    d_frame['Labels'] = db.labels_

    lbls = np.unique(labels)
    cluster_means = [np.mean(X[labels == num, :], axis=0) for num in lbls if num != -1]

    def xform(arr):
        day_price = scaler.inverse_transform(arr)
        return day_price

    total = []
    cluster_list = []
    for i in range(len(cluster_means)):
        cluster = X[labels == i]
        if len(cluster) >= 5:
            sorted_prices = sorted([xform(x)[1] for x in cluster])[:5]
        if (sorted_prices[4] - sorted_prices[0]) <= 20:
            if [(abs(sorted_prices[l] - sorted_prices[l+1]) < 20) for l in range(4)]:
                cluster_list.append(cluster)
    if cluster_list:
        if len(cluster_list) > 1:
            for clustr in cluster_list:
                total.append(sum(p[1] for p in xform(clustr)))
            min_index = total.index(min(total))
            chpst = cluster_list[min_index]
        elif len(cluster_list) == 1:
            chpst = cluster_list[0]
        # I just realized the code below is wrong; it doesn't return the 5-day period with the lowest average price
        sortd = sorted(xform(chpst))[:5]
        return pd.DataFrame(sortd, columns=['Day', 'Price'])
    else:
        print "None of the clusters meet the conditions set."

flight_df = scrape_data(datetime.datetime(2017, 4, 27), 'Atlanta', 'Germany', 'Munich')
# flight_df = scrape_data(datetime.datetime(2017, 4, 27), 'NYC', 'West Indies', 'Bridgetown')
# outs_df = task_3_dbscan(flight_df)
# cheap_df = task_4_dbscan(flight_df)

# flight90_df = scrape_data_90(datetime.datetime(2017, 4, 18), 'Atlanta', 'Germany', 'Berlin')
# outs90_df = task_3_dbscan(flight90_df)

# PyCharm breakpoint
2+2