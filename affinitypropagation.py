print(__doc__)
import pdb
from db_models import Data, session

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import AffinityPropagation

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
# Compute Affinity Propagation
af = AffinityPropagation(preference=1,affinity='precomputed').fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
    for x in X[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()