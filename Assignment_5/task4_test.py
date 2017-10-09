import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

'''panda = pd.read_csv('flights.csv')
df = pd.DataFrame(panda, columns=['Day', 'Price'])
scaler = MinMaxScaler()
X = scaler.fit_transform(df)

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
plt.savefig('task_3_dbscan.png')
df['Labels'] = db.labels_

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
        sorted_prices = sorted([xform(x)[1] for x in cluster])
    if max(sorted_prices) - min(sorted_prices) <= 20:
        if [(abs(sorted_prices[k] - sorted_prices[k+1]) < 20) for k in range(len(sorted_prices)-1)]:
            cluster_list.append(cluster)
if cluster_list:
    if len(cluster_list) > 1:
        for clustr in cluster_list:
            total.append(sum(p[1] for p in xform(clustr)))
        min_index = total.index(min(total))
        chpst = cluster_list[min_index]
    elif len(cluster_list) == 1:
        chpst = cluster_list[0]
    target = xform(chpst)
else:
    print "No clusters satisfy the conditions set."
    
df = pd.DataFrame(clean_data, columns=['Day', 'Price'])
    return df'''


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

    def xform(array):
        day_price = scaler.inverse_transform(array)
        return day_price

    total = []
    cluster_list = []
    for i in range(len(cluster_means)):
        cluster = X[labels == i]
        if len(cluster) >= 5:
            for point in cluster:
                # some euclidean computation for epsilon, y & x goes here
                if point:
                    pass
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


panda = pd.read_csv('Munich.csv')
df = pd.DataFrame(panda, columns=['Day', 'Price'])
flight_df = task_4_dbscan(df)

2+2