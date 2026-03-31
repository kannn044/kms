import streamlit as st
import time
from modules.users import get_user, update_user_profile, get_user_contributions
from modules.auth import validate_password, validate_email
from modules.ui.styles import (
    inject_global_css, render_page_header, render_badge, render_empty_state
)


def show_profile_page():
    """Display a modern user profile page."""
    inject_global_css()

    user = get_user(st.session_state['user_id'])

    if not user:
        st.error("Failed to load user profile")
        return

    # Profile header
    fullname = user['full_name'] or user['username']
    initials = "".join([w[0].upper() for w in fullname.split()[:2]]) if fullname else "U"
    role = user['role']
    role_class = "badge-admin" if role == "admin" else "badge-user"

    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-avatar-large">{initials}</div>
        <h2 style="color: #E8ECF1; margin: 0 0 0.25rem 0;">{fullname}</h2>
        <span class="badge {role_class}" style="font-size: 0.8rem;">{role.upper()}</span>
        <p style="color: #8899AA; margin-top: 0.75rem; font-size: 0.9rem;">
            📧 {user['email']} &nbsp;·&nbsp; 📅 Member since {user['created_date'][:10]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    profile_tabs = st.tabs(["⚙️ Profile Settings", "📄 My Contributions", "🔒 Account Security"])

    with profile_tabs[0]:
        show_profile_settings(user)

    with profile_tabs[1]:
        show_user_contributions(user['id'])

    with profile_tabs[2]:
        show_security_settings(user)


def show_profile_settings(user):
    """Profile information update form."""
    st.markdown("### Edit Your Information")

    with st.form("profile_update_form"):
        username = st.text_input("👤 Username", value=user['username'], disabled=True)
        email = st.text_input("📧 Email", value=user['email'])
        full_name = st.text_input("📝 Full Name", value=user['full_name'])

        update_clicked = st.form_submit_button("💾 Update Profile", use_container_width=True)

    if update_clicked:
        with st.spinner("Updating profile..."):
            progress = st.progress(0)
            for i in range(4):
                progress.progress((i + 1) / 4)
                time.sleep(0.15)

            success, message = update_user_profile(user['id'], email, full_name)

            if success:
                st.session_state['user_fullname'] = full_name
                progress.progress(1.0)
                st.success("✅ Profile updated successfully!")
            else:
                st.error(f"❌ {message}")


def show_user_contributions(user_id):
    """Display user's knowledge contributions as styled cards."""
    contributions = get_user_contributions(user_id)

    st.markdown(f"### Your Contributions ({len(contributions)})")

    if contributions:
        for item in contributions:
            st.markdown(f"""
            <div class="knowledge-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="knowledge-card-title">{item['title']}</div>
                    <span class="badge badge-category">{item['category']}</span>
                </div>
                <div class="knowledge-card-meta">
                    <span>📅 Created: {item['created_date']}</span>
                    <span>🔄 Updated: {item['last_updated']}</span>
                    <span>🆔 ID: {item['id']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            render_empty_state("📝", "No contributions yet", "Start sharing your knowledge!"),
            unsafe_allow_html=True
        )
        if st.button("➕ Add Your First Knowledge Item", use_container_width=True):
            st.session_state["sidebar_selection"] = "Add Knowledge"
            st.rerun()


def show_security_settings(user):
    """Password change form."""
    st.markdown("### Change Password")

    with st.form("password_form"):
        st.info("Leave blank if you don't want to change your password")

        current_password = st.text_input("🔐 Current Password", type="password")
        new_password = st.text_input("🔑 New Password", type="password")
        confirm_password = st.text_input("🔑 Confirm New Password", type="password")

        submit_button = st.form_submit_button("🔒 Change Password", use_container_width=True)

    if submit_button:
        if not current_password:
            st.error("❌ Current password is required")
            return
        if not new_password:
            st.error("❌ New password cannot be empty")
            return
        if new_password != confirm_password:
            st.error("❌ New passwords do not match")
            return

        # Validate new password strength
        valid, pwd_err = validate_password(new_password)
        if not valid:
            st.error(f"❌ {pwd_err}")
            return

        with st.spinner("Changing password..."):
            progress = st.progress(0)
            progress.progress(0.25)
            time.sleep(0.2)
            progress.progress(0.5)
            time.sleep(0.2)
            progress.progress(0.75)

            success, message = update_user_profile(
                user['id'], user['email'], user['full_name'],
                current_password, new_password
            )

            progress.progress(1.0)
            if success:
                st.success("✅ Password changed successfully!")
            else:
                st.error(f"❌ {message}")