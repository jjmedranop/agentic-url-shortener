from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string
import random

app = FastAPI(title="URL Shortener Service")
db = {} # In-memory database simulation

class URLPayload(BaseModel):
    long_url: str

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@post("/shorten")
def shorten_url(payload: URLPayload):
    code = generate_code()
    db[code] = payload.long_url
    return {"short_url": f"http://localhost:8000/{code}", "code": code}

@get("/{code}")
def redirect_url(code: str):
    url = db.get(code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"redirect_to": url}
