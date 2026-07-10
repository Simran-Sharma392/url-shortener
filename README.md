# URL Shortener

A URL shortening web application built with **FastAPI**, **SQLite**, and **SQLAlchemy**. Users can create short URLs, choose custom slugs, update existing links, delete them and track click analytics through a simple web interface.

## Features

- Shorten long URLs
- Custom slug support
- Redirect using short URLs
- Update existing URLs
- Delete URLs
- Click analytics
- User-agent tracking
- RESTful API with Swagger documentation
- Simple frontend built with HTML, CSS, and JavaScript

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2
- HTML
- CSS
- JavaScript

## Project Structure

```
backend/
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── __init__.py
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Create a short URL |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/shorten/{short_code}` | Retrieve URL details |
| PUT | `/shorten/{short_code}` | Update URL |
| DELETE | `/shorten/{short_code}` | Delete URL |
| GET | `/shorten/{short_code}/stats` | View analytics |

## Future Improvements

- User authentication
- Expiring links
- QR code generation
- Docker support
- Deployment

## License

This project is for educational and portfolio purposes.