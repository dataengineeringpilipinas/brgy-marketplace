# Barangay Home-Based Business Marketplace

A FastAPI-based marketplace application for barangay home-based businesses.

## Features

- **Business Profiles**: Residents can create and manage their home-based business profiles
- **Marketplace Listing**: Browse businesses with filters (category, verified, distance, search)
- **Order/Inquiry System**: Simple chat-based order system for buyers and sellers
- **Reviews & Ratings**: Rate and review businesses after completing orders
- **Promo Highlights**: Barangay-admin managed promotional highlights
- **Analytics Dashboard**: Admin dashboard with business and order statistics

## Project Structure

```
brgy-marketplace/
├── app/
│   ├── models/          # Database models
│   ├── controllers/     # Business logic
│   ├── routes/         # API routes
│   ├── schemas/        # Pydantic schemas
│   ├── templates/      # Jinja2 templates
│   ├── utils/         # Utility functions
│   └── database.py     # Database configuration
├── migrations/         # Alembic migrations
├── main.py            # FastAPI app entry point
├── requirements.txt   # Python dependencies
└── Dockerfile         # Container configuration
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Initialize database:
```bash
alembic upgrade head
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## Deployment to Fly.io

1. Create volume:
```bash
fly volumes create brgy_marketplace_data --size 10 --region lax
```

2. Deploy:
```bash
fly deploy
```

## API Documentation

Once running, visit:
- API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

A Vibecamp Creation
