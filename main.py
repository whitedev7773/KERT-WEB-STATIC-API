from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import random
import asyncio
from typing import List

app = FastAPI()

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

# await ServerDelay()로 사용
async def ServerDelay(delay=random.uniform(1, 3)):
    print(f"서버가 {round(delay, 3)}초 뒤에 응답합니다.")
    await asyncio.sleep(delay)  # Intentional delay of 1 second

def UpdateEntity(target: BaseModel, new: BaseModel):
    for key, value in new.dict().items():
        if hasattr(target, key):
            setattr(target, key, value)

# Models
class Admin(BaseModel):
    student_id: int
    generation: str
    role: str
    description: Optional[str] = datetime.now()

class User(BaseModel):
    student_id: int
    name: str
    email: str
    profile_picture: Optional[str] = None
    generation: str
    major: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

class Post(BaseModel):
    id: int
    title: str
    tag: str
    content: str
    admin_id: int
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

class Password(BaseModel):
    user_id: int
    hash: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

class History(BaseModel):
    id: int
    year: int
    month: int
    description: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

# In-memory data storage
admins = []
users = [
    User(
        student_id=2024005056,
        name="장기원",
        email="w.developer7773@gmail.com",
        profile_picture="https://github.com/whitedev7773.png",
        generation="2024.1",
        major="컴퓨터학부 플랫폼SW/데이터전공"
    ),
    User(
        student_id=2024005057,
        name="장기원",
        email="w.developer7773@gmail.com",
        profile_picture="https://github.com/whitedev7773.png",
        generation="2024.1",
        major="컴퓨터학부 플랫폼SW/데이터전공"
    ),
    User(
        student_id=2024005058,
        name="장기원",
        email="w.developer7773@gmail.com",
        profile_picture="https://github.com/whitedev7773.png",
        generation="2024.1",
        major="컴퓨터학부 플랫폼SW/데이터전공"
    ),
    User(
        student_id=2024005059,
        name="장기원",
        email="w.developer7773@gmail.com",
        profile_picture="https://github.com/whitedev7773.png",
        generation="2024.1",
        major="컴퓨터학부 플랫폼SW/데이터전공"
    ),
]
posts = []
comments = []
passwords = []
histories = []

# Helper functions
def find_item_by_id(collection, item_id, id_field='id'):
    return next((item for item in collection if getattr(item, id_field) == item_id), None)

# CRUD for Admin
@app.post("/admin", response_model=Admin)
async def create_admin(admin: Admin):
    await ServerDelay()
    user = find_item_by_id(users, admin.student_id, id_field='student_id')
    if user:
        admins.append(admin)
        return admin
    raise HTTPException(status_code=404, detail="Target User not found")

@app.get("/admin", response_model=List[Admin])
async def get_all_admin():
    await ServerDelay()
    return admins

@app.get("/admin/{student_id}", response_model=Admin)
async def get_admin(student_id: int):
    await ServerDelay()
    admin = find_item_by_id(admins, student_id, id_field='student_id')
    if admin:
        return admin
    raise HTTPException(status_code=404, detail="Admin not found")

@app.put("/admin/{student_id}", response_model=Admin)
async def update_admin(student_id: int, updated_admin: Admin):
    await ServerDelay()
    admin = find_item_by_id(admins, student_id, id_field='student_id')
    if admin:
        admin = UpdateEntity(admin, updated_admin)
        # admins.remove(admin)
        # admins.append(updated_admin)
        return updated_admin
    raise HTTPException(status_code=404, detail="Admin not found")

@app.delete("/admin/{student_id}")
async def delete_admin(student_id: int):
    await ServerDelay()
    admin = find_item_by_id(admins, student_id, id_field='student_id')
    if admin:
        admins.remove(admin)
        return {"message": "Admin deleted successfully"}
    raise HTTPException(status_code=404, detail="Admin not found")

# CRUD for User
@app.post("/users", response_model=User)
async def create_user(user: User):
    await ServerDelay()
    users.append(user)
    return user

@app.get("/users", response_model=List[User])
async def get_all_user():
    await ServerDelay()
    return users

@app.get("/users/{student_id}", response_model=User)
async def get_user(student_id: int):
    await ServerDelay()
    user = find_item_by_id(users, student_id, id_field='student_id')
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{student_id}", response_model=User)
async def update_user(student_id: int, updated_user: User):
    await ServerDelay()
    user = find_item_by_id(users, student_id, id_field='student_id')
    if user:
        updated_user.updated_at = datetime.now()
        user = UpdateEntity(user, updated_user)
        # users.remove(user)
        # users.append(updated_user)
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{student_id}")
async def delete_user(student_id: int):
    await ServerDelay()
    user = find_item_by_id(users, student_id, id_field='student_id')
    if user:
        users.remove(user)
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# CRUD for Post
@app.post("/posts", response_model=Post)
async def create_post(post: Post):
    await ServerDelay()
    posts.append(post)
    return post

@app.get("/posts", response_model=List[Post])
async def get_post(id: int):
    await ServerDelay()
    return posts

@app.get("/posts/{id}", response_model=Post)
async def get_post(id: int):
    await ServerDelay()
    post = find_item_by_id(posts, id)
    if post:
        return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{id}", response_model=Post)
async def update_post(id: int, updated_post: Post):
    await ServerDelay()
    post = find_item_by_id(posts, id)
    if post:
        updated_post.updated_at = datetime.now()
        post = UpdateEntity(post, update_post)
        # posts.remove(post)
        # posts.append(updated_post)
        return updated_post
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{id}")
async def delete_post(id: int):
    await ServerDelay()
    post = find_item_by_id(posts, id)
    if post:
        posts.remove(post)
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

# CRUD for History
@app.post("/histories", response_model=History)
async def create_history(history: History):
    await ServerDelay()
    histories.append(history)
    return history

@app.get("/histories", response_model=List[History])
async def get_history(id: int):
    await ServerDelay()
    return histories

@app.get("/histories/{id}", response_model=History)
async def get_history(id: int):
    await ServerDelay()
    history = find_item_by_id(histories, id)
    if history:
        return history
    raise HTTPException(status_code=404, detail="History not found")

@app.put("/histories/{id}", response_model=History)
async def update_history(id: int, updated_history: History):
    await ServerDelay()
    history = find_item_by_id(histories, id)
    if history:
        updated_history.updated_at = datetime.now()
        history = UpdateEntity(history, updated_history)
        # histories.remove(history)
        # histories.append(updated_history)
        return updated_history
    raise HTTPException(status_code=404, detail="History not found")

@app.delete("/histories/{id}")
async def delete_history(id: int):
    await ServerDelay()
    history = find_item_by_id(histories, id)
    if history:
        histories.remove(history)
        return {"message": "History deleted successfully"}
    raise HTTPException(status_code=404, detail="History not found")
