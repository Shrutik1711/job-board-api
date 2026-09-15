# Job Board API

A RESTful Job Board API built with Flask, MySQL, and SQLAlchemy, allowing companies to post and manage job listings.

## Features
- User signup and login
- Post, view, update, and delete job listings
- MySQL database integration using SQLAlchemy ORM

## Tech Stack
- Python, Flask
- MySQL, SQLAlchemy
- Postman (for testing)

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup | Register a new user |
| POST | /login | Login existing user |
| GET | /jobs | Get all job listings |
| POST | /jobs | Post a new job |
| PUT | /jobs/<id> | Update a job listing |
| DELETE | /jobs/<id> | Delete a job listing |

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your `DB_PASSWORD`
4. Run: `python job_board.py`