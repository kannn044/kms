import streamlit as st
import pandas as pd
import time
import os
from modules.knowledge import (
    add_knowledge_item, 
    update_knowledge_item, 
    delete_knowledge_item,
    get_knowledge_item,
    search_knowledge_items,
    get_categories
)
from modules.vectorstore import add_to_vectorstore

def show_add_knowledge_page(conn):
    """Display form to add new knowledge with OCR capability"""
    if conn is None:
        from modules.database import get_db_connection
        conn = get_db_connection()
        
    st.subheader("Add New Knowledge")
    
    # เพิ่ม tabs สำหรับเลือกวิธีเพิ่ม knowledge
    add_tabs = st.tabs(["Manual Entry", "Extract from File (OCR)"])
    
    # ========================= TAB 1: MANUAL ENTRY =========================
    with add_tabs[0]:
        show_manual_entry_form(conn)
    
    # ========================= TAB 2: OCR EXTRACTION =========================
    with add_tabs[1]:
        show_ocr_extraction_form(conn)

def show_manual_entry_form(conn):
    """แสดงฟอร์มสำหรับกรอกข้อมูลด้วยตนเอง"""
    with st.form("manual_knowledge_form"):
        title = st.text_input("Title*")
        content = st.text_area("Content*", height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            existing_categories = get_categories()
            default_categories = ["General", "Technical", "Process", "Project", "Research"]
            category_options = list(set(default_categories + existing_categories))
            category = st.selectbox("Category*", category_options)
        
        with col2:
            tags = st.text_input("Tags (comma separated)")
        
        uploaded_file = st.file_uploader("Attach File (optional)", 
                                        type=["pdf", "docx", "xlsx", "txt", "jpg", "png", "jpeg"])
        
        submit_button = st.form_submit_button("Save")
    
    if submit_button:
        if not title or not content or not category:
            st.error("Title, Content and Category are required")
            return
            
        with st.spinner("Saving and indexing knowledge..."):
            # แสดงความคืบหน้า
            progress = st.progress(0)
            status_text = st.empty()
            
            # ขั้นตอนที่ 1: บันทึกข้อมูล
            status_text.text("Saving content and metadata...")
            progress.progress(30)
            time.sleep(0.5)  # จำลองการประมวลผล
            
            # ขั้นตอนที่ 2: สร้าง vector embeddings
            status_text.text("Creating vector embeddings...")
            progress.progress(60)
            time.sleep(0.5)  # จำลองการประมวลผล
            
            # ขั้นตอนที่ 3: อัพเดต vector database
            status_text.text("Updating vector database...")
            progress.progress(90)
            time.sleep(0.5)  # จำลองการประมวลผล
            
            # บันทึกข้อมูล
            author_id = st.session_state['user_id']
            success, result = add_knowledge_item(title, content, category, tags, author_id, uploaded_file)
            
            if success:
                progress.progress(100)
                status_text.success("✅ Knowledge Added Successfully!")
                time.sleep(1)
                st.rerun()
            else:
                progress.empty()
                st.error(f"Failed to add knowledge: {result}")

def show_ocr_extraction_form(conn):
    """แสดงฟอร์มสำหรับสกัดข้อความจากไฟล์ด้วย OCR"""
    try:
        import pytesseract
        from PIL import Image
        import io
        import fitz  # PyMuPDF
        import docx
    except ImportError:
        st.error("""
        Missing required libraries. Please install:
        ```
        pip install pytesseract pillow pymupdf python-docx
        ```
        And install Tesseract OCR engine for your operating system.
        """)
        return
    
    st.write("### Extract Text from Files")
    st.info("Upload an image or document to extract text using OCR technology.")
    
    # รับไฟล์ที่อัปโหลด
    uploaded_ocr_file = st.file_uploader(
        "Upload a file for text extraction", 
        type=["jpg", "jpeg", "png", "pdf", "docx"],
        key="ocr_file_uploader"
    )
    
    # placeholder สำหรับข้อความที่สกัดได้
    extracted_text = ""
    extracted_title = ""
    ocr_status = st.empty()
    ocr_progress = st.empty()
    extracted_content = st.empty()
    
    if uploaded_ocr_file:
        with st.spinner("Processing file..."):
            progress_bar = ocr_progress.progress(0)
            ocr_status.info("Analyzing file type...")
            time.sleep(0.5)  # จำลองการประมวลผล
            
            # สกัดข้อความตามประเภทไฟล์
            file_extension = uploaded_ocr_file.name.split('.')[-1].lower()
            
            try:
                # 1. ประมวลผลไฟล์รูปภาพ
                if file_extension in ['jpg', 'jpeg', 'png']:
                    ocr_status.info("Performing OCR on image...")
                    progress_bar.progress(30)
                    
                    image = Image.open(uploaded_ocr_file)
                    try:
                        extracted_text = pytesseract.image_to_string(image, lang='tha+eng')
                    except:
                        # หากไม่สามารถใช้ภาษาไทยได้ ให้ใช้ภาษาอังกฤษอย่างเดียว
                        extracted_text = pytesseract.image_to_string(image)
                    
                    progress_bar.progress(80)
                    
                # 2. ประมวลผลไฟล์ PDF
                elif file_extension == 'pdf':
                    ocr_status.info("Extracting text from PDF...")
                    progress_bar.progress(20)
                    
                    pdf_bytes = uploaded_ocr_file.read()
                    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                    
                    total_pages = len(pdf_document)
                    all_text = []
                    
                    for i, page in enumerate(pdf_document):
                        text = page.get_text()
                        all_text.append(text)
                        progress_value = 20 + int(60 * (i + 1) / total_pages)
                        progress_bar.progress(progress_value)
                        ocr_status.info(f"Processing page {i+1} of {total_pages}...")
                        time.sleep(0.2)  # จำลองการประมวลผล
                    
                    extracted_text = "\n\n".join(all_text)
                
                # 3. ประมวลผลไฟล์ Word
                elif file_extension == 'docx':
                    ocr_status.info("Extracting text from Word document...")
                    progress_bar.progress(30)
                    
                    doc = docx.Document(io.BytesIO(uploaded_ocr_file.read()))
                    all_paragraphs = []
                    
                    total_paras = len(doc.paragraphs)
                    for i, para in enumerate(doc.paragraphs):
                        if para.text:
                            all_paragraphs.append(para.text)
                        if i % 10 == 0:  # อัพเดตทุก 10 ย่อหน้า
                            progress_value = 30 + int(50 * (i + 1) / total_paras)
                            progress_bar.progress(progress_value)
                    
                    extracted_text = "\n\n".join(all_paragraphs)
                
                # แสดงข้อความที่สกัดได้
                progress_bar.progress(90)
                ocr_status.info("Text extraction complete!")
                
                if extracted_text:
                    # ลองสกัดชื่อเรื่องจากบรรทัดแรก
                    lines = extracted_text.split('\n')
                    extracted_title = next((line for line in lines if line.strip()), "")
                    if len(extracted_title) > 70:
                        extracted_title = extracted_title[:67] + "..."
                        
                    progress_bar.progress(100)
                    ocr_status.success("✅ Text successfully extracted!")
                else:
                    ocr_status.warning("No text could be extracted from this file.")
                    
            except Exception as e:
                ocr_status.error(f"Error extracting text: {e}")
                progress_bar.empty()
    
    # แสดงฟอร์มสำหรับแก้ไข/ยืนยันข้อมูลก่อนบันทึก
    if extracted_text:
        with st.form("ocr_knowledge_form"):
            st.subheader("Review and Edit Extracted Content")
            
            title = st.text_input("Title*", value=extracted_title)
            content = st.text_area("Content*", value=extracted_text, height=300)
            
            col1, col2 = st.columns(2)
            with col1:
                existing_categories = get_categories()
                default_categories = ["General", "Technical", "Process", "Project", "Research"]
                category_options = list(set(default_categories + existing_categories))
                category = st.selectbox("Category*", category_options, key="ocr_category")
            
            with col2:
                tags = st.text_input("Tags (comma separated)", key="ocr_tags")
            
            # ตัวเลือกเก็บไฟล์ต้นฉบับ
            keep_original = st.checkbox("Attach original file", value=True)
            
            submit_ocr = st.form_submit_button("Save Knowledge")
        
        if submit_ocr:
            if not title or not content or not category:
                st.error("Title, Content and Category are required")
                return
                
            with st.spinner("Saving extracted knowledge..."):
                # แสดงความคืบหน้า
                save_progress = st.progress(0)
                save_status = st.empty()
                
                save_status.text("Processing content...")
                save_progress.progress(30)
                time.sleep(0.5)  # จำลองการประมวลผล
                
                save_status.text("Creating vector embeddings...")
                save_progress.progress(60)
                time.sleep(0.5)  # จำลองการประมวลผล
                
                # เตรียมไฟล์แนบ (ถ้าเลือกเก็บไฟล์ต้นฉบับ)
                file_to_attach = uploaded_ocr_file if keep_original else None
                
                # บันทึกข้อมูล
                author_id = st.session_state['user_id']
                success, result = add_knowledge_item(title, content, category, tags, author_id, file_to_attach)
                
                if success:
                    save_progress.progress(100)
                    save_status.success("✅ Knowledge Added Successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    save_progress.empty()
                    st.error(f"Failed to add knowledge: {result}")

def show_manage_knowledge_page():
    """Display interface to manage knowledge items"""
    st.subheader("Manage Knowledge Items")
    
    # ค้นหาข้อมูลทั้งหมด
    all_items = search_knowledge_items()
    
    if all_items:
        # สร้างตาราง DataFrame สำหรับแสดงข้อมูล
        df_data = []
        for item in all_items:
            df_data.append({
                "ID": item['id'],
                "Title": item['title'],
                "Category": item['category'], 
                "Updated": item['last_updated'],
                "Author": item['full_name'] or item['username']
            })
        
        df = pd.DataFrame(df_data)
        
        # แสดงตาราง
        st.dataframe(df)
        
        # เลือกรายการที่ต้องการจัดการ
        item_id = st.number_input("Select Item ID to Edit/Delete", 
                                  min_value=1, 
                                  max_value=int(df["ID"].max()) if len(df) > 0 else 1)
        
        if st.button("Load Item"):
            item = get_knowledge_item(item_id)
            if item:
                # Store in session state
                st.session_state["edit_id"] = item['id']
                st.session_state["edit_title"] = item['title']
                st.session_state["edit_content"] = item['content']
                st.session_state["edit_category"] = item['category']
                st.session_state["edit_tags"] = item['tags']
                st.session_state["edit_file_path"] = item['file_path']
                st.experimental_rerun()
            else:
                st.error("Item not found")
        
        # Edit form (shown only when an item is loaded)
        if "edit_id" in st.session_state:
            show_edit_form()
    else:
        st.info("No knowledge items found in the database")

def show_edit_form():
    """Display form to edit a knowledge item"""
    st.subheader("Edit Knowledge Item")
    
    with st.form("edit_knowledge_form"):
        edit_title = st.text_input("Title", value=st.session_state["edit_title"])
        edit_content = st.text_area("Content", value=st.session_state["edit_content"], height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            # Get categories
            existing_categories = get_categories()
            default_categories = ["General", "Technical", "Process", "Project", "Research"]
            category_options = list(set(default_categories + existing_categories))
            
            # Find index of current category
            try:
                category_index = category_options.index(st.session_state["edit_category"])
            except ValueError:
                category_index = 0
                
            edit_category = st.selectbox("Category", category_options, index=category_index)
        
        with col2:
            edit_tags = st.text_input("Tags", value=st.session_state["edit_tags"] or "")
        
        # Display current file if exists
        if st.session_state["edit_file_path"]:
            file_name = st.session_state["edit_file_path"].split("/")[-1]
            st.write(f"Current file: {file_name}")
        
        # Option to upload new file
        new_file = st.file_uploader("Replace File (optional)", 
                                   type=["pdf", "docx", "xlsx", "txt", "jpg", "png"])
        
        col1, col2 = st.columns(2)
        with col1:
            update_button = st.form_submit_button("Update")
        
        with col2:
            delete_button = st.form_submit_button("Delete", type="primary")
    
    # Handle update
    if update_button:
        if not edit_title or not edit_content or not edit_category:
            st.error("Title, Content and Category are required")
            return
            
        with st.spinner("Updating and re-indexing knowledge..."):
            # แสดงความคืบหน้า
            progress = st.progress(0)
            status = st.empty()
            
            status.text("Updating content...")
            progress.progress(30)
            time.sleep(0.5)  # จำลองการประมวลผล
            
            status.text("Updating vector embeddings...")
            progress.progress(60)
            time.sleep(0.5)  # จำลองการประมวลผล
            
            success, message = update_knowledge_item(
                st.session_state["edit_id"],
                edit_title,
                edit_content,
                edit_category,
                edit_tags,
                new_file
            )
            
            if success:
                progress.progress(100)
                status.success("Knowledge Updated Successfully!")
                # Clear session state
                for key in list(st.session_state.keys()):
                    if key.startswith("edit_"):
                        del st.session_state[key]
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Failed to update: {message}")
    
    # Handle delete
    if delete_button:
        with st.spinner("Deleting knowledge and rebuilding index..."):
            progress = st.progress(0)
            status = st.empty()
            
            status.text("Removing knowledge entry...")
            progress.progress(40)
            time.sleep(0.5)  # จำลองการประมวลผล
            
            status.text("Rebuilding vector index...")
            progress.progress(70)
            time.sleep(0.5)  # จำลองการประมวลผล
            
            success, message = delete_knowledge_item(st.session_state["edit_id"])
            
            if success:
                progress.progress(100)
                status.success("Knowledge Deleted Successfully!")
                # Clear session state
                for key in list(st.session_state.keys()):
                    if key.startswith("edit_"):
                        del st.session_state[key]
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Failed to delete: {message}")