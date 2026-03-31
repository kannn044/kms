import re
import time
import streamlit as st
from modules.auth import login_user, register_user
from config import PASSWORD_MIN_LENGTH
from modules.ui.styles import inject_global_css


def show_login_page():
    """Display a modern, beautiful login page."""
    inject_global_css()

    # Extra login-specific styles
    st.markdown("""
    <style>
    .login-wrapper {
        max-width: 420px;
        margin: 2rem auto;
        animation: fadeInUp 0.6s ease-out;
    }
    .login-card {
        background: linear-gradient(145deg, rgba(30, 42, 58, 0.9), rgba(26, 35, 50, 0.7));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    }
    .login-logo {
        width: 72px;
        height: 72px;
        margin: 0 auto 1.25rem auto;
        background: linear-gradient(135deg, #6C63FF, #00D4AA);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
        box-shadow: 0 8px 24px rgba(108, 99, 255, 0.35);
        animation: pulseGlow 3s ease-in-out infinite;
    }
    .login-title {
        text-align: center;
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6C63FF, #00D4AA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.25rem;
    }
    .login-subtitle {
        text-align: center;
        color: #8899AA;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    .register-link {
        text-align: center;
        color: #8899AA;
        margin-top: 1rem;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Login card
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-logo">📚</div>
            <div class="login-title">Knowledge Management</div>
            <div class="login-subtitle">Sign in to access your knowledge base</div>
    """, unsafe_allow_html=True)

    # Error message
    if st.session_state.get('login_failed'):
        st.error("⚠️ Invalid credentials or account not approved yet")
        st.session_state['login_failed'] = False

    # Login form
    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        remember = st.checkbox("Remember me")
        login_clicked = st.form_submit_button("Sign In", use_container_width=True)

    # Register section
    st.markdown('<div class="register-link">Don\'t have an account?</div>', unsafe_allow_html=True)
    register_clicked = st.button("Create Account", key="register_btn", use_container_width=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Handle login
    if login_clicked:
        with st.spinner("Authenticating..."):
            user = login_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = user['username']
                st.session_state['user_id'] = user['id']
                st.session_state['user_role'] = user['role']
                st.session_state['user_fullname'] = user['full_name']

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.008)
                    progress.progress((i + 1) / 100)

                st.rerun()
            else:
                st.session_state['login_failed'] = True
                st.rerun()

    if register_clicked:
        st.session_state['show_register'] = True
        st.rerun()


def show_register_page():
    """Display a modern registration page."""
    inject_global_css()

    st.markdown("""
    <style>
    .register-wrapper {
        max-width: 520px;
        margin: 1rem auto;
        animation: fadeInUp 0.6s ease-out;
    }
    .register-card {
        background: linear-gradient(145deg, rgba(30, 42, 58, 0.9), rgba(26, 35, 50, 0.7));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    }
    .reg-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6C63FF, #00D4AA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.25rem;
    }
    .reg-subtitle {
        text-align: center;
        color: #8899AA;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }
    .pwd-req {
        background: #162030;
        border: 1px solid #2A3A4E;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.8rem;
        color: #8899AA;
    }
    .pwd-req-item {
        margin: 0.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Registration success redirect
    if st.session_state.get('registration_success'):
        st.success("✅ Registration successful! Please wait for admin approval.")
        countdown = st.empty()
        for i in range(3, 0, -1):
            countdown.info(f"Redirecting to login in {i}...")
            time.sleep(1)
        st.session_state['registration_success'] = False
        st.session_state['show_register'] = False
        st.rerun()

    # Register card
    st.markdown("""
    <div class="register-wrapper">
        <div class="register-card">
            <div style="text-align: center; margin-bottom: 1rem;">
                <span style="font-size: 2.5rem;">📝</span>
            </div>
            <div class="reg-title">Create Your Account</div>
            <div class="reg-subtitle">Join the knowledge management system</div>
    """, unsafe_allow_html=True)

    with st.form("register_form"):
        st.markdown("**Account Information**")
        username = st.text_input("Username *", placeholder="Choose a username")
        email = st.text_input("Email *", placeholder="your@email.com")

        st.markdown("**Personal Information**")
        full_name = st.text_input("Full Name *", placeholder="Your full name")

        st.markdown("**Security**")
        password = st.text_input("Password *", type="password", placeholder="Create a strong password")

        st.markdown("""
        <div class="pwd-req">
            <div class="pwd-req-item">🔒 At least 8 characters</div>
            <div class="pwd-req-item">🔠 One uppercase letter</div>
            <div class="pwd-req-item">🔡 One lowercase letter</div>
            <div class="pwd-req-item">🔢 One number</div>
        </div>
        """, unsafe_allow_html=True)

        confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
        terms = st.checkbox("I agree to the terms of service and privacy policy")

        submit_button = st.form_submit_button("Create Account", use_container_width=True)

    # Back to login
    st.markdown('<div style="text-align: center; color: #8899AA; margin-top: 1rem;">Already have an account?</div>', unsafe_allow_html=True)
    if st.button("Back to Sign In", key="back_to_login_btn", use_container_width=True):
        st.session_state['show_register'] = False
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Handle submission
    if submit_button:
        error_message = None
        if not username or not email or not full_name or not password or not confirm_password:
            error_message = "All fields are required"
        elif not validate_email(email):
            error_message = "Invalid email format"
        elif password != confirm_password:
            error_message = "Passwords do not match"
        elif not terms:
            error_message = "You must agree to the terms and privacy policy"
        else:
            valid_pwd, pwd_err = validate_password(password)
            if not valid_pwd:
                error_message = pwd_err

        if error_message:
            st.error(f"❌ {error_message}")
        else:
            with st.spinner("Creating your account..."):
                progress = st.progress(0)
                for i in range(4):
                    progress.progress((i + 1) / 4)
                    time.sleep(0.3)

                success, message = register_user(username, password, email, full_name)
                if success:
                    progress.progress(1.0)
                    st.session_state['registration_success'] = True
                    st.rerun()
                else:
                    st.error(f"❌ {message}")


def validate_email(email):
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength."""
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    return True, ""