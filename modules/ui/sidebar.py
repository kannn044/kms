import streamlit as st

def show_sidebar():
    """Display sidebar menu based on user role"""
    with st.sidebar:
        st.write(f"Welcome, {st.session_state['user_fullname']}")
        st.write(f"Role: {st.session_state['user_role'].capitalize()}")
        
        # Build menu based on user role
        menu_options = ["Home", "Add Knowledge", "Search", "Profile"]
        
        if st.session_state['user_role'] == 'admin':
            menu_options.extend(["Manage Knowledge", "User Management"])
            
        choice = st.selectbox("Menu", menu_options)
        
        # Show application version
        st.markdown("---")
        st.caption("Version 1.0.0")
        
        # Logout button
        if st.button("Logout", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()()
            
        return choice