import bz2
import numpy as np
import random
from db_models import Data, session
import scipy.stats as stats
import math

class GroupCounter(object):

    def __init__(self, dm, encoder=lambda x: x):
        self.dm = dm
        self.encoder = encoder
        self.evaluation = {}
        self.evaluation[1] = {}
        self.evaluation[2] = {}

    def test(self, a):
        return self.encoder(a)

    def compressString(self, string):
        return bz2.compress(bytes(string, 'utf-8'))

    def compressGroup(self, group):

        groups = self.dm.getGroup(group)

        means = []
        std = []
        ind = []

        for key, i in enumerate(groups):
            key = key+1
            prom = []

            for j in range(0,500):

                dirichlet = np.random.dirichlet(np.ones(key),size=1)
                limits = (dirichlet*100)[0]
                
                sample_groups = random.sample(groups, key)
                long_string = ''

                group_order = 0

                for g in sample_groups:
                
                    data_rows = Data.getByGroup(g, limit=int(limits[group_order]) )

                    for data_row in data_rows:
                        long_string = str(long_string) + str(self.encoder(data_row.full_string()))
                
                    group_order = group_order+1

                valor = len(self.compressString(long_string))
                prom.append(valor)

            ind.append(key)
            means.append(np.median(prom))
            std.append(np.std(prom))

        spearman = stats.spearmanr(ind, means)
        pearson = stats.pearsonr(ind, means)
        logValues = np.polyfit(np.log(ind), means, 1)

        self.evaluation[group] = {
            'means' : means,
            'std' : std,
            'spearman' : spearman,
            'pearson' : pearson,
            'logValues' : logValues.tolist()
        }

        self.evaluation[group]['mse'] = self._mse(group)


    def _mse(self, groupId):
        n = 0
        total = 0
        for group, mean in enumerate(self.evaluation[groupId]['means']):
            group = group+1
            total = total + math.pow(self._aprox(mean, groupId)-group, 2)
            n = n+1
        return total/n

    def train(self):
        self.compressGroup(1)
        self.compressGroup(2)

    def model_evaluation(self):
        return (self.evaluation[1], self.evaluation[2])

    def _e(self, x, a, b):
        return math.exp((x-b)/a)

    def _aprox(self, x, groupId):
        a = self.evaluation[groupId]['logValues'][0]
        b = self.evaluation[groupId]['logValues'][1]
        return self._e(x, a, b)

    def _expected(self, groupId, groups):
        return self.evaluation[groupId]['means'][groups]
