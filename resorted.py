from db_models import Data, session
import random
import zlib
import pdb
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math

groups_number = 12
groups = range(1,groups_number+1)

for i in groups:
	# Por cada cantidad de grupos, lo corro 500 veces
	prom = []
	limit = int(100/i)

	for j in range(0,250):
		sample_groups = random.sample(groups, i)
		long_string = ''

		for g in sample_groups:
			data_rows = Data.getByGroup(g, limit=limit)
			for data_row in data_rows:
				long_string = str(long_string) + str(data_row.resorted())

		valor = len(zlib.compress(long_string, 9))
		prom.append(valor)

	print {'index': i, 'median': np.median(prom), 'sdv': np.std(prom)}