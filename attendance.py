from sqlalchemy import Column, Integer, String
from base_model import Base, BaseModel


class Attendance(Base, BaseModel):
    __tablename__: str = 'attendance'

    student_id = Column(Integer)
    course_code = Column(String(128), nullable=False)

    @property
    def __repr__(self):
        return "<Attendance(id='%s' student_id='%s', course_code='%s')>" % (
            self.id, self.student_id, self.course_code)


# student = Attendance
# print(student.__dict__)
