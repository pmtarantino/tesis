import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Data(Base):
	__tablename__ = 'data'
	id = Column(Integer, primary_key=True)
	hla = Column(String)
	pep = Column(String)
	alpha = Column(String)
	beta = Column(String)
	groupID = Column(Integer)

	@classmethod
	def getByGroup(self, groupID):
		return session.query(self).filter(self.groupID == groupID)

engine = create_engine('mysql+mysqlconnector://root:root@localhost/tesis')
Session = sessionmaker(bind=engine)
session = Session()