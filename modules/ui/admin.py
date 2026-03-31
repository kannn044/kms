import streamlit as st
import pandas as pd
from modules.users import (
    get_pending_users,
    get_all_users,
    update_user_status,
    update_user_role
)
from modules.ui.styles import (
    inject_global_css, render_page_header, render_metric_card,
    render_badge, render_empty_state
)


def show_user_management_page():
    """Display a modern admin user management interface."""
    inject_global_css()

    render_page_header(
        title="User Management",
        subtitle="Manage users, approve registrations, and view system stats",
        icon="👥"
    )

    admin_tabs = st.tabs(["📋 Pending Approvals", "👤 All Users", "📊 System Stats"])

    with admin_tabs[0]:
        show_pending_approvals()

    with admin_tabs[1]:
        show_all_users()

    with admin_tabs[2]:
        show_system_stats()


def show_pending_approvals():
    """Pending user approval cards."""
    pending_users = get_pending_users()

    if pending_users:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <span style="font-size: 1.5rem;">⏳</span>
            <span style="color: #FFB547; font-weight: 600; font-size: 1.1rem;">
                {len(pending_users)} pending approval{'s' if len(pending_users) > 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

        for user in pending_users:
            st.markdown(f"""
            <div class="user-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <div>
                        <span style="color: #E8ECF1; font-weight: 600; font-size: 1.05rem;">{user['full_name'] or user['username']}</span>
                        <span class="badge badge-pending" style="margin-left: 0.5rem;">Pending</span>
                    </div>
                </div>
                <div style="color: #8899AA; font-size: 0.85rem;">
                    📧 {user['email']} &nbsp;·&nbsp; 📅 Requested: {user['created_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Approve", key=f"approve_{user['id']}", use_container_width=True):
                    success, message = update_user_status(user['id'], "approved")
                    if success:
                        st.success(f"✅ {user['username']} approved!")
                        st.rerun()
                    else:
                        st.error(message)
            with col2:
                if st.button(f"❌ Reject", key=f"reject_{user['id']}", use_container_width=True):
                    success, message = update_user_status(user['id'], "rejected")
                    if success:
                        st.warning(f"User {user['username']} rejected")
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.markdown(
            render_empty_state("✅", "No pending approvals", "All user requests have been processed"),
            unsafe_allow_html=True
        )


def show_all_users():
    """Display and manage all users with styled cards."""
    all_users = get_all_users()

    if all_users:
        filtered_users = [
            u for u in all_users
            if u['username'] != 'admin' and u['id'] != st.session_state['user_id']
        ]

        if filtered_users:
            # Show user cards
            for user in filtered_users:
                status_class = f"badge-{user['status']}"
                role_class = "badge-admin" if user['role'] == 'admin' else "badge-user"

                st.markdown(f"""
                <div class="user-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color: #E8ECF1; font-weight: 600;">{user['full_name'] or user['username']}</span>
                            <span style="color: #8899AA; font-size: 0.85rem;"> @{user['username']}</span>
                        </div>
                        <div>
                            <span class="badge {role_class}">{user['role']}</span>
                            <span class="badge {status_class}">{user['status']}</span>
                        </div>
                    </div>
                    <div style="color: #8899AA; font-size: 0.85rem; margin-top: 0.5rem;">
                        📧 {user['email']} &nbsp;·&nbsp; 📅 {user['created_date']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🔧 Modify User")

            selected_user_id = st.selectbox(
                "Select User",
                options=[u['id'] for u in filtered_users],
                format_func=lambda x: next(
                    (f"{u['full_name'] or u['username']} (@{u['username']})" for u in filtered_users if u['id'] == x),
                    ""
                )
            )

            selected_user = next((u for u in filtered_users if u['id'] == selected_user_id), None)

            if selected_user:
                col1, col2 = st.columns(2)

                with col1:
                    new_role = st.selectbox(
                        "Role",
                        options=["user", "admin"],
                        index=0 if selected_user["role"] == "user" else 1
                    )
                    if st.button("💾 Update Role", use_container_width=True):
                        success, message = update_user_role(selected_user_id, new_role)
                        if success:
                            st.success(f"✅ Role updated to {new_role}")
                            st.rerun()
                        else:
                            st.error(message)

                with col2:
                    new_status = st.selectbox(
                        "Status",
                        options=["pending", "approved", "rejected"],
                        index=["pending", "approved", "rejected"].index(selected_user["status"])
                    )
                    if st.button("💾 Update Status", use_container_width=True):
                        success, message = update_user_status(selected_user_id, new_status)
                        if success:
                            st.success(f"✅ Status updated to {new_status}")
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.markdown(
                render_empty_state("👤", "No users to manage", "Only the admin account exists"),
                unsafe_allow_html=True
            )
    else:
        st.info("No users found")


def show_system_stats():
    """Display system statistics with styled metric cards."""
    from modules.knowledge import get_knowledge_stats
    from modules.database import get_db_connection

    knowledge_stats = get_knowledge_stats()

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE status='approved'")
    active_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE status='pending'")
    pending_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    admin_users = c.fetchone()[0]
    conn.close()

    st.markdown("### 📚 Knowledge Base")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_metric_card("📄", knowledge_stats["total_items"], "Knowledge Items"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("📂", knowledge_stats["total_categories"], "Categories"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("✍️", knowledge_stats["total_contributors"], "Contributors"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 👥 Users")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_metric_card("✅", active_users, "Active Users"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("⏳", pending_users, "Pending"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("🛡️", admin_users, "Administrators"), unsafe_allow_html=True)