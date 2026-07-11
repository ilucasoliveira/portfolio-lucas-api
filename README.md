# ᚦ Portfolio Contact API

REST API that receives messages from my [portfolio's](add-your-portfolio-url) contact form and delivers them to my inbox via email — built with FastAPI, validated with Pydantic v2, no database required by design.

## ✦ Architecture

```
Portfolio (React) ──POST /message──►  FastAPI
                                        │
                                        ├─ Pydantic validation ──► 422 on invalid data
                                        ├─ email_service (SMTP/SSL) ──► 📬 inbox
                                        └─ SMTP failure ──► 503
```

**Design decisions:**

- **No database.** The API is a dispatcher, not a warehouse — messages are delivered, not stored. Fewer moving parts, zero persistence cost.
- **Separation of concerns.** Routes (`main.py`) don't know how emails are sent; all SMTP logic lives in `email_service.py`. Swapping SMTP for a transactional service (e.g. Resend) means rewriting one file.
- **`Reply-To` header.** Replying to a delivered message goes straight to the visitor's address — no copy-pasting.
- **Honest status codes.** `201` on success, `422` for invalid input (automatic via Pydantic), `503` when the mail provider fails — client errors and server errors properly separated.

## ✦ Tech Stack

- **FastAPI** — routing, automatic OpenAPI docs, CORS middleware
- **Pydantic v2** — request validation (`EmailStr`, length constraints)
- **smtplib + EmailMessage** — SMTP over SSL (standard library)
- **python-dotenv** — credentials via environment variables
- **Poetry** — dependency management

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

### `GET /`

Health check — returns `{"status": "ok"}`.

Interactive docs available at `/docs` when running.

## ✦ Getting Started

```bash
# clone and install
git clone https://github.com/ilucasoliveira/[your-repo-name].git
cd [your-repo-name]
poetry install

# configure credentials
cp .env.example .env
# edit .env with your Gmail address and App Password

# run
poetry run fastapi dev main.py
```

### Environment variables

| Variable             | Description                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------- |
| `GMAIL_USER`         | Gmail address that sends and receives the messages                                           |
| `GMAIL_APP_PASSWORD` | 16-character [Google App Password](https://myaccount.google.com/apppasswords) (requires 2FA) |

> ⚠️ Never commit the `.env` file. An `.env.example` with empty values documents the expected variables.

## ✦ Project Structure

```
├── main.py            # FastAPI app, CORS, POST /message route
├── schemas.py         # Pydantic ContactForm schema
├── email_service.py   # SMTP delivery (the only file that knows how emails are sent)
├── pyproject.toml     # Poetry configuration
└── .env               # credentials (not committed)
```

## ✦ Author

**Lucas de Oliveira** — Full Stack Python Developer

- GitHub: [@ilucasoliveira](https://github.com/ilucasoliveira)
- LinkedIn: [in/ilucasoliveira](https://www.linkedin.com/in/ilucasoliveira/)
- Portfolio: [add your portfolio URL here]

---

ᛚ · _forged in Minas · MMXXVI_
