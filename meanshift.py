print(__doc__)
import pdb
from db_models import Data, session

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs

def stringToFloat(old_string):
	numbers = []
	for letter in old_string:
	  numbers.append(str(ord(letter)))

	string = ''.join(numbers)
	return float(string)/(pow(10,(len(string)-1)))

X = []
labels_true = []

for groupID in [1,2]:
	groups = Data.getByGroup(groupID)
	for data_row in groups:
		X.append([stringToFloat(data_row.alpha), stringToFloat(data_row.beta)])
		labels_true.append(groupID)

X = np.array(X)
print len(X)
labels_true = np.array(labels_true)

# #############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(X, quantile=0.4, n_samples=len(X))

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
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