from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UpdateUser
from uuid import uuid4,UUID
from typing import List
import uvicorn


app = FastAPI()

db: List[User] = [
    User(
        id=UUID("aec72dd9-6ec9-43c0-9a20-a7a25afc7328"), 
        first_name="Luis",
        last_name="Camacho",
        middle_name="Fernando",
        gender=Gender.male,
        roles=[Role.admin]
    ),
    User(
        id=UUID("fd0f4426-7b06-4894-8e1f-8535ad11064e"), 
        first_name="JC", 
        last_name="Camacho",
        gender=Gender.male,
        roles=[Role.student]
    ),
]


@app.get('/')
async def root():
    return {"Hello": "World"}


@app.get('/api/v1/users')
async def fetch_users():
    print(uuid4())
    return db


@app.post('/api/v1/users')
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.put('/api/v1/users/{user_id}')
async def update_user(user_update: UpdateUser, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return {"message": f"User with id: {user_id} was updated"}
    
    raise HTTPException(
        status_code=404,
        detail= f"User with id: {user_id} does not exist."
    )

@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": f"User with id: {user_id} deleted"}
    
    raise HTTPException(
        status_code=404,
        detail= f"User with id: {user_id} does not exist."
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    
    