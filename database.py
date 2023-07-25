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
        :return: returns a dict of the object
        """
        if obj_id is not None:
            obj = self.__session.query(cls).filter_by(id=obj_id).first()
            if obj is not None:
                return object_as_dict(obj)
            return obj
        obj_dictionary = {}
        for obj in self.__session.query(cls):
            obj_dictionary[obj.id] = object_as_dict(obj)
        return obj_dictionary

    def update(self, cls: [Student, Attendance], obj_id: int, **kwargs):
        """
        Updates an Object
        :param cls: The class of the object to be updated
        :param obj_id: The id of the object to be updated
        :param kwargs: The attributes to be updated
        :return: A dict of the object
        """
        obj = self.__session.query(cls).filter_by(id=obj_id).first()
        if obj is not None:
            for key, value in kwargs.items():
                setattr(obj, key, value)
        self.save()
        return object_as_dict(obj)

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

    # def close(self):
    #     """call remove() method on the private session attribute"""
    #     self.__session.remove()
