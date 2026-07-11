import smtplib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ContactForm
from email_service import send_email

app = FastAPI(
    title="Lucas' API Portfolio",
    description="An API that sends messages from my portfolio to my email",
    version="1.0.0",
    contact={
        "name":"Lucas de Oliveira",
        "email":"lucasdeoliveira937@gmail.com"
    }
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/message", status_code=201)
def create_message(contact: ContactForm):
    
    try:
        send_email(contact)
    except smtplib.SMTPException:
        raise HTTPException(status_code=503, detail="Message service temporarily unavailable. Please try again later.")
    
    return {"detail":"The message has been sent successfully!"}

@app.get("/")
def health_check():
    return {"status": "ok"}