from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from schemas import ContactForm
from email_service import send_email, EmailDeliveryError

app = FastAPI(
    title="Lucas' API Portfolio",
    description="An API that sends messages from my portfolio to my email",
    version="1.0.0",
    contact={
        "name":"Lucas de Oliveira",
        "email":"lucasoliveirapimentel.dev@gmail.com"
    }
)

origins = [
    "http://localhost:5173",
    "https://lucasdeoliveira.vercel.app",
    "https://ilucasoliveira.dev",
]

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.head("/ping")
def ping_head():
    return Response()

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
    except EmailDeliveryError:
        raise HTTPException(status_code=503, detail="Message service temporarily unavailable. Please try again later.")
    
    return {"detail":"The message has been sent successfully!"}

@app.get("/")
def health_check():
    return {"status": "ok"}