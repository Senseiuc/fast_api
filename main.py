# main.py
from typing import Optional
from fastapi import FastAPI
from student import Student as Stud
from pydantic import BaseModel
from database import Database
import uvicorn

app = FastAPI()
storage = Database()
storage.reload()


class Student(BaseModel):
    name: str
    audio: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    audio: Optional[str] = None


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "Success"}


@app.get("/get-students")
async def get_students() -> dict:
    return storage.get(Stud)


@app.get("/get-student/{student_id}")
async def get_student(student_id: int) -> dict:
    return storage.get(Stud, student_id)


# @app.get("/get-by-name")
# async def get_student(*, name: Optional[str] = None) -> dict:
#     for std in storage.get(ST):
#         if students[std]["name"] == name:
#             return students[std]
#     return {"data": "Not Found"}


@app.post("/create-student/{student_id}")
async def create_student(student_id: int, student: dict):
    if storage.get(Stud, student_id) is not None:
        return {'Error': 'student exists'}
    instance = Stud(student_id, **student)
    storage.new(instance)
    storage.save()
    return {'data': instance.__dict__, 'message': 'successfully created student'}


# @app.put('/update-student/{student_id}')
# async def update_student(student_id: int, student: UpdateStudent):
#     if student_id not in students:
#         return {'Error': 'Not a student'}
#     s_t_b_u = students[student_id]
#     if student.name is not None:
#         s_t_b_u.name = student.name
#     if student.age is not None:
#         s_t_b_u.age = student.age
#     if student.year is not None:
#         s_t_b_u.year = student.year
#     return students[student_id]
#
#
# @app.delete('/delete-student/{student_id}')
# async def delete_student(student_id: int):
#     if student_id not in students:
#         return {'Error': 'student does not exist'}
#     del students[student_id]
#     return {'Message': 'student successfully deleted'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
