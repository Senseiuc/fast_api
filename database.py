from typing import Optional

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

from attendance import Attendance
from base_model import Base
from env import user, password, db, host
from student import Student


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class Database:
    __engine = None
    __session = None

    def __init__(self):
        """
        Instantiate a db storage object
        """
        connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{db}"
        self.__engine = create_engine(connection_string, echo=True)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(sess_factory)
        self.__session = session

    def get(self, cls: [Student, Attendance], obj_id: Optional[int] = None) -> [Student, Attendance]:
        """
        Gets an object using the class and the id
        :param cls: the class of the object
        :param obj_id: the object id
        :return: returns an object
        """
        if obj_id is not None:
            stud = self.__session.query(cls).filter_by(id=obj_id).first()
            if stud is not None:
                return object_as_dict(stud)
            return stud
        stud_dictionary = {}
        for stud in self.__session.query(cls):
            stud_dictionary[stud.id] = object_as_dict(stud)
        return stud_dictionary

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
