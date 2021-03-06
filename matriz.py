import pdb
from db_models import Data, session

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
import zlib
import random
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

objects = []
labels_true = []

groups_number = 12
groups = range(1,groups_number+1)
groups = [1,3,4,5,10,11,12,2,6,7,8,9]

for groupID in groups:
	groups = Data.getByGroup(groupID)
	for data_row in groups:
		objects.append(data_row)
		labels_true.append(data_row.groupID)

dist = lambda p1, p2: Data.distance(p1,p2)
X = np.asarray([[dist(p1, p2) for p2 in objects] for p1 in objects])

f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(X)
plt.show()