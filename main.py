# main.py
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12"
    },
    2: {
        "name": "James",
        "age": 23,
        "year": "year 12"
    }
}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "Success"}


@app.get("/get-students")
async def get_students() -> dict:
    return students


@app.get("/get-student/{student_id}")
async def get_student(student_id: int) -> Student | None:
    return students.get(student_id)


@app.get("/get-by-name")
async def get_student(*, name: Optional[str] = None) -> dict:
    for std in students:
        if students[std]["name"] == name:
            return students[std]
    return {"data": "Not Found"}


@app.post("/create-student/{student_id}")
async def create_student(student_id: int, student: Student):
    if student_id in students:
        return {'Error': 'student exists'}
    students[student_id] = student
    return students[student_id]


@app.put('/update-student/{student_id}')
async def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {'Error': 'Not a student'}
    s_t_b_u = students[student_id]
    if student.name is not None:
        s_t_b_u.name = student.name
    if student.age is not None:
        s_t_b_u.age = student.age
    if student.year is not None:
        s_t_b_u.year = student.year
    return students[student_id]


@app.delete('/delete-student/{student_id}')
async def delete_student(student_id: int):
    if student_id not in students:
        return {'Error': 'student does not exist'}
    del students[student_id]
    return {'Message': 'student successfully deleted'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
