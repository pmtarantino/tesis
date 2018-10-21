print(__doc__)
import pdb
from db_models import Data, session

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs


objects = []
labels_true = []

for groupID in range(1,3):
	groups = Data.getByGroup(groupID)
	for data_row in groups:
		objects.append(data_row)
		labels_true.append(data_row.groupID)

dist = lambda p1, p2: Data.distance(p1,p2)
X = np.asarray([[dist(p1, p2) for p2 in objects] for p1 in objects])

labels_true = np.array(labels_true)

X = StandardScaler().fit_transform(X)

# #############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(X, quantile=0.4, n_samples=len(X))

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, metric='precomputed')
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()