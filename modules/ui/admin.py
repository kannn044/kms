import streamlit as st
import pandas as pd
from modules.users import (
    get_pending_users,
    get_all_users,
    update_user_status,
    update_user_role
)

def show_user_management_page():
    """Display admin user management interface"""
    st.subheader("User Management")
    
    # Create tabs for different sections
    admin_tabs = st.tabs(["Pending Approvals", "All Users", "System Stats"])
    
    # Tab 1: Pending Approvals
    with admin_tabs[0]:
        show_pending_approvals()
    
    # Tab 2: All Users
    with admin_tabs[1]:
        show_all_users()
    
    # Tab 3: System Stats
    with admin_tabs[2]:
        show_system_stats()

def show_pending_approvals():
    """Display pending user approval requests"""
    st.header("Pending User Approvals")
    pending_users = get_pending_users()
    
    if pending_users:
        st.info(f"You have {len(pending_users)} pending approval requests")
        
        for user in pending_users:
            with st.expander(f"User: {user['username']} ({user['email']})"):
                st.write(f"**Full Name:** {user['full_name']}")
                st.write(f"**Email:** {user['email']}")
                st.write(f"**Requested on:** {user['created_date']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve {user['username']}", key=f"approve_{user['id']}"):
                        success, message = update_user_status(user['id'], "approved")
                        if success:
                            st.success(f"User {user['username']} has been approved")
                            st.rerun()()
                        else:
                            st.error(message)
                
                with col2:
                    if st.button(f"Reject {user['username']}", key=f"reject_{user['id']}"):
                        success, message = update_user_status(user['id'], "rejected")
                        if success:
                            st.success(f"User {user['username']} has been rejected")
                            st.rerun()()
                        else:
                            st.error(message)
    else:
        st.success("No pending approval requests")

def show_all_users():
    """Display and manage all users"""
    st.header("Manage All Users")
    all_users = get_all_users()
    
    if all_users:
        # Filter out admin user from display list
        filtered_users = []
        for user in all_users:
            # Don't show current admin in the list
            if user['username'] != 'admin' and user['id'] != st.session_state['user_id']:
                filtered_users.append({
                    "ID": user['id'],
                    "Username": user['username'],
                    "Email": user['email'],
                    "Full Name": user['full_name'],
                    "Role": user['role'],
                    "Status": user['status'],
                    "Created": user['created_date']
                })
        
        if filtered_users:
            # Show table of users
            df = pd.DataFrame(filtered_users)
            st.dataframe(df)
            
            st.subheader("Change User Role/Status")
            
            # Select user to modify
            selected_user_id = st.selectbox(
                "Select User",
                options=[user["ID"] for user in filtered_users],
                format_func=lambda x: next((f"{user['Username']} ({user['Email']})" 
                                          for user in filtered_users if user["ID"] == x), "")
            )
            
            # Get selected user data
            selected_user = next((user for user in filtered_users if user["ID"] == selected_user_id), None)
            
            if selected_user:
                col1, col2 = st.columns(2)
                
                # Change role
                with col1:
                    new_role = st.selectbox(
                        "Change Role",
                        options=["user", "admin"],
                        index=0 if selected_user["Role"] == "user" else 1
                    )
                    
                    if st.button("Update Role"):
                        success, message = update_user_role(selected_user_id, new_role)
                        if success:
                            st.success(f"User role updated to {new_role}")
                            st.rerun()()
                        else:
                            st.error(message)
                
                # Change status
                with col2:
                    new_status = st.selectbox(
                        "Change Status",
                        options=["pending", "approved", "rejected"],
                        index=0 if selected_user["Status"] == "pending" else 
                             (1 if selected_user["Status"] == "approved" else 2)
                    )
                    
                    if st.button("Update Status"):
                        success, message = update_user_status(selected_user_id, new_status)
                        if success:
                            st.success(f"User status updated to {new_status}")
                            st.rerun()()
                        else:
                            st.error(message)
        else:
            st.info("No users to manage")
    else:
        st.info("No users found")

def show_system_stats():
    """Display system statistics"""
    st.header("System Statistics")
    
    # Import only when needed to avoid circular imports
    from modules.knowledge import get_knowledge_stats
    from modules.database import get_db_connection
    
    # Get stats
    knowledge_stats = get_knowledge_stats()
    
    # Get user stats
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM users WHERE status='approved'")
    active_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE status='pending'")
    pending_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    admin_users = c.fetchone()[0]
    
    conn.close()
    
    # Display stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Knowledge Base")
        st.metric("Total Knowledge Items", knowledge_stats["total_items"])
        st.metric("Categories", knowledge_stats["total_categories"])
        st.metric("Contributors", knowledge_stats["total_contributors"])
    
    with col2:
        st.subheader("Users")
        st.metric("Active Users", active_users)
        st.metric("Pending Approvals", pending_users)
        st.metric("Administrators", admin_users)