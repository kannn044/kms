import streamlit as st
import os
import time
from modules.knowledge import search_knowledge_items, semantic_search_with_details, get_categories
from modules.ui.styles import (
    inject_global_css, render_page_header, render_knowledge_card,
    render_empty_state, render_badge, render_score_bar
)
from config import DEFAULT_TOP_K


def show_search_page():
    """Display a modern search page with keyword and semantic tabs."""
    inject_global_css()

    render_page_header(
        title="Search Knowledge Base",
        subtitle="Find information using keywords or AI-powered semantic search",
        icon="🔍"
    )

    # Tabs (using native Streamlit tabs)
    tab_keyword, tab_semantic = st.tabs(["🔤 Keyword Search", "🧠 Semantic Search"])

    with tab_keyword:
        show_keyword_search_tab()

    with tab_semantic:
        show_semantic_search_tab()


def show_keyword_search_tab():
    """Keyword-based search form and results."""
    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input(
            "Search by keywords",
            key="keyword_input",
            placeholder="Search titles, content, or tags..."
        )
    with col2:
        categories = ["All Categories"] + get_categories()
        category = st.selectbox("Category", categories, key="keyword_category")

    if st.button("🔍 Search", key="keyword_search_btn", use_container_width=True):
        with st.spinner("Searching..."):
            filtered_category = None if category == "All Categories" else category
            results = search_knowledge_items(keyword, filtered_category)

            if results:
                st.success(f"Found {len(results)} results")
                display_search_results(results)
            else:
                st.markdown(
                    render_empty_state("🔍", "No results found", "Try different keywords or broaden your search"),
                    unsafe_allow_html=True
                )


def show_semantic_search_tab():
    """AI-powered semantic search form and results."""
    query = st.text_input(
        "Describe what you're looking for",
        key="semantic_input",
        placeholder="e.g. 'How to set up the deployment pipeline'"
    )
    top_k = st.slider("Number of results", min_value=1, max_value=20, value=5, key="semantic_slider")

    if st.button("🧠 Semantic Search", key="semantic_search_btn", use_container_width=True):
        if not query:
            st.warning("Please enter a search query")
            return

        # Progress stages
        progress = st.progress(0)
        status_text = st.empty()

        stages = [
            "Analyzing your query...",
            "Converting to vector embedding...",
            "Searching knowledge base...",
            "Calculating similarity scores...",
            "Preparing results..."
        ]

        for i, stage in enumerate(stages):
            status_text.text(f"🔄 {stage}")
            progress.progress((i + 1) / len(stages))
            time.sleep(0.4)

        try:
            results = semantic_search_with_details(query, top_k)
            status_text.empty()
            progress.empty()

            if results:
                st.success(f"Found {len(results)} semantically similar results")

                for item, score in results:
                    similarity = max(0, (1 - score) * 100)

                    with st.expander(f"📄 {item['title']}  —  {similarity:.0f}% match"):
                        # Score bar
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;">
                            <span class="badge badge-category">{item['category']}</span>
                            <span style="color: #8899AA; font-size: 0.85rem;">Similarity: {similarity:.1f}%</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(render_score_bar(similarity), unsafe_allow_html=True)

                        # Content preview
                        content_preview = item['content'][:500]
                        if len(item['content']) > 500:
                            content_preview += "..."
                        st.markdown(f"**Content:** {content_preview}")

                        # Tags
                        if item.get('tags'):
                            tags_html = " ".join([
                                f'<span class="badge badge-tag">{t.strip()}</span>'
                                for t in str(item['tags']).split(",") if t.strip()
                            ])
                            st.markdown(f"**Tags:** {tags_html}", unsafe_allow_html=True)

                        st.markdown(f"**Created:** {item['created_date']}")

                        # File attachment
                        if item.get('file_path') and os.path.exists(item['file_path']):
                            display_attachment(item['file_path'])
            else:
                st.markdown(
                    render_empty_state("🧠", "No similar results found", "Try rephrasing your query"),
                    unsafe_allow_html=True
                )
        except Exception as e:
            status_text.empty()
            progress.empty()
            st.error(f"Error during semantic search: {e}")
            st.info("If this is your first time using semantic search, try adding some knowledge items first.")


def display_search_results(results):
    """Display keyword search results as styled cards."""
    for item in results:
        author_name = item.get('full_name') or item.get('username', 'Unknown')
        preview = item['content'][:200] + "..." if len(item['content']) > 200 else item['content']

        st.markdown(
            render_knowledge_card(
                title=item['title'],
                category=item['category'],
                tags=item.get('tags', ''),
                date=item['last_updated'],
                author=author_name,
                preview=preview
            ),
            unsafe_allow_html=True
        )

        # File attachment
        if item.get('file_path'):
            display_attachment(item['file_path'])


def display_attachment(file_path):
    """Display file attachment download button."""
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        ext = file_name.split('.')[-1].lower() if '.' in file_name else ''
        icon_map = {
            'pdf': '📕', 'docx': '📘', 'doc': '📘', 'xlsx': '📗', 'xls': '📗',
            'txt': '📄', 'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️'
        }
        icon = icon_map.get(ext, '📎')

        with open(file_path, "rb") as file:
            st.download_button(
                label=f"{icon}  Download: {file_name}",
                data=file,
                file_name=file_name,
                use_container_width=True
            )
    else:
        st.warning("📎 Attached file not found")