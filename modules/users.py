from modules.database import get_db_connection, make_password_hash, verify_password
from modules.auth import validate_email

def get_user(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    return dict(user) if user else None

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    return dict(user) if user else None

def get_pending_users():
    """Get users with pending status"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE status = 'pending' ORDER BY created_date DESC")
    users = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return users

def get_all_users():
    """Get all users"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users ORDER BY username")
    users = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return users

def update_user_status(user_id, status):
    """Update user status (pending/approved/rejected)"""
    if status not in ['pending', 'approved', 'rejected']:
        return False, "Invalid status"
        
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        c.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
        conn.commit()
        conn.close()
        return True, f"User status updated to {status}"
    except Exception as e:
        conn.close()
        return False, str(e)

def update_user_role(user_id, role):
    """Update user role (user/admin)"""
    if role not in ['user', 'admin']:
        return False, "Invalid role"
        
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        c.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
        conn.commit()
        conn.close()
        return True, f"User role updated to {role}"
    except Exception as e:
        conn.close()
        return False, str(e)

def update_user_profile(user_id, email, full_name, current_password=None, new_password=None):
    """Update user profile information"""
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format"
        
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        # Check if another user already has this email
        c.execute("SELECT id FROM users WHERE email = ? AND id != ?", (email, user_id))
        if c.fetchone():
            conn.close()
            return False, "Email already in use by another account"
        
        if new_password and current_password:
            # Verify current password
            c.execute("SELECT password FROM users WHERE id = ?", (user_id,))
            result = c.fetchone()
            if not result or not verify_password(current_password, result['password']):
                conn.close()
                return False, "Current password is incorrect"
                
            # Update with new password
            hashed_password = make_password_hash(new_password)
            c.execute(
                "UPDATE users SET email = ?, full_name = ?, password = ? WHERE id = ?",
                (email, full_name, hashed_password, user_id)
            )
        else:
            # Update without changing password
            c.execute(
                "UPDATE users SET email = ?, full_name = ? WHERE id = ?",
                (email, full_name, user_id)
            )
        
        conn.commit()
        conn.close()
        return True, "Profile updated successfully"
    except Exception as e:
        conn.close()
        return False, str(e)

def get_user_contributions(user_id):
    """Get knowledge items contributed by a user"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("""
    SELECT id, title, category, created_date, last_updated
    FROM knowledge_items
    WHERE author_id = ?
    ORDER BY last_updated DESC
    """, (user_id,))
    
    contributions = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return contributions