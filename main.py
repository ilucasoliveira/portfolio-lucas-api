import logging

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded

from schemas import ContactForm
from email_service import send_email, EmailDeliveryError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=get_client_ip)

app = FastAPI(
    title="Lucas' API Portfolio",
    description="An API that sends messages from my portfolio to my email",
    version="1.1.0",
    contact={
        "name": "Lucas de Oliveira",
        "email": "lucasoliveirapimentel.dev@gmail.com",
    },
)

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning("Rate limit exceeded for %s", get_client_ip(request))
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many messages. Please try again later."},
    )


origins = [
    "http://localhost:5173",
    "https://lucasdeoliveira.vercel.app",
    "https://ilucasoliveira.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

SUCCESS_RESPONSE = {"detail": "The message has been sent successfully!"}


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.head("/ping")
def ping_head():
    return Response()


@app.post("/message", status_code=201)
@limiter.limit("3/minute;10/day")
def create_message(request: Request, contact: ContactForm):
    if contact.website:
        logger.info("Honeypot triggered, message discarded")
        return SUCCESS_RESPONSE

    try:
        send_email(contact)
    except EmailDeliveryError:
        raise HTTPException(
            status_code=503,
            detail="Message service temporarily unavailable. Please try again later.",
        )

    return SUCCESS_RESPONSE
