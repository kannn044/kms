import streamlit as st
import os
from modules.knowledge import search_knowledge_items, semantic_search_with_details, get_categories
from config import DEFAULT_TOP_K

def show_search_page():
    """Display search page with keyword and semantic search options"""
    st.subheader("Search Knowledge Base")
    
    # กำหนดค่าเริ่มต้นใน session state
    if 'active_tab' not in st.session_state:
        st.session_state['active_tab'] = 0
    
    # สร้างแท็บด้วย simple tab implementation
    tab_titles = ["Keyword Search", "Semantic Search"]
    selected_tab = tab_titles[st.session_state['active_tab']]
    
    # สร้างแถบแท็บด้วย HTML/CSS แทน
    tabs_html = f"""
    <style>
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1px;
        margin-bottom: 1rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 40px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-size: 16px;
    }}
    </style>
    """
    st.markdown(tabs_html, unsafe_allow_html=True)
    
    # สร้างแท็บแบบ manual
    cols = st.columns(len(tab_titles))
    for i, title in enumerate(tab_titles):
        if cols[i].button(
            title, 
            key=f"tab_{i}",
            type="secondary" if i != st.session_state['active_tab'] else "primary",
            use_container_width=True
        ):
            st.session_state['active_tab'] = i
            st.rerun()
    
    # แสดงเนื้อหาตามแท็บที่เลือก
    if st.session_state['active_tab'] == 0:
        # Keyword Search Tab
        show_keyword_search_tab()
    else:
        # Semantic Search Tab
        show_semantic_search_tab()

def show_keyword_search_tab():
    """Display keyword search form"""
    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("Search by keywords (title, content or tags)", key="keyword_input")
        
    with col2:
        categories = ["All Categories"] + get_categories()
        category = st.selectbox("Filter by Category", categories, key="keyword_category")
    
    if st.button("Search", key="keyword_search_btn"):
        with st.spinner("Searching..."):
            filtered_category = None if category == "All Categories" else category
            results = search_knowledge_items(keyword, filtered_category)
            
            if results:
                st.success(f"Found {len(results)} results")
                display_search_results(results)
            else:
                st.info("No results found for your query")

def show_semantic_search_tab():
    """Display semantic search form"""
    query = st.text_input("Describe what you're looking for in natural language", key="semantic_input")
    top_k = st.slider("Number of results", min_value=1, max_value=20, value=5, key="semantic_slider")
    
    # Container for search progress
    search_progress = st.empty()
    
    if st.button("Semantic Search", key="semantic_search_btn"):
        if not query:
            st.warning("Please enter a search query")
            return
            
        with search_progress.container():
            # สร้าง progress bar
            progress = st.progress(0)
            status_text = st.empty()
            
            # แสดงขั้นตอนการทำงาน
            stages = [
                "Analyzing your query...",
                "Converting to vector embedding...",
                "Searching knowledge base...",
                "Calculating similarity scores...",
                "Preparing results..."
            ]
            
            # จำลองการประมวลผล
            for i, stage in enumerate(stages):
                status_text.text(stage)
                progress.progress((i+1)/len(stages))
                import time
                time.sleep(0.5)  # หน่วงเวลาเล็กน้อย
            
            try:
                results = semantic_search_with_details(query, top_k)
                
                if results:
                    st.success(f"Found {len(results)} semantically similar results")
                    
                    # แสดงผล
                    for item, score in results:
                        similarity = (1 - score) * 100
                        with st.expander(f"{item['title']} ({item['category']}) - Similarity: {similarity:.1f}%"):
                            st.markdown(f"**Content:** {item['content'][:500]}...")
                            st.markdown(f"**Tags:** {item['tags']}")
                            st.markdown(f"**Created:** {item['created_date']}")
                            
                            # แสดงไฟล์แนบ
                            if item['file_path'] and os.path.exists(item['file_path']):
                                display_attachment(item['file_path'])
                else:
                    st.info("No semantically similar results found")
            except Exception as e:
                st.error(f"Error during semantic search: {e}")
                st.info("If this is your first time using semantic search, try adding some knowledge items first.")

def display_search_results(results):
    """Helper function to display search results"""
    for item in results:
        with st.expander(f"{item['title']} ({item['category']})"):
            st.write(f"**Content:** {item['content']}")
            st.write(f"**Tags:** {item['tags']}")
            st.write(f"**Created:** {item['created_date']}")
            st.write(f"**Last Updated:** {item['last_updated']}")
            author_name = item['full_name'] or item['username']
            st.write(f"**Author:** {author_name}")
            
            # Handle file attachment
            if item['file_path']:
                display_attachment(item['file_path'])

def display_attachment(file_path):
    """Helper function to display file attachment download button"""
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            btn = st.download_button(
                label="Download Attached File",
                data=file,
                file_name=file_name
            )
    else:
        st.error("Attached file not found")