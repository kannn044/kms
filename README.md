
- Be sure to change the default admin password after first login

## Development

To extend the system:

1. Add new models in the appropriate module
2. Create UI components in the ui directory
3. Update the app.py file to include new features

## Vector Search Implementation

This system uses:
- **FAISS** for efficient vector similarity search
- **Sentence Transformers** (`all-MiniLM-L6-v2` model) for generating embeddings
- Automatic indexing of content when added/updated

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Built with:
- Streamlit
- LangChain
- FAISS
- Sentence Transformers
- SQLite