import os
import string
import redis
import json
from random import choice
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from .worker.celery_worker import send_email_task
from .schemas import Email, ActivateEmail
from .constants import EXPIRE_TIME, REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)


def check_activated_email(email):
    with open('emails.json', 'r') as f:
        stored_emails = json.load(f).get('emails')

        for stored_email in stored_emails:
            if email == stored_email:
                raise HTTPException(status_code=400, detail={'error': 'Email already activated'})


@app.on_event("startup")
async def startup_event():
    if not os.path.exists('emails.json'):
        with open('emails.json', 'w+') as f:
            json.dump({'emails': []}, f)


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

    with open('emails.json', 'r') as read_f:
        parsed_data = json.load(read_f)
        emails = parsed_data['emails']
        emails.append(email)

        with open('emails.json', 'w') as write_f:
            json.dump(parsed_data, write_f)

    r.delete(email)

    return JSONResponse(status_code=200, content={'message': 'Email activated'})
