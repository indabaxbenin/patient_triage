from fastapi import FastAPI
import uvicorn
import os
import logging
from io import BytesIO
from enum import Enum
import uvicorn
from medical_chatbot import get_severity_chatgpt

app = FastAPI(docs_url="/docs",redoc_url = None)\

@app.get("/")
async def root():
    return "Working"

def compute_severity(user_input):
    if 'headache' in user_input or 'stomach pain' in user_input:
        severity = 'Not severe'
    elif 'high blood pressure' in user_input or 'hypertension' in user_input:
        severity = "Moderately severe"
    elif 'bleeding' in user_input:
        severity = 'Very severe'
    return severity
    
@app.get("/get-severity")
async def get_severity(user_input: str):
    #user_input = user_input.lower()
    severity = get_severity_chatgpt(user_input)
    if severity.lower() == 'very severe':
        response = "Hello Patient! We have recieved your complaints. We will be scheduling an appointment immediately. You will be allocated within 24-48 hours."
    elif severity.lower() == 'noderately severe':
        response = "Hello Patient! We have received your complaints and deemed your symptoms moderate. We will allocate you in 2 to 5 days."
    else:
        response = "Hello Patient! We have received your complaints and deemed your symptoms not severe. We will allocate you in 1 week."
    return response
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5050, reload=True)