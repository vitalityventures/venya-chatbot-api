import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        return JSONResponse(content={"message": "API is working!", "api_key": "Key found!"})
    else:
        return JSONResponse(content={"message": "API is working!", "api_key": "Key NOT found!"})
