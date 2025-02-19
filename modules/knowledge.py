import os
import uuid
from datetime import datetime
from modules.database import get_db_connection
from modules.vectorstore import add_to_vectorstore, rebuild_vectorstore
from config import UPLOAD_FOLDER

def add_knowledge_item(title, content, category, tags, author_id, uploaded_file=None):
    """Add a new knowledge item and index it in vector store"""
    conn = get_db_connection()
    c = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = None
    
    # Save file if uploaded
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)
    
    try:
        # Insert into database
        c.execute(
            "INSERT INTO knowledge_items (title, content, category, tags, created_date, last_updated, author_id, file_path, vector_indexed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (title, content, category, tags, current_time, current_time, author_id, file_path, 0)
        )
        conn.commit()
        
        # Get the ID of the newly inserted item
        c.execute("SELECT last_insert_rowid()")
        doc_id = c.fetchone()[0]
        
        # Add to vector store
        add_to_vectorstore(doc_id, title, content, category, tags)
        
        # Update indexed status
        c.execute("UPDATE knowledge_items SET vector_indexed = 1 WHERE id = ?", (doc_id,))
        conn.commit()
        conn.close()
        
        return True, doc_id
    except Exception as e:
        conn.close()
        return False, str(e)

def update_knowledge_item(item_id, title, content, category, tags, uploaded_file=None):
    """Update an existing knowledge item and reindex it"""
    conn = get_db_connection()
    c = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Get current file path if exists
        c.execute("SELECT file_path FROM knowledge_items WHERE id = ?", (item_id,))
        result = c.fetchone()
        current_file_path = result['file_path'] if result else None
        
        file_path = current_file_path
        
        # Handle file upload if provided
        if uploaded_file:
            # Delete old file if exists
            if current_file_path and os.path.exists(current_file_path):
                os.remove(current_file_path)
            
            # Save new file
            file_path = save_uploaded_file(uploaded_file)
        
        # Update database
        if file_path:
            c.execute(
                "UPDATE knowledge_items SET title=?, content=?, category=?, tags=?, last_updated=?, file_path=?, vector_indexed=? WHERE id=?",
                (title, content, category, tags, current_time, file_path, 0, item_id)
            )
        else:
            c.execute(
                "UPDATE knowledge_items SET title=?, content=?, category=?, tags=?, last_updated=?, vector_indexed=? WHERE id=?",
                (title, content, category, tags, current_time, 0, item_id)
            )
        conn.commit()
        
        # Update vector store
        add_to_vectorstore(item_id, title, content, category, tags)
        
        # Update indexed status
        c.execute("UPDATE knowledge_items SET vector_indexed = 1 WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        
        return True, "Knowledge item updated successfully"
    except Exception as e:
        conn.close()
        return False, str(e)

def delete_knowledge_item(item_id):
    """Delete a knowledge item and rebuild the vector store"""
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        # Get file path if exists
        c.execute("SELECT file_path FROM knowledge_items WHERE id = ?", (item_id,))
        result = c.fetchone()
        file_path = result['file_path'] if result else None
        
        # Delete file if exists
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        c.execute("DELETE FROM knowledge_items WHERE id = ?", (item_id,))
        conn.commit()
        
        # Get all remaining items to rebuild vector store
        c.execute("SELECT id, title, content, category, tags FROM knowledge_items")
        all_items = [dict(row) for row in c.fetchall()]
        conn.close()
        
        # Rebuild vector store
        rebuild_vectorstore(all_items)
        
        return True, "Knowledge item deleted successfully"
    except Exception as e:
        conn.close()
        return False, str(e)

def get_knowledge_item(item_id):
    """Get a knowledge item by ID with author details"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("""
    SELECT k.*, u.username, u.full_name 
    FROM knowledge_items k
    LEFT JOIN users u ON k.author_id = u.id
    WHERE k.id = ?
    """, (item_id,))
    
    result = c.fetchone()
    conn.close()
    
    return dict(result) if result else None

def search_knowledge_items(search_term=None, category=None, limit=None):
    """Search knowledge items by keyword"""
    conn = get_db_connection()
    c = conn.cursor()
    
    query = """
    SELECT k.*, u.username, u.full_name 
    FROM knowledge_items k
    LEFT JOIN users u ON k.author_id = u.id
    WHERE 1=1
    """
    params = []
    
    if search_term:
        query += " AND (k.title LIKE ? OR k.content LIKE ? OR k.tags LIKE ?)"
        term = f"%{search_term}%"
        params.extend([term, term, term])
    
    if category and category != "All Categories":
        query += " AND k.category = ?"
        params.append(category)
    
    query += " ORDER BY k.last_updated DESC"
    
    if limit:
        query += f" LIMIT {limit}"
    
    c.execute(query, params)
    results = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return results

def semantic_search_with_details(query, top_k=5):
    """Perform semantic search and get full item details"""
    from modules.vectorstore import semantic_search
    
    # Get semantic search results
    search_results = semantic_search(query, top_k)
    
    # Get full details for each result
    detailed_results = []
    for doc, score in search_results:
        doc_id = doc.metadata["id"]
        item = get_knowledge_item(doc_id)
        if item:
            detailed_results.append((item, score))
    
    return detailed_results

def get_categories():
    """Get all unique categories"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT DISTINCT category FROM knowledge_items ORDER BY category")
    categories = [row['category'] for row in c.fetchall()]
    conn.close()
    
    return categories

def get_knowledge_stats():
    """Get statistics about knowledge items"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Total items
    c.execute("SELECT COUNT(*) as count FROM knowledge_items")
    total_items = c.fetchone()['count']
    
    # Total categories
    c.execute("SELECT COUNT(DISTINCT category) as count FROM knowledge_items")
    total_categories = c.fetchone()['count']
    
    # Total contributors
    c.execute("SELECT COUNT(DISTINCT author_id) as count FROM knowledge_items")
    total_contributors = c.fetchone()['count']
    
    conn.close()
    
    return {
        "total_items": total_items,
        "total_categories": total_categories,
        "total_contributors": total_contributors
    }

def save_uploaded_file(uploaded_file):
    """Save an uploaded file and return the path"""
    if uploaded_file is None:
        return None
        
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Create unique filename
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return file_path