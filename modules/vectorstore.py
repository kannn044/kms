import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from config import VECTORSTORE_PATH, EMBEDDING_MODEL

@st.cache_resource
def get_embeddings():
    """Get the embedding model"""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

@st.cache_resource
def get_vectorstore():
    """Get or create the vector store with improved error handling"""
    try:
        embeddings = get_embeddings()
        vectorstore_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faiss_index")
        
        # ตรวจสอบว่าโฟลเดอร์ faiss_index มีอยู่หรือไม่
        if not os.path.exists(vectorstore_path):
            os.makedirs(vectorstore_path, exist_ok=True)
        
        index_path = os.path.join(vectorstore_path, "index.faiss")
        docstore_path = os.path.join(vectorstore_path, "index.pkl")
        
        # ตรวจสอบว่าไฟล์ index.faiss และ index.pkl มีอยู่จริงหรือไม่
        if os.path.exists(index_path) and os.path.exists(docstore_path):
            try:
                return FAISS.load_local(vectorstore_path, embeddings)
            except Exception as e:
                st.warning(f"Failed to load existing vector store: {e}")
                # สร้างใหม่และบันทึกทันที
                empty_doc = Document(page_content="Initial document", metadata={"id": 0})
                empty_store = FAISS.from_documents([empty_doc], embeddings)
                empty_store.save_local(vectorstore_path)
                return empty_store
        else:
            # สร้างเอกสารเริ่มต้นเพื่อหลีกเลี่ยง list index out of range
            empty_doc = Document(page_content="Initial document", metadata={"id": 0})
            empty_store = FAISS.from_documents([empty_doc], embeddings)
            empty_store.save_local(vectorstore_path)
            return empty_store
    except Exception as e:
        st.error(f"Critical error in get_vectorstore: {e}")
        # ในกรณีที่มีข้อผิดพลาดร้ายแรง ให้สร้าง minimal vectorstore
        embeddings = get_embeddings()
        empty_doc = Document(page_content="Fallback document", metadata={"id": 0})
        return FAISS.from_documents([empty_doc], embeddings)

def add_to_vectorstore(doc_id, title, content, category, tags):
    """Add a document to the vector store with improved error handling"""
    try:
        # สร้าง metadata
        metadata = {
            "id": doc_id,
            "title": title,
            "category": category,
            "tags": tags
        }
        
        # แปลงข้อความเป็น Document object ของ Langchain
        document = Document(page_content=content, metadata=metadata)
        
        # ใช้ try-except แยกสำหรับแต่ละขั้นตอนเพื่อระบุจุดที่เกิดข้อผิดพลาดได้ชัดเจน
        try:
            vectorstore = get_vectorstore()
        except Exception as e:
            st.error(f"Error loading vector store: {e}")
            # สร้าง vectorstore ใหม่เป็นฉบับเปล่าๆ
            try:
                embeddings = get_embeddings()
                vectorstore = FAISS.from_documents([document], embeddings)
                vectorstore_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faiss_index")
                os.makedirs(vectorstore_path, exist_ok=True)
                vectorstore.save_local(vectorstore_path)
                return True
            except Exception as e2:
                st.error(f"Failed to create new vector store: {e2}")
                return False
        
        # เพิ่มเอกสารเข้า vectorstore อย่างปลอดภัย
        try:
            # ถ้ามีเอกสารในคลังอยู่แล้ว ให้ใช้ add_documents
            if len(vectorstore.index_to_docstore_id) > 0:
                vectorstore.add_documents([document])
            # ถ้ายังไม่มีเอกสารใดๆ ให้สร้างใหม่ด้วย from_documents
            else:
                embeddings = get_embeddings()
                vectorstore = FAISS.from_documents([document], embeddings)
        except Exception as e:
            st.error(f"Error adding document to vector store: {e}")
            # ถ้าเกิด list index out of range ให้ลองสร้าง vectorstore ใหม่
            try:
                embeddings = get_embeddings()
                vectorstore = FAISS.from_documents([document], embeddings)
            except Exception as e2:
                st.error(f"Failed to create vector store with new document: {e2}")
                return False
        
        # บันทึก vectorstore
        try:
            vectorstore_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faiss_index")
            os.makedirs(vectorstore_path, exist_ok=True)
            vectorstore.save_local(vectorstore_path)
            return True
        except Exception as e:
            st.error(f"Error saving vector store: {e}")
            return False
            
    except Exception as e:
        st.error(f"Unexpected error in add_to_vectorstore: {e}")
        return False

def semantic_search(query, top_k=5):
    """Search for semantically similar documents"""
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    return results

def rebuild_vectorstore(knowledge_items):
    """Rebuild the entire vector store from scratch"""
    embeddings = get_embeddings()
    documents = []
    
    for item in knowledge_items:
        doc_id = item['id']
        title = item['title']
        content = item['content']
        category = item['category']
        tags = item['tags']
        
        metadata = {
            "id": doc_id,
            "title": title,
            "category": category,
            "tags": tags
        }
        
        document = Document(page_content=content, metadata=metadata)
        documents.append(document)
    
    # Create new vectorstore
    if documents:
        vectorstore = FAISS.from_documents(documents, embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)
        return True
    else:
        # Create empty vectorstore
        vectorstore = FAISS.from_documents([], embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)
        return True