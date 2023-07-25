from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from student import Student as Stud
from database import Database
import uvicorn

app = FastAPI()
storage = Database()
storage.reload()


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "Success"}


@app.get("/get-students")
async def get_students() -> dict:
    return storage.get(Stud)


@app.get("/get-student/{student_id}")
async def get_student(student_id: int) -> dict | None:
    stud = storage.get(Stud, student_id)
    if stud is None:
        return {'Error': 'Student does not exist'}
    return stud


class Student(BaseModel):
    name: str


# @app.get("/get-by-name")
# async def get_student(*, name: Optional[str] = None) -> dict:
#     for std in storage.get(ST):
#         if students[std]["name"] == name:
#             return students[std]
#     return {"data": "Not Found"}


@app.post("/create-student/{student_id}")
async def create_student(student_id: int, student: Student):
    if storage.get(Stud, student_id) is not None:
        return {'Error': 'student exists'}
    instance = Stud(student_id, name=student.name)
    storage.new(instance)
    storage.save()
    return {'data': instance.__dict__, 'message': 'successfully created student'}


@app.post("/add-audio/{student_id}")
async def add_audio(student_id: int, audio: UploadFile):
    if storage.get(Stud, student_id) is None:
        return {'Error': 'student does not exists'}
    # data = audio.file.read()
    print(audio.__dict__)
    instance = storage.update(Stud, student_id, audio=audio.filename)
    return {'data': instance, 'message': 'audio successfully added'}

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
