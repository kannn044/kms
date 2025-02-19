import streamlit as st
from modules.users import get_user, update_user_profile, get_user_contributions
from modules.auth import validate_password, validate_email
import time

def show_profile_page():
    """Display user profile and settings"""
    st.subheader("Your Profile")
    
    # Get current user data
    user = get_user(st.session_state['user_id'])
    
    if not user:
        st.error("Failed to load user profile")
        return
    
    # Create tabs for profile sections
    profile_tabs = st.tabs(["Profile Settings", "My Contributions", "Account Security"])
    
    # Tab 1: Profile Settings
    with profile_tabs[0]:
        show_profile_settings(user)
    
    # Tab 2: User Contributions
    with profile_tabs[1]:
        show_user_contributions(user['id'])
    
    # Tab 3: Account Security
    with profile_tabs[2]:
        show_security_settings(user)

def show_profile_settings(user):
    """Display and handle profile information tab"""
    st.header("Basic Information")
    
    # ใช้ form แทนปุ่มเดี่ยวเพื่อให้ทำงานทันที
    with st.form("profile_update_form"):
        username = st.text_input("Username", value=user['username'], disabled=True)
        email = st.text_input("Email", value=user['email'])
        full_name = st.text_input("Full Name", value=user['full_name'])
        
        # ปุ่ม submit form
        update_clicked = st.form_submit_button("Update Profile", use_container_width=True)
    
    # สร้าง placeholder สำหรับแสดงสถานะ
    status_placeholder = st.empty()
    
    # จัดการเมื่อกดปุ่ม
    if update_clicked:
        with status_placeholder.container():
            # แสดง progress
            with st.spinner("Updating profile..."):
                progress_bar = st.progress(0)
                
                for i in range(4):
                    progress_bar.progress((i+1)/4)
                    time.sleep(0.2)
                
                # เรียกฟังก์ชันอัปเดตโปรไฟล์
                success, message = update_user_profile(user['id'], email, full_name)
                
                if success:
                    # อัปเดต session state
                    st.session_state['user_fullname'] = full_name
                    progress_bar.progress(1.0)
                    st.success("✅ Profile updated successfully!")
                else:
                    st.error(f"❌ {message}")

def show_user_contributions(user_id):
    """Display user's knowledge contributions"""
    contributions = get_user_contributions(user_id)
    
    st.write("### Your Knowledge Contributions")
    
    if contributions:
        st.write(f"Total contributions: {len(contributions)}")
        
        for item in contributions:
            with st.expander(f"{item['title']} - {item['created_date']}"):
                st.write(f"**Category:** {item['category']}")
                st.write(f"**Last updated:** {item['last_updated']}")
                st.write(f"**ID:** {item['id']}")
                
                # Link to edit
                if st.button("Edit This Item", key=f"edit_{item['id']}"):
                    # Store ID in session and redirect to manage page
                    st.session_state["edit_id"] = item['id']
                    st.session_state["redirect_to_manage"] = True
                    st.rerun()()
    else:
        st.info("You haven't contributed any knowledge items yet.")
        if st.button("Add Your First Knowledge Item"):
            # Redirect to add knowledge page
            st.session_state["sidebar_selection"] = "Add Knowledge"
            st.rerun()()

def show_security_settings(user):
    """Display and handle security settings tab"""
    st.header("Change Password")
    
    # เพิ่ม session state สำหรับติดตามสถานะการเปลี่ยนรหัสผ่าน
    if 'is_changing_password' not in st.session_state:
        st.session_state['is_changing_password'] = False
    
    # สร้าง placeholder สำหรับแสดงข้อความ loading
    password_status = st.empty()
    
    with st.form("password_form"):
        st.write("Leave blank if you don't want to change your password")
        
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        submit_button = st.form_submit_button("Change Password")
    
    if submit_button:
        # ตรวจสอบข้อมูล
        if not current_password:
            password_status.error("Current password is required to change password")
            return
            
        if not new_password:
            password_status.error("New password cannot be empty")
            return
            
        if new_password != confirm_password:
            password_status.error("New passwords do not match")
            return
        
        # กำหนดสถานะว่ากำลังเปลี่ยนรหัสผ่าน
        st.session_state['is_changing_password'] = True
        
        # แสดง loading
        with password_status.container():
            with st.spinner("Changing your password..."):
                # แสดงความคืบหน้า
                progress = st.progress(0)
                
                # ขั้นตอนที่ 1: ตรวจสอบรหัสผ่านปัจจุบัน
                progress.progress(0.25)
                st.text("Verifying current password...")
                
                # ขั้นตอนที่ 2: ตรวจสอบความปลอดภัยของรหัสผ่านใหม่
                progress.progress(0.5)
                st.text("Validating new password strength...")
                
                # ขั้นตอนที่ 3: อัปเดตรหัสผ่าน
                progress.progress(0.75)
                st.text("Updating password...")
                
                # ทำการเปลี่ยนรหัสผ่าน
                import time
                time.sleep(0.5)  # จำลองการประมวลผล
                success, message = update_user_profile(
                    user['id'], 
                    user['email'], 
                    user['full_name'],
                    current_password,
                    new_password
                )
                
                # แสดงผลลัพธ์
                progress.progress(1.0)
                if success:
                    st.success("✅ Password changed successfully!")
                else:
                    st.error(f"❌ {message}")
                
                # รีเซ็ตสถานะ
                st.session_state['is_changing_password'] = False