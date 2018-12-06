from db_models import Data, session
import random
import zlib
import pdb
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import pylzma
import bz2

groups_number = 12
groups = range(1,groups_number+1)

means = []
std = []
ind = []

from itertools import groupby
def compress(string):
    return bz2.compress(string)

for i in groups:
	prom = []

	for j in range(0,500):
		dirichlet = np.random.dirichlet(np.ones(i),size=1)
		limits = (dirichlet*100)[0]
		
		sample_groups = random.sample(groups, i)
		long_string = ''

		group_order = 0

		for g in sample_groups:
		
			data_rows = Data.getByGroup(g, limit=int(limits[group_order]) )
			for data_row in data_rows:
				long_string = str(long_string) + str(data_row.full_string())
		
			group_order = group_order+1

		valor = len(compress(long_string))
		prom.append(valor)

	print {'index': i, 'median': np.median(prom), 'sdv': np.std(prom)}
	ind.append(i)
 	means.append(np.median(prom))
 	std.append(np.std(prom))


width = 0.35       # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(ind, means, width, color='r', yerr=std)
plt.xscale('log')
plt.show()