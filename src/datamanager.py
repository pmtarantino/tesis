from db_models import Data, session

class DataManager(object):

	def __init__(self, groupId1, groupId2):
		self.group1 = groupId1
		self.group2 = groupId2

	def getGroup(self, id):
		if id == 1:
			return self.group1
		else:
			return self.group2