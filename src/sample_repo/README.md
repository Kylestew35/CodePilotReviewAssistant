# Order Processing Service

A microservice for processing e-commerce orders.

## Setup

Install dependencies and run:

```bash
pip install -r requirements.txt
python app.py
```

## Configuration

Edit `config.json` with your database credentials.

## API

- `POST /orders` — Create an order
- `GET /orders` — List all orders
- `DELETE /orders/{id}` — Cancel an order

## Notes

This service handles order creation, user management, and reporting.
Tax calculation is supported for US, UK, and DE.
