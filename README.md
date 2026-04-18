# Event Booking Backend

Production-style backend service for event booking and ticket management.

## 🚀 Tech Stack

- Python / Django
- Django REST Framework
- PostgreSQL (planned)
- Redis (planned)
- Celery (planned)

## 📦 Features

- Event management
- Ticket types with availability tracking
- Booking system
- Payment model (foundation)
- REST API (DRF)

## 🔧 API Endpoints

- `GET /api/events/` — list events
- `GET /api/events/{id}/` — event details

## 🧠 Architecture

- Layered architecture (models → serializers → views)
- Prepared for service & repository pattern
- Designed with scalability in mind

## 📍 Current Status

Initial backend implementation:
- database schema
- migrations
- basic API

## 🛠 Setup

```bash
git clone <repo>
cd event-booking

python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

## 📌 Roadmap

- [ ] Booking logic (transactions, concurrency handling)
- [ ] JWT authentication
- [ ] Redis caching layer
- [ ] Celery background tasks (auto-cancel bookings)
- [ ] PostgreSQL integration
- [ ] N+1 query optimization