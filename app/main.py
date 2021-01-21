import string
import redis
from random import choice
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException

from .worker.celery_worker import send_email_task
from .schemas import Email, ActivateEmail
from .constants import EXPIRE_TIME, REDIS_HOST, REDIS_PORT


load_dotenv('.env')

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

app = FastAPI()


def check_activated_email(email):
    stored_emails = r.lrange('activated_emails', 0, -1)

    for stored_email in stored_emails:
        if email == stored_email.decode('utf-8'):
            raise HTTPException(status_code=400, detail={'error': 'Email already activated'})


@app.post("/generate-code")
async def generate_code(payload: Email):
    email = payload.email

    check_activated_email(email)

    chars = string.digits
    generated_code = ''.join(choice(chars) for _ in range(4))
    r.set(email, generated_code, ex=EXPIRE_TIME)

    send_email_task.delay(generated_code, email)

    return JSONResponse(status_code=200, content={'message': 'Code was sent on email'})


@app.post('/activate-email')
async def activate_email(payload: ActivateEmail):
    email = payload.email
    code = payload.code

    check_activated_email(email)

    if not r.exists(email):
        return HTTPException(status_code=400, detail={'error': 'Email does not exist'})

    stored_code = r.get(email).decode("utf-8")
    if code != stored_code:
        return HTTPException(status_code=400, detail={'error': 'Your code does not match the stored value'})

    r.lpush('activated_emails', email)
    r.delete(email)

    return JSONResponse(status_code=200, content={'message': 'Email activated'})
