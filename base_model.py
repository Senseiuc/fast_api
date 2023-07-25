from datetime import datetime
from sqlalchemy import DateTime, Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, student_id: int, **kwargs):
        """
        Initialising the storage class
        :param kwargs: Arguments with names
        """
        """Initialization of the base model"""
        self.id = student_id
        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)
        if kwargs.get("created_at", None) and type(self.created_at) is str:
            self.created_at = datetime.strptime(kwargs["created_at"], time)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get("updated_at", None) and type(self.updated_at) is str:
            self.updated_at = datetime.strptime(kwargs["updated_at"], time)
        else:
            self.updated_at = datetime.utcnow()
