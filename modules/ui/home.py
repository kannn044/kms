import streamlit as st
from modules.knowledge import get_knowledge_stats, search_knowledge_items
from modules.ui.styles import inject_global_css, render_page_header, render_metric_card, render_knowledge_card, render_empty_state

def show_home_page():
    """Display a modern dashboard home page."""
    inject_global_css()

    # Welcome header
    fullname = st.session_state.get('user_fullname', 'User')
    render_page_header(
        title=f"Welcome back, {fullname}!",
        subtitle="Your organization's knowledge base at a glance",
        icon="📚"
    )

    # Statistics
    stats = get_knowledge_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_metric_card("📄", stats["total_items"], "Knowledge Items"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("📂", stats["total_categories"], "Categories"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("👥", stats["total_contributors"], "Contributors"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick actions
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="color: #E8ECF1; font-weight: 600; margin-bottom: 1rem;">⚡ Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)

    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        if st.button("➕  Add Knowledge", use_container_width=True):
            st.session_state["sidebar_selection"] = "Add Knowledge"
    with qa_col2:
        if st.button("🔍  Search", use_container_width=True):
            st.session_state["sidebar_selection"] = "Search"
    with qa_col3:
        if st.button("👤  My Profile", use_container_width=True):
            st.session_state["sidebar_selection"] = "Profile"

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent additions
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="color: #E8ECF1; font-weight: 600;">🕐 Recent Additions</h3>
    </div>
    """, unsafe_allow_html=True)

    recent_items = search_knowledge_items(limit=5)

    if recent_items:
        for item in recent_items:
            preview = item['content'][:150] + "..." if len(item['content']) > 150 else item['content']
            author_name = item.get('full_name') or item.get('username', 'Unknown')
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
    else:
        st.markdown(
            render_empty_state("📝", "No knowledge items yet", "Be the first to contribute!"),
            unsafe_allow_html=True
        )

    # Help section
    with st.expander("📘 Quick Help"):
        st.markdown("""
        ### How to use the Knowledge Management System:

        1. **➕ Add Knowledge** — Share your expertise by adding new items
        2. **🔍 Search** — Find information using keywords or AI-powered semantic search
        3. **📂 Categories** — Organize knowledge by category for easy access
        4. **📎 Files** — Attach documents, images or other files to your knowledge items

        Need more help? Contact your administrator.
        """)