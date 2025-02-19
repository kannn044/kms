import sqlite3
import hashlib
from datetime import datetime
import streamlit as st
from config import DATABASE_PATH, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_EMAIL

def get_db_connection():
    """Create a database connection and return connection object"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_database():
    """Initialize the database with required tables if they don't exist"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT,
        role TEXT DEFAULT 'user',
        status TEXT DEFAULT 'pending',
        created_date TEXT NOT NULL
    )
    ''')
    
    # Create knowledge_items table
    c.execute('''
    CREATE TABLE IF NOT EXISTS knowledge_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT NOT NULL,
        tags TEXT,
        created_date TEXT NOT NULL,
        last_updated TEXT NOT NULL,
        author_id INTEGER,
        file_path TEXT,
        vector_indexed BOOLEAN DEFAULT 0,
        FOREIGN KEY (author_id) REFERENCES users (id)
    )
    ''')
    
    # Add admin user if not exists
    admin_exists = c.execute("SELECT COUNT(*) FROM users WHERE username = ?", 
                            (DEFAULT_ADMIN_USERNAME,)).fetchone()[0]
    
    if not admin_exists:
        admin_password_hash = make_password_hash(DEFAULT_ADMIN_PASSWORD)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO users (username, password, email, full_name, role, status, created_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (DEFAULT_ADMIN_USERNAME, admin_password_hash, DEFAULT_ADMIN_EMAIL,
             "System Administrator", "admin", "approved", current_time)
        )
    
    conn.commit()
    conn.close()
    return True

def make_password_hash(password):
    """Create a SHA-256 hash of the password"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return make_password_hash(password) == hashed_password

# Cache the connection to improve performance
@st.cache_resource
def get_cached_connection():
    """Get a cached database connection"""
    return get_db_connection()