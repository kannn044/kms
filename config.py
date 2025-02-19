import os

# Application settings
APP_NAME = "Knowledge Management System"
APP_ICON = "📚"
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_ADMIN_EMAIL = "admin@example.com"

# File paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(ROOT_DIR, 'knowledge_db.sqlite')
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploaded_files')
VECTORSTORE_PATH = os.path.join(ROOT_DIR, 'faiss_index')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTORSTORE_PATH, exist_ok=True)

# Vector store settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5

# Security settings
PASSWORD_MIN_LENGTH = 8
SESSION_EXPIRY_DAYS = 7