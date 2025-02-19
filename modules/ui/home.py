import streamlit as st
from modules.knowledge import get_knowledge_stats, search_knowledge_items

def show_home_page():
    """Display home page with dashboard"""
    st.title("Knowledge Management System 📚")
    st.markdown("### Welcome to your organization's knowledge base")
    
    # Get statistics
    stats = get_knowledge_stats()
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Knowledge Items", stats["total_items"])
    with col2:
        st.metric("Categories", stats["total_categories"])
    with col3:
        st.metric("Contributors", stats["total_contributors"])
    
    # Display recent additions
    st.subheader("Recent Additions")
    recent_items = search_knowledge_items(limit=5)
    
    if recent_items:
        for item in recent_items:
            with st.expander(f"{item['title']} ({item['category']})"):
                content_preview = item['content'][:200] + "..." if len(item['content']) > 200 else item['content']
                st.write(f"**Content:** {content_preview}")
                st.write(f"**Tags:** {item['tags']}")
                st.write(f"**Last Updated:** {item['last_updated']}")
                author_name = item['full_name'] or item['username']
                st.write(f"**Author:** {author_name}")
    else:
        st.info("No knowledge items found. Be the first to contribute!")
    
    # Show quick help
    with st.expander("📘 Quick Help"):
        st.markdown("""
        ### How to use the Knowledge Management System:
        
        1. **Add Knowledge**: Share your expertise by adding new knowledge items
        2. **Search**: Find information using keywords or semantic search
        3. **Categories**: Organize knowledge by category for easy access
        4. **Files**: Attach documents, images or other files to your knowledge items
        
        Need more help? Contact your administrator.
        """)