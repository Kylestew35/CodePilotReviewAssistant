"""
E-commerce Order Processing Service
A sample repository used as the analysis target for CodePilot Review Assistant.
"""

import os
import json
import hashlib
import datetime
from typing import List, Dict, Optional

# Global config loaded once at module level — smell: no error handling
CONFIG = json.load(open("config.json"))

DATABASE_URL = CONFIG.get("database_url")
SECRET_KEY = CONFIG.get("secret_key", "hardcoded-fallback-secret-123")  # security smell


class OrderProcessor:
    """Processes customer orders."""

    def __init__(self):
        self.db = None  # never initialized properly
        self.orders = []
        self.cache = {}

    def process_order(self, order_data):
        """Process a single order."""
        # No input validation
        user_id = order_data["user_id"]
        items = order_data["items"]
        total = 0

        for item in items:
            price = self.get_price(item["sku"])
            qty = item["qty"]
            total = total + (price * qty)  # smell: repeated pattern, no discount logic

        # Magic number
        if total > 1000:
            total = total * 0.9

        order = {
            "id": self._generate_id(),
            "user_id": user_id,
            "items": items,
            "total": total,
            "status": "pending",
            "created_at": str(datetime.datetime.now()),
        }

        self.orders.append(order)
        self._save_order(order)
        self._notify_user(user_id, order)
        return order

    def get_price(self, sku):
        """Get price for SKU."""
        if sku in self.cache:
            return self.cache[sku]
        # Simulated DB call — no error handling, no timeout
        price = self.db.query(f"SELECT price FROM products WHERE sku = '{sku}'")  # SQL injection
        self.cache[sku] = price
        return price

    def _generate_id(self):
        """Generate order ID."""
        return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()  # md5 smell

    def _save_order(self, order):
        """Persist order to DB."""
        # Fire and forget — no transaction, no rollback
        self.db.execute(f"INSERT INTO orders VALUES ('{order['id']}', '{order['user_id']}', '{order['total']}')")  # SQL injection

    def _notify_user(self, user_id, order):
        """Send notification."""
        # Inline email template — no abstraction
        msg = "Dear user " + str(user_id) + ", your order " + str(order["id"]) + " total is $" + str(order["total"])
        print("Sending email:", msg)  # print instead of logger

    def get_all_orders(self):
        return self.orders  # returns mutable internal list directly

    def cancel_order(self, order_id):
        """Cancel an order."""
        for i, order in enumerate(self.orders):
            if order["id"] == order_id:
                self.orders[i]["status"] = "cancelled"
                # No DB update, no notification to user
                return True
        return False  # silent failure, no exception

    def calculate_tax(self, total, country):
        """Calculate tax."""
        # Hardcoded tax rates — not configurable
        if country == "US":
            return total * 0.08
        elif country == "UK":
            return total * 0.20
        elif country == "DE":
            return total * 0.19
        # Falls through with no return for unknown country — returns None silently


class UserManager:
    """Manages users."""

    def __init__(self):
        self.users = {}

    def create_user(self, username, password, email):
        """Create a new user."""
        # Password stored in plain text
        user = {
            "id": len(self.users) + 1,
            "username": username,
            "password": password,  # plain-text password
            "email": email,
            "created_at": str(datetime.datetime.now()),
        }
        self.users[username] = user
        return user

    def authenticate(self, username, password):
        """Authenticate user."""
        user = self.users.get(username)
        if user and user["password"] == password:  # plain-text compare
            return user
        return None

    def get_user(self, user_id):
        """Get user by ID."""
        # O(n) scan instead of indexed lookup
        for username, user in self.users.items():
            if user["id"] == user_id:
                return user
        return None


def bulk_import_orders(file_path):
    """Import orders from a CSV file."""
    # No file existence check, no encoding handling
    data = open(file_path).read()
    lines = data.split("\n")
    processor = OrderProcessor()
    results = []
    for line in lines:
        if line:
            parts = line.split(",")
            # Fragile CSV parsing — no quoting support
            order = {
                "user_id": parts[0],
                "items": [{"sku": parts[1], "qty": int(parts[2])}],
            }
            result = processor.process_order(order)
            results.append(result)
    return results


def generate_report(start_date, end_date):
    """Generate orders report between two dates."""
    # Entire report built in memory — scalability issue
    processor = OrderProcessor()
    all_orders = processor.get_all_orders()
    filtered = []
    for order in all_orders:
        # String date comparison — fragile
        if order["created_at"] >= start_date and order["created_at"] <= end_date:
            filtered.append(order)
    return filtered
