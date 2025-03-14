from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Initialize FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working!"}

# Set your OpenAI API key (you’ll replace this in Vercel later)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

venya_data = {
    "Botox": "Smooths wrinkles and fine lines. Price: $12/unit.",
    "Microneedling": "Enhances skin texture and promotes collagen. Price: $300.",
    "HydraFacial": "Cleanses, exfoliates, hydrates skin. Price: $250.",
    "IV Therapy": "Customized infusions to boost wellness.",
    "Sculptra": "Stimulates collagen to restore volume. Price: $899/vial.",
    "Contact": "Address: 933 NW 25th Ave, Portland, OR 97210. Phone: (503) 444-9294."
}

class ChatRequest(BaseModel):
    question: str

def generate_response(question: str):
    for key, value in venya_data.items():
        if key.lower() in question.lower():
            return value

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an assistant for Venya MedSpa."},
                      {"role": "user", "content": question}],
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/chat")
async def chat_with_assistant(request: ChatRequest):
    response = generate_response(request.question)
    return {"response": response}
