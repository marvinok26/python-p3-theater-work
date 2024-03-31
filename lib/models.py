from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///auditions.db')
Base = declarative_base()

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', backref=backref('auditions', cascade='all, delete-orphan'))

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if hired_auditions:
            return hired_auditions[0]
        else:
            return 'no actor has been hired for this role'

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) > 1:
            return hired_auditions[1]
        else:
            return 'no actor has been hired for understudy for this role'

Base.metadata.create_all(engine)
