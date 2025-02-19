import streamlit as st
import os

# Import config
from config import APP_NAME, APP_ICON, VECTORSTORE_PATH

# Import modules
from modules.database import get_db_connection,init_database
from modules.vectorstore import rebuild_vectorstore
from modules.knowledge import get_knowledge_stats, search_knowledge_items

# Import UI components
from modules.ui.login import show_login_page, show_register_page
from modules.ui.sidebar import show_sidebar
from modules.ui.home import show_home_page
from modules.ui.search import show_search_page
from modules.ui.knowledge_form import show_add_knowledge_page, show_manage_knowledge_page
from modules.ui.profile import show_profile_page
from modules.ui.admin import show_user_management_page

# Configure page settings
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide"
)

def main():
    """Main application entry point"""
    # Initialize database
    init_database()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False
    
    # Handle auth flow
    if st.session_state['show_register']:
        show_register_page()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        # Show main application
        choice = show_sidebar()
        
        if choice == "Home":
            show_home_page()
        elif choice == "Add Knowledge":
            # show_add_knowledge_page()
            conn = get_db_connection()  # หรือใช้ conn ที่สร้างไว้แล้ว
            show_add_knowledge_page(conn)
        elif choice == "Search":
            show_search_page()
        elif choice == "Profile":
            show_profile_page()
        elif choice == "Manage Knowledge":
            if st.session_state['user_role'] == 'admin':
                show_manage_knowledge_page()
            else:
                st.error("You do not have permission to access this page")
        elif choice == "User Management":
            if st.session_state['user_role'] == 'admin':
                show_user_management_page()
            else:
                st.error("You do not have permission to access this page")

if __name__ == "__main__":
    main()