import streamlit as st
from modules.ui.styles import inject_global_css

def show_sidebar():
    """Display a modern styled sidebar with navigation icons."""
    inject_global_css()

    with st.sidebar:
        # User profile section
        fullname = st.session_state.get('user_fullname', 'User')
        role = st.session_state.get('user_role', 'user')
        initials = "".join([w[0].upper() for w in fullname.split()[:2]]) if fullname else "U"
        role_class = "badge-admin" if role == "admin" else "badge-user"

        st.markdown(f"""
        <div class="sidebar-profile">
            <div class="sidebar-avatar">{initials}</div>
            <div class="sidebar-name">{fullname}</div>
            <span class="sidebar-role {role_class}">{role}</span>
        </div>
        """, unsafe_allow_html=True)

        # Navigation with icons
        menu_items = {
            "Home": "📊",
            "Add Knowledge": "➕",
            "Search": "🔍",
            "Profile": "👤",
        }

        if role == 'admin':
            menu_items["Manage Knowledge"] = "⚙️"
            menu_items["User Management"] = "👥"

        menu_labels = [f"{icon}  {name}" for name, icon in menu_items.items()]
        menu_keys = list(menu_items.keys())

        selected_label = st.radio(
            "Navigation",
            menu_labels,
            label_visibility="collapsed"
        )

        # Map label back to key
        selected_index = menu_labels.index(selected_label) if selected_label in menu_labels else 0
        choice = menu_keys[selected_index]

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # Version
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0;">
            <span style="color: #5A6B7D; font-size: 0.75rem;">KMS v1.0.0</span>
        </div>
        """, unsafe_allow_html=True)

        # Logout
        if st.button("🚪  Logout", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        return choice