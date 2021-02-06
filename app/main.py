import os
import string
import redis
from random import choice
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import EmailStr
from fastapi.responses import FileResponse

from .worker.celery_worker import send_email_task
from .utils import ActivateEmail, Login, check_activated_email
from .constants import (EXPIRE_TIME, REDIS_HOST, REDIS_PORT,
                        ADMIN_USERNAME, ADMIN_PASSWORD, ALLOW_ORIGINS)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    if not os.path.exists('emails.txt'):
        with open('emails.txt', 'w+') as f:
            pass


@app.get("/generate-code")
async def generate_code(email: EmailStr):
    check_activated_email(email)
    chars = string.digits
    generated_code = ''.join(choice(chars) for _ in range(4))

    stored_limit = r.hget(email, 'limit')

    if stored_limit:
        stored_limit = int(stored_limit.decode('utf-8'))
        if stored_limit >= 2:
            raise HTTPException(status_code=400, detail={'error': 'You can not send code more than two times'})
        else:
            r.hmset(email, {'code': generated_code, 'limit': 2})
    else:
        r.hmset(email, {'code': generated_code, 'limit': 1})

    r.expire(email, EXPIRE_TIME)
    send_email_task.delay(generated_code, email)

    return JSONResponse(status_code=200, content={'message': 'Code was sent on email'})


@app.post('/activate-email')
async def activate_email(payload: ActivateEmail):
    email = payload.email
    platform = payload.platform
    name = payload.name
    code = payload.code
    check_activated_email(email)

    if not r.exists(email):
        return HTTPException(status_code=400, detail={'error': 'Email for activation does not exist'})

    stored_code = r.hget(email, 'code').decode('utf-8')
    if code != stored_code:
        return HTTPException(status_code=400, detail={'error': 'Your code does not match the stored value'})

    with open('emails.txt', 'a') as f:
        f.write(f"{email}\t{platform}\t{name}\n")

    r.delete(email)

    return JSONResponse(status_code=200, content={'message': 'Email activated successfully'})


@app.post('/load-emails')
async def load_emails(payload: Login):
    if payload.username != ADMIN_USERNAME or payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail={'error': 'Invalid credentials'})

    return FileResponse('emails.txt')

