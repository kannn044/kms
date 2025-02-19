import re
import streamlit as st
from modules.auth import login_user, register_user
from modules.database import get_db_connection
import time
from config import PASSWORD_MIN_LENGTH

def show_login_page():
    """Display enhanced login page with properly positioned register button"""
    # ใช้ CSS เพื่อปรับแต่งหน้า login
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding-bottom: 1rem;
    }
    .login-card {
        background-color: #1E2A38;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-logo {
        width: 80px;
        height: 80px;
        margin: 0 auto 1rem auto;
        background-color: #4263EB;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: white;
    }
    .login-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        font-size: 1rem;
        color: #A0AEC0;
        margin-bottom: 1rem;
    }
    /* Stacked buttons with proper styling */
    .auth-buttons {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        width: 100%;
    }
    .login-button {
        width: 100%;
        background-color: #4263EB;
        color: white;
        font-weight: 500;
        height: 2.8rem;
        border-radius: 6px;
        border: none;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .login-button:hover {
        background-color: #3251D8;
        box-shadow: 0 4px 10px rgba(66, 99, 235, 0.3);
    }
    .register-button {
        width: 100%;
        background-color: transparent;
        color: #4263EB;
        font-weight: 500;
        height: 2.8rem;
        border-radius: 6px;
        border: 1px solid #4263EB;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .register-button:hover {
        background-color: rgba(66, 99, 235, 0.1);
    }
    .register-section {
        text-align: center;
        margin-top: 1rem;
        color: #A0AEC0;
    }
    .form-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
    }
    .form-footer a {
        color: #4263EB;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .form-footer a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # แสดงหน้า login ด้วย HTML/CSS ที่สวยงาม
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <div class="login-logo">📚</div>
                <h1 class="login-title">Knowledge Management</h1>
                <p class="login-subtitle">Access your organization's knowledge base</p>
            </div>
    """, unsafe_allow_html=True)
    
    # แสดงข้อความผิดพลาด (ถ้ามี)
    if 'login_failed' in st.session_state and st.session_state['login_failed']:
        st.error("Invalid username or password, or your account is not approved yet")
        st.session_state['login_failed'] = False
    
    # ฟอร์ม login
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Remember me และ Forgot password
        col1, col2 = st.columns([1, 1])
        with col1:
            remember = st.checkbox("Remember me")
        # with col2:
        #     st.markdown('<div style="text-align: right;"><a href="#" style="color: #4263EB; text-decoration: none;">Forgot password?</a></div>', unsafe_allow_html=True)
        
        # ปุ่ม Login (ภายในฟอร์ม)
        login_clicked = st.form_submit_button("Login", use_container_width=True)
    
    # ส่วนลงทะเบียน (อยู่ด้านล่างในการ์ดเดียวกัน แต่นอกฟอร์ม login)
    st.markdown("""
        <div class="register-section">
            <p>Don't have an account yet?</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ปุ่ม Register ด้านล่างปุ่ม Login
    register_clicked = st.button("Register", key="register_btn", use_container_width=True)
    
    # ปิด login-card
    # st.markdown("</div>")
    
    # ตรวจสอบการล็อกอิน
    if login_clicked:
        with st.spinner("Authenticating..."):
            user = login_user(username, password)
            
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = user['username']
                st.session_state['user_id'] = user['id']
                st.session_state['user_role'] = user['role']
                st.session_state['user_fullname'] = user['full_name']
                
                # แสดง loading animation
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress((i+1)/100)
                
                st.rerun()
            else:
                st.session_state['login_failed'] = True
                st.rerun()
    
    # ตรวจสอบการกดปุ่ม Register
    if register_clicked:
        st.session_state['show_register'] = True
        st.rerun()


def show_register_page():
    """Display enhanced register page that matches the login design"""
    # ใช้ CSS เพื่อปรับแต่งหน้า register ให้เข้ากับหน้า login
    st.markdown("""
    <style>
    .register-container {
        max-width: 550px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #1E2A38;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    }
    .register-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .register-logo {
        width: 80px;
        height: 80px;
        margin: 0 auto 1rem auto;
        background-color: #4263EB;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: white;
    }
    .register-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.5rem;
    }
    .register-subtitle {
        font-size: 1rem;
        color: #A0AEC0;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4263EB;
        color: white;
        font-weight: 500;
        height: 2.5rem;
        border-radius: 6px;
        border: none;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #3251D8;
        box-shadow: 0 4px 10px rgba(66, 99, 235, 0.3);
    }
    .back-button {
        background-color: transparent !important;
        color: #4263EB !important;
        text-decoration: none;
        border: 1px solid #4263EB !important;
    }
    .back-button:hover {
        background-color: rgba(66, 99, 235, 0.1) !important;
    }
    .stTextInput > div > div > input,
    .stForm > div > div > div > div > div > div > input {
        background-color: #2D3748;
        color: white;
        border: 1px solid #4A5568;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        height: 2.8rem;
    }
    .stTextInput > div > div > input:focus,
    .stForm > div > div > div > div > div > div > input:focus {
        border-color: #4263EB;
        box-shadow: 0 0 0 1px #4263EB;
    }
    .register-error {
        background-color: rgba(254, 178, 178, 0.1);
        border-left: 4px solid #E53E3E;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        color: #FC8181;
    }
    .register-success {
        background-color: rgba(154, 230, 180, 0.1);
        border-left: 4px solid #38A169;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        color: #9AE6B4;
    }
    .form-divider {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
        color: #A0AEC0;
    }
    .form-divider::before,
    .form-divider::after {
        content: "";
        flex: 1;
        border-bottom: 1px solid #4A5568;
    }
    .form-divider::before {
        margin-right: 1rem;
    }
    .form-divider::after {
        margin-left: 1rem;
    }
    .password-requirements {
        font-size: 0.8rem;
        color: #A0AEC0;
        margin: 0.5rem 0;
        padding: 0.75rem;
        background-color: #2D3748;
        border-radius: 4px;
    }
    .requirement-item {
        display: flex;
        align-items: center;
        margin-bottom: 0.3rem;
    }
    .requirement-icon {
        margin-right: 0.5rem;
    }
    .form-info {
        font-size: 0.8rem;
        color: #A0AEC0;
        margin-top: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # แสดงหน้า register ด้วย HTML/CSS ที่สวยงาม
    st.markdown("""
    <div class="register-container">
        <div class="register-header">
            <div class="register-logo">📝</div>
            <h1 class="register-title">Create New Account</h1>
            <p class="register-subtitle">Join your organization's knowledge management system</p>
        </div>
    """, unsafe_allow_html=True)
    
    # สถานะการลงทะเบียน
    if 'registration_success' in st.session_state and st.session_state['registration_success']:
        st.markdown("""
        <div class="register-success">
            <strong>Registration successful!</strong> Please wait for admin approval before logging in.
            <br>You will be redirected to login page in a few seconds...
        </div>
        """, unsafe_allow_html=True)
        
        # เพิ่ม countdown
        countdown = st.empty()
        for i in range(5, 0, -1):
            countdown.markdown(f"<div style='text-align: center; color: #A0AEC0;'>Redirecting in {i} seconds...</div>", unsafe_allow_html=True)
            time.sleep(1)
        
        # กลับไปหน้า login
        st.session_state['registration_success'] = False
        st.session_state['show_register'] = False
        st.rerun()
    
    # ฟอร์มลงทะเบียน
    with st.form("register_form"):
        # ข้อมูลบัญชี
        st.markdown("<h3 style='color: white; font-size: 1.2rem; margin-bottom: 1rem;'>Account Information</h3>", unsafe_allow_html=True)
        
        username = st.text_input("Username*")
        email = st.text_input("Email*")

        # ข้อมูลส่วนตัว
        st.markdown("<div class='form-divider'>Personal Information</div>", unsafe_allow_html=True)
        full_name = st.text_input("Full Name*")
        
        # รหัสผ่าน
        st.markdown("<div class='form-divider'>Security</div>", unsafe_allow_html=True)
        password = st.text_input("Password*", type="password")
        
        # แสดงข้อกำหนดรหัสผ่าน
        st.markdown("""
        <div class="password-requirements">
            <div class="requirement-item">
                <span class="requirement-icon">🔒</span> Must be at least 8 characters
            </div>
            <div class="requirement-item">
                <span class="requirement-icon">🔠</span> Must contain at least one uppercase letter
            </div>
            <div class="requirement-item">
                <span class="requirement-icon">🔡</span> Must contain at least one lowercase letter
            </div>
            <div class="requirement-item">
                <span class="requirement-icon">🔢</span> Must contain at least one number
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        # ข้อตกลงและเงื่อนไข
        st.markdown("<div class='form-divider'>Terms</div>", unsafe_allow_html=True)
        st.checkbox("I agree to the terms of service and privacy policy", key="terms_agree")
        
        # ปุ่มลงทะเบียน
        submit_button = st.form_submit_button("Register")
        
        # ข้อมูลเพิ่มเติม
        st.markdown("""
        <div class="form-info">
            * All fields marked with an asterisk are required.<br>
            * Your account will require admin approval before you can login.
        </div>
        """, unsafe_allow_html=True)
    
    # ปุ่มกลับไปหน้า login
    st.markdown("<div style='text-align: center; margin-top: 1.5rem;'>Already have an account?</div>", unsafe_allow_html=True)
    if st.button("Back to Login", key="back_to_login_btn", help="Return to login page"):
        st.session_state['show_register'] = False
        st.rerun()
    
    # ปิด container
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ตรวจสอบการส่งฟอร์ม
    if submit_button:
        # ตรวจสอบข้อมูล
        error_message = None
        
        if not username or not email or not full_name or not password or not confirm_password:
            error_message = "All fields are required"
        elif not validate_email(email):
            error_message = "Invalid email format"
        elif password != confirm_password:
            error_message = "Passwords do not match"
        elif not st.session_state.get("terms_agree", False):
            error_message = "You must agree to the terms of service and privacy policy"
        else:
            # ตรวจสอบความซับซ้อนของรหัสผ่าน
            valid_password, pwd_error = validate_password(password)
            if not valid_password:
                error_message = pwd_error
        
        if error_message:
            # แสดงข้อความผิดพลาด
            st.markdown(f"""
            <div class="register-error">
                <strong>Registration failed.</strong> {error_message}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Creating your account..."):
                # แสดง progress
                progress = st.progress(0)
                stages = ["Validating information", "Creating user record", "Setting up profile", "Finalizing"]
                
                for i, stage in enumerate(stages):
                    st.text(stage + "...")
                    progress.progress((i+1)/len(stages))
                    time.sleep(0.5)
                
                # ลงทะเบียนผู้ใช้
                success, message = register_user(username, password, email, full_name)
                
                if success:
                    progress.progress(1.0)
                    st.session_state['registration_success'] = True
                    st.rerun()
                else:
                    st.markdown(f"""
                    <div class="register-error">
                        <strong>Registration failed.</strong> {message}
                    </div>
                    """, unsafe_allow_html=True)

def back_to_login():
    """Helper function to go back to login page"""
    st.session_state['show_register'] = False
    st.session_state['registration_success'] = False
    
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