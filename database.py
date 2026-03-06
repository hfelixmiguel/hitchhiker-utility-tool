"""
Database module for Intergalactic Hitchhiker's Guide Utility.

Provides SQLite-based persistent storage for calculation history.
"""

import sqlite3
import os
import json
import logging
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Database file path
DB_PATH = os.environ.get('DATABASE_PATH', '/tmp/hitchhiker_history.db')


def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database with required tables."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create calculations history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calculations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    distance_ly REAL NOT NULL,
                    fuel_efficiency REAL NOT NULL,
                    tax_rate REAL NOT NULL,
                    base_cost REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    total_cost REAL NOT NULL,
                    currency TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create advice requests table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advice_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    count INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


def save_calculation(distance_ly, fuel_efficiency, tax_rate, base_cost, tax_amount, total_cost, currency):
    """Save a calculation to the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO calculations 
                (distance_ly, fuel_efficiency, tax_rate, base_cost, tax_amount, total_cost, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (distance_ly, fuel_efficiency, tax_rate, base_cost, tax_amount, total_cost, currency))
            conn.commit()
            logger.info(f"Saved calculation: {distance_ly} ly = {total_cost} {currency}")
            return cursor.lastrowid
    except Exception as e:
        logger.error(f"Failed to save calculation: {e}")
        return None


def get_calculations(limit=50):
    """Get calculation history from the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM calculations 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Failed to get calculations: {e}")
        return []


def save_advice_request(count):
    """Save an advice request to the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO advice_requests (count)
                VALUES (?)
            ''', (count,))
            conn.commit()
            logger.info(f"Saved advice request: {count} advices")
            return cursor.lastrowid
    except Exception as e:
        logger.error(f"Failed to save advice request: {e}")
        return None


def clear_history():
    """Clear all history from the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM calculations')
            cursor.execute('DELETE FROM advice_requests')
            conn.commit()
            logger.info("History cleared successfully")
            return True
    except Exception as e:
        logger.error(f"Failed to clear history: {e}")
        return False


# Initialize database on module import
init_database()
