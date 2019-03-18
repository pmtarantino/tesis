from datamanager import DataManager
from groupcounter import GroupCounter

dm = DataManager([2,6,7,8,9],[1,3,4,5,10,11,12])

gc = GroupCounter(dm)

gc.train()

print(gc.model_evaluation())

#(
#   {
#     'means': [4159.5, 4737.0, 4920.0, 5095.5, 5189.0],
#     'std': [419.74810915119076, 435.4999105212308, 361.5791447249136, 330.22057643338945, 262.9617585201316],
#     'spearman': SpearmanrResult(correlation=0.9999999999999999, pvalue=1.4042654220543672e-24),
#     'pearson': (0.9373180928175989, 0.018660407588632036),
#     'logValues': [635.8317568307905, 4211.3921428748],
#     'mse': 0.04213468400108587
#   },
#   {
#     'means': [3838.5, 4123.5, 4254.5, 4350.0, 4392.5, 4448.0, 4452.5],
#     'std': [253.59445775489652, 226.12029156181453, 184.76256876326437, 175.13453507518156, 175.10969677319414, 166.04081053765066, 161.30804761077482],
#     'spearman': SpearmanrResult(correlation=1.0, pvalue=0.0),
#     'pearson': (0.9160537876569391, 0.0037466309782821653),
#     'logValues': [320.0927760686305, 3875.808204786221],
#     'mse': 0.16502486587983475
#   }
# )