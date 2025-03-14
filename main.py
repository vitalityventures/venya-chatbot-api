import openai
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return JSONResponse(content={"message": "API is working!"})

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant for Venya MedSpa."},
                {"role": "user", "content": request.question}
            ],
            api_key=os.getenv("OPENAI_API_KEY")
        )
        return JSONResponse(content={"response": response["choices"][0]["message"]["content"]})
    
    except openai.error.OpenAIError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

