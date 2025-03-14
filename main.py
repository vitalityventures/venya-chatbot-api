import openai
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# Initialize FastAPI
app = FastAPI()

# Ensure OpenAI API key is set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Sample predefined responses
venya_data = {
    "botox": "Smooths wrinkles and fine lines. Price: $12/unit.",
    "microneedling": "Enhances skin texture and promotes collagen. Price: $300.",
    "hydrafacial": "Cleanses, exfoliates, hydrates skin. Price: $250.",
    "iv therapy": "Customized infusions to boost wellness.",
    "sculptra": "Stimulates collagen to restore volume. Price: $899/vial.",
    "contact": "Address: 933 NW 25th Ave, Portland, OR 97210. Phone: (503) 444-9294."
}

# Define request model
class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def generate_response(request: ChatRequest):
    question = request.question.lower()

    # Check for predefined answers
    for key, value in venya_data.items():
        if key in question:
            return JSONResponse(content={"response": value})

    # If no predefined response, ask OpenAI (with a timeout)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an assistant for Venya MedSpa."},
                      {"role": "user", "content": request.question}],
            api_key=OPENAI_API_KEY,
            timeout=5  # **NEW: Added timeout to avoid long delays**
        )
        return JSONResponse(content={"response": response["choices"][0]["message"]["content"]})

    except openai.error.Timeout:
        return JSONResponse(content={"response": "I'm sorry, this question is taking too long to answer. Can you try rewording it?"})

    except Exception as e:
        return JSONResponse(content={"response": "I'm not sure about that. Maybe try asking another way!"})

