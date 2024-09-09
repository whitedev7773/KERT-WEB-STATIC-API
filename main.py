import time
import random
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # cross-origin request에서 cookie를 포함할 것인지 (default=False)
    allow_methods=["*"],     # cross-origin request에서 허용할 method들을 나타냄. (default=['GET']
    allow_headers=["*"],     # cross-origin request에서 허용할 HTTP Header 목록
)


def ServerDelay(delay=random.uniform(1, 3)):
    # delay = 3
    print(f"서버가 {delay}초 뒤에 응답합니다.")
    time.sleep(delay)

# 연혁 ===================================================================================================
# ========================================================================================================
history_id = 0

class HistoryEntity(BaseModel):
    year: int
    month: int
    content: str

def GenerateHistories(year: int, month: int, content: str):
    global history_id
    history = {
        "id": history_id,
        "year": year,
        "month": month,
        "content": content,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    history_id += 1
    return history


sampleHistoryData = [
    GenerateHistories(2021, 9, "제2회 KOSPO 웹서비스 정보보안 경진대회 최우수상"),
    GenerateHistories(2023, 4, "전국사이버보안연합 cca 소속"),
    GenerateHistories(2019, 4, "전국사이버보안연합 cca 소속"),
    GenerateHistories(2019, 5, "정보보호대학동아리연합 KUCIS 소속"),
    GenerateHistories(2024, 6, "정보보호대학동아리연합 KUCIS 소속"),
    GenerateHistories(2015, 7, "정보보호대학동아리연합 KUCIS 소속"),
    GenerateHistories(2015, 8, "정보보호대학동아리연합 KUCIS 소속"),
    GenerateHistories(2015, 9, "정보보호대학동아리연합 KUCIS 소속"),
    GenerateHistories(2024, 10, "정보보호대학동아리연합 KUCIS 소속"),
    GenerateHistories(2024, 11, "정보보호대학동아리연합 KUCIS 소속")
]


@app.get("/histories")
async def return_all_histories():
    ServerDelay()
    return sampleHistoryData
    

@app.post("/histories")
async def add_history(res: HistoryEntity):
    global sampleHistoryData

    ServerDelay()
    newHistory = GenerateHistories(res.year, res.month, res.content)
    sampleHistoryData.append(newHistory)
    return newHistory


@app.delete("/histories/{id}")
async def delete_history(id: int):
    global sampleHistoryData

    ServerDelay()
    sampleHistoryData = [history for history in sampleHistoryData if history["id"] != id]
    return sampleHistoryData
# ========================================================================================================



# 관리자 =================================================================================================
# ========================================================================================================
class AdminEntity(BaseModel):
    student_id: str
    generation: int
    role: str
    description: str

class AdminUpdateEntity(BaseModel):
    generation: int
    role: str
    description: str

def GenerateAdmin(student_id: str, generation: int, role: str, description: str):
    admin = {
        "student_id": student_id,  
        "generation": generation, 
        "role": role,
        "description": description,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    return admin


sampleAdminList = [
    GenerateAdmin("2020000000", 20, "최고 관리자", "최고 관리자임 ㅇㅇ"),
    GenerateAdmin("2021000000", 21, "기술 관리자", "기술 관리자임 ㅇㅇ"),
    GenerateAdmin("2022000000", 22, "홍보 관리자", "홍보 관리자임 ㅇㅇ"),
    GenerateAdmin("2023000000", 23, "학술 관리자", "학술 관리자임 ㅇㅇ"),
    GenerateAdmin("2024000000", 24, "운영 관리자", "운영 관리자임 ㅇㅇ"),
    GenerateAdmin("2025000000", 25, "대외 관리자", "대외 관리자임 ㅇㅇ"),
    GenerateAdmin("2030000000", 30, "기타 관리자", "그냥 의미없는 관리자임 ㅇㅇ")
]

@app.get("/admin")
async def return_all_admins():
    ServerDelay()
    return sampleAdminList
    
@app.post("/admin")
async def add_admin(res: AdminEntity):
    global sampleAdminList

    ServerDelay()
    newAdmin = GenerateAdmin(res.student_id, res.generation, res.role, res.description)
    sampleAdminList.append(newAdmin)
    return newAdmin

@app.put("/admin/{student_id}")
async def update_admin(student_id: str, res: AdminUpdateEntity):
    for admin in sampleAdminList:
        if admin['student_id'] == student_id:
            if res.generation is not None:
                admin['generation'] = res.generation
            if res.role is not None:
                admin['role'] = res.role
            if res.description is not None:
                admin['description'] = res.description
            admin['updated_at'] = datetime.now()
            return admin
    return None  # 해당 student_id가 없을 경우

@app.delete("/admin/{student_id}")
async def delete_admin(student_id: str):
    global sampleAdminList

    ServerDelay()
    sampleAdminList = [admin for admin in sampleAdminList if admin["student_id"] != student_id]
    return sampleAdminList
# ========================================================================================================