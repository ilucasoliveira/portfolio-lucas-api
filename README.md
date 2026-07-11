# ᚦ Portfolio Contact API

REST API that receives messages from my [portfolio's](https://lucasdeoliveira.vercel.app) contact form and delivers them to my inbox via transactional email — built with FastAPI, validated with Pydantic v2, no database required by design.

**Live:** https://portfolio-lucas-api.onrender.com ([interactive docs](https://portfolio-lucas-api.onrender.com/docs))
**Frontend repository:** [ilucasoliveira/portfolio](https://github.com/ilucasoliveira/portfolio)

## ✦ Architecture

```
Portfolio (React) ──POST /message──►  FastAPI (Render)
                                        │
                                        ├─ Pydantic validation ──► 422 on invalid data
                                        ├─ email_service (Resend API) ──► 📬 inbox
                                        └─ delivery failure ──► 503
```

**Design decisions:**

- **No database.** The API is a dispatcher, not a warehouse — messages are delivered, not stored. Fewer moving parts, zero persistence cost.
- **Separation of concerns.** Routes (`main.py`) don't know how emails are sent; all delivery logic lives in `email_service.py` behind a custom `EmailDeliveryError`. This paid off in production: the original SMTP implementation hit blocked ports on Render's free tier (`OSError: Network is unreachable`), and swapping to Resend's HTTP API meant rewriting **one file** — routes, schemas and frontend untouched.
- **`Reply-To` header.** Replying to a delivered message goes straight to the visitor's address — no copy-pasting.
- **Honest status codes.** `201` on success, `422` for invalid input (automatic via Pydantic), `503` when the mail provider fails — client errors and server errors properly separated.

## ✦ Tech Stack

- **FastAPI** — routing, automatic OpenAPI docs, CORS middleware
- **Pydantic v2** — request validation (`EmailStr`, length constraints)
- **Resend** — transactional email delivery over HTTPS
- **python-dotenv** — credentials via environment variables
- **Poetry** — dependency management
- **Render** — deployment (kept awake via UptimeRobot pinging `/ping`)

## ✦ API Reference

### `POST /message`

| Field     | Type   | Constraints        |
| --------- | ------ | ------------------ |
| `name`    | string | 2–300 chars        |
| `email`   | string | valid email format |
| `subject` | string | 5–300 chars        |
| `message` | string | 10–1000 chars      |

**Responses**

| Code  | Meaning                                           |
| ----- | ------------------------------------------------- |
| `201` | Message delivered                                 |
| `422` | Validation failed (detailed field errors in body) |
| `503` | Mail service temporarily unavailable              |

### `GET /ping`

Health check — returns `{"status": "ok"}`. Used for uptime monitoring.

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

### Environment variables

| Variable         | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| `RESEND_API_KEY` | [Resend](https://resend.com) API key with sending access     |
| `GMAIL_USER`     | Destination inbox — where the contact messages are delivered |

> ⚠️ Never commit the `.env` file. An `.env.example` with empty values documents the expected variables.

## ✦ Project Structure

```
├── main.py            # FastAPI app, CORS, POST /message and GET /ping routes
├── schemas.py         # Pydantic ContactForm schema
├── email_service.py   # Email delivery (the only file that knows how emails are sent)
├── pyproject.toml     # Poetry configuration
└── .env               # credentials (not committed)
```

## ✦ Author

**Lucas de Oliveira** — Full Stack Python Developer

- Portfolio: [lucasdeoliveira.vercel.app](https://lucasdeoliveira.vercel.app)
- GitHub: [@ilucasoliveira](https://github.com/ilucasoliveira)
- LinkedIn: [in/ilucasoliveira](https://www.linkedin.com/in/ilucasoliveira/)

---

ᛚ · _forged in Minas · MMXXVI_
