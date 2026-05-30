from fastapi import FastAPI
from pydantic import BaseModel
import json
import uvicorn

app = FastAPI()

# Pydantic을 활용한 데이터 검증 모델 (오류 처리 조건 충족을 위함)
class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

# (1) GET /courses 구현
@app.get("/courses")
async def get_courses():
    # JSON 파일 읽기 (GET 요청 시 전체 데이터 반환)
    with open("courses.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# (2) POST /courses 구현
@app.post("/courses")
async def add_course(course: Course):
    # 1. 기존 데이터 읽기
    with open("courses.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 2. 새로운 과목 정보 추가 (Pydantic 모델을 딕셔너리로 변환)
    data.append(course.model_dump())
    
    # 3. 변경된 내용을 다시 파일에 덮어쓰기
    with open("courses.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    return {"message": "과목이 성공적으로 추가되었습니다.", "course": course}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)