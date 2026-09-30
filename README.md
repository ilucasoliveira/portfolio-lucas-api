# ᚦ Portfolio Contact API

REST API that receives messages from my [portfolio's](https://ilucasoliveira.dev) contact form and delivers them to my inbox via transactional email. Built with FastAPI, validated with Pydantic v2, protected against spam and abuse, and intentionally stateless: no database.

**Live:** https://portfolio-lucas-api.onrender.com ([interactive docs](https://portfolio-lucas-api.onrender.com/docs))
**Frontend repository:** [ilucasoliveira/portfolio](https://github.com/ilucasoliveira/portfolio)

## ✦ Architecture

```
Portfolio (React) ──POST /message──►  FastAPI (Render)
                                        │
                                        ├─ Rate limit (per IP) ──────► 429 when exceeded
                                        ├─ Pydantic validation ──────► 422 on invalid data
                                        ├─ Honeypot filled ──────────► 201, silently discarded
                                        ├─ email_service (Resend) ───► 📬 inbox
                                        └─ Delivery failure ─────────► 503, error logged
```

**Design decisions:**

- **No database.** The API is a dispatcher, not a warehouse: messages are delivered, not stored. Fewer moving parts, zero persistence cost.
- **Separation of concerns.** Routes (`main.py`) don't know how emails are sent. All delivery logic lives in `email_service.py` behind a custom `EmailDeliveryError`. This paid off in production: the original SMTP implementation hit blocked ports on Render's free tier (`OSError: Network is unreachable`), and swapping to Resend's HTTP API meant rewriting **one file**, with routes, schemas and frontend untouched.
- **Defense in depth against spam.** A hidden `website` field works as a honeypot: bots fill it, humans never see it. Filled submissions get a normal `201` so the bot never learns it was caught. On top of that, each IP is limited to 3 messages per minute and 10 per day.
- **Validation on both ends.** The frontend validates for user experience; the API validates because anyone can call it directly. Whitespace is stripped before length checks, so `"   "` counts as empty.
- **Observable failures.** Delivery errors are logged with their full traceback before being turned into a `503`, so a failing provider shows up in the server logs instead of disappearing.
- **`Reply-To` header.** Replying to a delivered message goes straight to the visitor's address.
- **Consistent error shape.** Every error response uses `{"detail": ...}`, including rate limiting.

## ✦ Tech Stack

- **FastAPI**: routing, automatic OpenAPI docs, CORS middleware
- **Pydantic v2**: request validation (`EmailStr`, length constraints, whitespace stripping)
- **SlowAPI**: per-IP rate limiting
- **Resend**: transactional email delivery over HTTPS
- **pytest**: API tests with the email provider mocked out
- **python-dotenv**: credentials via environment variables
- **Poetry**: dependency management
- **Render**: deployment (kept awake via UptimeRobot pinging `/ping`)

## ✦ API Reference

### `POST /message`

| Field     | Type   | Constraints                        |
| --------- | ------ | ---------------------------------- |
| `name`    | string | 1 to 100 chars (after trimming)    |
| `email`   | string | valid email format                 |
| `subject` | string | 1 to 150 chars (after trimming)    |
| `message` | string | 10 to 5000 chars (after trimming)  |
| `website` | string | honeypot, must be empty (optional) |

**Responses**

| Code  | Meaning                                           |
| ----- | ------------------------------------------------- |
| `201` | Message delivered                                 |
| `422` | Validation failed (detailed field errors in body) |
| `429` | Rate limit exceeded (3/minute, 10/day per IP)     |
| `503` | Mail service temporarily unavailable              |

### `GET /ping`

Health check, returns `{"status": "ok"}`. Used for uptime monitoring and by the portfolio's live API status indicator.

Interactive docs available at `/docs`.

## ✦ Getting Started

```bash
# clone and install
git clone https://github.com/ilucasoliveira/portfolio-lucas-api.git
cd portfolio-lucas-api
poetry install

# configure credentials
cp .env.example .env
# edit .env with your Resend API key and destination email

# run
poetry run fastapi dev main.py
```

### Running the tests

```bash
poetry run pytest
```

The suite covers successful delivery, validation errors, whitespace handling, the honeypot, rate limiting and provider failure. Email delivery is mocked, so no real messages are sent.

### Environment variables

| Variable         | Required | Description                                                      |
| ---------------- | -------- | ---------------------------------------------------------------- |
| `RESEND_API_KEY` | yes      | [Resend](https://resend.com) API key with sending access         |
| `GMAIL_USER`     | yes      | Destination inbox, where the contact messages are delivered      |
| `RESEND_FROM`    | no       | Verified sender. Defaults to `Portfolio <onboarding@resend.dev>` |

> ⚠️ Never commit the `.env` file. The `.env.example` with empty values documents the expected variables.

## ✦ Project Structure

```
├── main.py            # FastAPI app, CORS, rate limiting and routes
├── schemas.py         # Pydantic ContactForm schema
├── email_service.py   # Email delivery (the only file that knows how emails are sent)
├── tests/
│   └── test_main.py   # API tests with the email provider mocked
├── pyproject.toml     # Poetry and pytest configuration
└── .env               # credentials (not committed)
```

## ✦ Author

**Lucas de Oliveira**, Full Stack Python Developer

- Portfolio: [ilucasoliveira.dev](https://ilucasoliveira.dev)
- GitHub: [@ilucasoliveira](https://github.com/ilucasoliveira)
- LinkedIn: [in/ilucasoliveira](https://www.linkedin.com/in/ilucasoliveira/)

---

ᛚ · _forged in Minas · MMXXVI_
