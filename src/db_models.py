import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import zlib
import pdb
from  sqlalchemy.sql.expression import func, select
from random import shuffle

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compress_distance(a, b, opt=9):
	compress1 = zlib.compress(a,opt)
	compress2 = zlib.compress(b,opt)

	compressboth = zlib.compress(a + b,opt)
	
	return float(len(compressboth) / float(len(compress1) + len(compress2)))


Base = declarative_base()

class Data(Base):
	__tablename__ = 'data'
	id = Column(Integer, primary_key=True)
	hla = Column(String)
	pep = Column(String)
	alpha = Column(String)
	beta = Column(String)
	groupID = Column(Integer)

	def full_string(self):
		return self.alpha + self.beta

	def resorted(self):
		s = self.alpha + self.beta
		rango = list(range(len(s)-1))
		shuffle(rango)
		return (''.join([s[i] for i in rango]))

	def to_int_list(self):
		ints = []
		for i in range(0,30):
			ints.append(ord(self.alpha[i]))
		for i in range(0,30):
			ints.append(ord(self.beta[i]))
		return ints

	@classmethod
	def getByGroup(self, groupID, limit=30):
		return session.query(self).filter(self.groupID == groupID).order_by(func.rand()).limit(limit)

	@classmethod
	def distance(self, object1, object2):

		return compress_distance(object1.alpha, object2.alpha) + compress_distance(object1.beta, object2.beta)

	@classmethod
	def getRandom(self, limit=1):
		return session.query(self).order_by(func.rand()).limit(limit)

engine = create_engine('mysql+mysqlconnector://root:root@localhost/tesis')
Session = sessionmaker(bind=engine)
session = Session()