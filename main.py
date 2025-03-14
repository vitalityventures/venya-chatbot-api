from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.responses import JSONResponse

# Initialize FastAPI
app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message": "API is working!", "api_key": "Key found!"})

# Ensure OPENAI_API_KEY is set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Simple data
venya_data = {
    "Botox": "Smooths wrinkles and fine lines. Price: $12/unit.",
    "Microneedling": "Enhances skin texture and promotes collagen. Price: $300.",
    "HydraFacial": "Cleanses, exfoliates, hydrates skin. Price: $250.",
    "IV Therapy": "Customized infusions to boost wellness.",
    "Sculptra": "Stimulates collagen to restore volume. Price: $899/vial.",
    "Contact": "Address: 933 NW 25th Ave, Portland, OR 97210. Phone: (503) 444-9294."
}

# Define request model
class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def generate_response(request: ChatRequest):
    question = request.question.strip()

    # If the user asks about a known service, return the predefined response
    for key, value in venya_data.items():
        if key.lower() in question.lower():
            return {"response": value}

    # Validate API key
    if not OPENAI_API_KEY:
        return JSONResponse(content={"error": "OpenAI API key is missing."}, status_code=500)

    # Call OpenAI for unknown queries
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant for Venya MedSpa."},
                {"role": "user", "content": question}
            ],
            api_key=OPENAI_API_KEY
        )
        return {"response": response["choices"][0]["message"]["content"]}

    except openai.error.OpenAIError as e:
        return JSONResponse(content={"error": f"OpenAI API error: {str(e)}"}, status_code=500)
    
    except Exception as e:
        return JSONResponse(content={"error": f"Server error: {str(e)}"}, status_code=500)
