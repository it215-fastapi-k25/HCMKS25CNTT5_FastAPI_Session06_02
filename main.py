from typing import Optional
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field

app = FastAPI(title="API quan ly hoc vien")

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18},
]

class StudentInput(BaseModel):
    code: str = Field(..., min_length=1, description="Ma hoc vien, khong duoc rong")
    name: str = Field(..., min_length=1, description="Ten hoc vien, khong duoc rong")
    email: str = Field(..., min_length=1, description="Email, khong duoc rong")
    age: int = Field(..., gt=0, description="Tuoi, phai lon hon 0")


def find_student(student_id: int):
    """Duyet list students, tim hoc vien theo id."""
    for s in students: 
        if s["id"] == student_id: 
            return s 
        
    return None 


def is_code_duplicated(code: str, exclude_id: Optional[int] = None) -> bool:
    """
    Kiem tra code da ton tai o mot hoc vien khac hay chua.
    exclude_id dung khi update, de bo qua chinh hoc vien dang sua.
    """
    return any(s["code"] == code and s["id"] != exclude_id for s in students)


def get_next_id() -> int:
    """Sinh id moi cho hoc vien, dua tren id lon nhat hien co."""
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentInput):
    """
    Them hoc vien moi.
    - code khong duoc trung -> 400 "Student code already exists"
    - name, email khong duoc rong, age > 0 -> Pydantic tu validate (422)
    """
    if is_code_duplicated(payload.code):
        raise HTTPException(status_code=400, detail="Student code already exists")

    new_student = {
        "id": get_next_id(),
        "code": payload.code,
        "name": payload.name,
        "email": payload.email,
        "age": payload.age,
    }
    students.append(new_student)
    return new_student


@app.get("/students")
def get_students(
    keyword: Optional[str] = Query(
        None, description="Tim theo name, code hoac email (khong phan biet hoa thuong)"
    ),
    min_age: Optional[int] = Query(None, description="Loc tuoi tu muc nay tro len"),
    max_age: Optional[int] = Query(None, description="Loc tuoi nho hon hoac bang muc nay"),
):
    """
    Lay danh sach hoc vien, co the ket hop tim kiem + loc cung luc:
    - keyword: tim gan dung (substring, khong phan biet hoa thuong) trong name, code hoac email.
    - min_age / max_age: loc theo khoang tuoi.
    """
    result = students

    if keyword:
        keyword_lower = keyword.lower()
        result = [
            s
            for s in result
            if keyword_lower in s["name"].lower()
            or keyword_lower in s["code"].lower()
            or keyword_lower in s["email"].lower()
        ]

    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]

    if max_age is not None:
        result = [s for s in result if s["age"] <= max_age]

    return result


@app.get("/students/{student_id}")
def get_student_detail(student_id: int):
    """Lay chi tiet 1 hoc vien theo id."""
    student = find_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/students/{student_id}")
def update_student(student_id: int, payload: StudentInput):
    """
    Cap nhat hoc vien theo id.
    - student_id phai ton tai -> 404 "Student not found"
    - code khong duoc trung voi hoc vien khac -> 400 "Student code already exists"
    """
    student = find_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if is_code_duplicated(payload.code, exclude_id=student_id):
        raise HTTPException(status_code=400, detail="Student code already exists")

    student["code"] = payload.code
    student["name"] = payload.name
    student["email"] = payload.email
    student["age"] = payload.age

    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """Xoa hoc vien theo id. Neu khong tim thay -> 404 'Student not found'."""
    for index, s in enumerate(students):
        if s["id"] == student_id:
            removed = students.pop(index)
            return {"message": "Xoa hoc vien thanh cong", "data": removed}

    raise HTTPException(status_code=404, detail="Student not found")
