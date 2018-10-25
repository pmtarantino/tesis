import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import zlib
import pdb
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

	@classmethod
	def getByGroup(self, groupID, limit=50):
		return session.query(self).filter(self.groupID == groupID).limit(limit)

	@classmethod
	def distance(self, object1, object2):
		#return abs(object1.groupID - object2.groupID)

		compress1 = zlib.compress(object1.full_string(),9)
		compress2 = zlib.compress(object2.full_string(),9)

		compressboth = zlib.compress(object1.full_string() + object2.full_string(),9)
		
		distance = float(len(compressboth) / float(len(compress1) + len(compress2)))
		return distance

engine = create_engine('mysql+mysqlconnector://root:root@localhost/tesis')
Session = sessionmaker(bind=engine)
session = Session()