# heatmap distancias
# tratar de identificar grupos mas que nada

import pdb
from db_models import Data, session

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
import zlib
import random

objects = []
labels_true = []

groups_number = 3

for groupID in range(1,groups_number+1):
	groups = Data.getByGroup(groupID)
	for data_row in groups:
		objects.append(data_row)
		labels_true.append(data_row.groupID)

dist = lambda p1, p2: Data.distance(p1,p2)
X = np.asarray([[dist(p1, p2) for p2 in objects] for p1 in objects])
pdb.set_trace()
labels_true = np.array(labels_true)

db = DBSCAN(metric="precomputed", eps=0.7).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
			% metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
			% metrics.adjusted_mutual_info_score(labels_true, labels))

# #############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
					for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
		if k == -1:
				# Black used for noise.
				col = [0, 0, 0, 1]

		class_member_mask = (labels == k)

		xy = X[class_member_mask & core_samples_mask]
		plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
						 markeredgecolor='k', markersize=14)

		xy = X[class_member_mask & ~core_samples_mask]
		plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
						 markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()