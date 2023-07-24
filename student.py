from sqlalchemy import Column, String, JSON
from base_model import Base, BaseModel


class Student(BaseModel, Base):
    __tablename__ = 'students'

    name = Column(String(128), nullable=False)
    audio = Column(JSON)

    def __repr__(self):
        return "<Student(id='%s' name='%s', audio='%s')>" % (self.id, self.name, self.audio)


# student = Student(name='john')
# print(student)
