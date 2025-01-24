from http import HTTPStatus
import json
import datetime
from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate
from src.models.User import User
from src.models.Status import Status

app = FastAPI()
add_pagination(app)

users: list[User]


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> Status:
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@app.get("/api/users/", status_code=HTTPStatus.OK)
def users() -> Page[User]:
    return paginate(users)


if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    print("Users loaded")

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
