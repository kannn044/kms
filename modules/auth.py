import re
import streamlit as st
from datetime import datetime
from modules.database import get_db_connection, make_password_hash, verify_password
from config import PASSWORD_MIN_LENGTH

def login_user(username, password):
    """Authenticate user and return user data if successful"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(password, user['password']):
        # ตรวจสอบสถานะ - อาจมีปัญหาตรงนี้
        if user['status'] == 'approved':
            return dict(user)
        else:
            # ควรตรวจสอบการแสดงข้อความผิดพลาดที่ชัดเจนว่าบัญชีรอการอนุมัติ
            return None
    return None

def register_user(username, password, email, full_name):
    """Register a new user with pending status"""
    # Validate input
    if not username or not password or not email or not full_name:
        return False, "All fields are required"
        
    if not validate_email(email):
        return False, "Invalid email format"
        
    valid_password, pwd_error = validate_password(password)
    if not valid_password:
        return False, pwd_error
    
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Check if username or email already exists
        c.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if c.fetchone():
            conn.close()
            return False, "Username or email already exists"
        
        # Add new user
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hashed_password = make_password_hash(password)
        
        c.execute(
            "INSERT INTO users (username, password, email, full_name, created_date) VALUES (?, ?, ?, ?, ?)",
            (username, hashed_password, email, full_name, current_time)
        )
        conn.commit()
        conn.close()
        return True, "Registration successful. Please wait for admin approval."
        
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def validate_email(email):
    """Validate email format using regex"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    return True, ""

def check_auth():
    """Check if user is authenticated and return role"""
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        return False, None
    
    return True, st.session_state.get('user_role', 'user')

def require_auth(page_function):
    """Decorator to require authentication for a page"""
    def wrapper(*args, **kwargs):
        is_authenticated, role = check_auth()
        if is_authenticated:
            return page_function(*args, **kwargs)
        else:
            st.error("You need to log in to access this page")
            st.rerun()()
    return wrapper

def require_admin(page_function):
    """Decorator to require admin role for a page"""
    def wrapper(*args, **kwargs):
        is_authenticated, role = check_auth()
        if is_authenticated and role == 'admin':
            return page_function(*args, **kwargs)
        else:
            st.error("You need admin privileges to access this page")
            st.rerun()()
    return wrapper