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


history_id = 0


def ServerDelay():
    delay = random.uniform(0, 2)
    print(f"서버가 {delay}초 뒤에 응답합니다.")
    time.sleep(delay)


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


class HistoryEntity(BaseModel):
    year: int
    month: int
    content: str
    

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
