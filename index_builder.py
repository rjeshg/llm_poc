from langchain_community.embeddings import HuggingFaceEmbeddings  # Fixed import
from langchain.vectorstores import FAISS
from chunker import chunk_text_with_metadata


def process_documents(documents, max_tokens=256):  # Reduced chunk size
    """
    Processes documents to ensure chunks fit within the model's token limit.

    Args:
        documents (list): List of documents containing text and metadata.
        max_tokens (int): Maximum token limit for the embedding model.

    Returns:
        list: Processed documents with appropriately sized chunks.
    """
    processed_documents = []
    for doc in documents:
        for chunk in doc["chunks"]:
            text = chunk["text"]
            metadata = chunk["metadata"]
            smaller_chunks = chunk_text_with_metadata(text, metadata, max_tokens)
            processed_documents.extend(smaller_chunks)
    print(f"Processed {len(processed_documents)} chunks across all documents.")
    return processed_documents


def build_faiss_index(documents):
    """
    Builds an in-memory FAISS vector database index.

    Args:
        documents (list): List of documents containing chunks and metadata.

    Returns:
        FAISS: An in-memory FAISS vector store.
    """
    # Process documents
    documents = process_documents(documents)

    # Prepare texts and metadata
    texts = [doc["text"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]

    # Use a smaller and faster embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Build FAISS vector store
    vector_store = FAISS.from_texts(texts=texts, embedding=embedding_model, metadatas=metadatas)

    # Save the FAISS index for reuse
    vector_store.save_local("faiss_index")

    print(f"Indexed {len(texts)} chunks into FAISS.")
    return vector_store


def query_faiss(vector_store, query, top_k=5):
    """
    Queries the FAISS vectorstore to retrieve the most relevant chunks with metadata.

    Args:
        vector_store (FAISS): FAISS vectorstore.
        query (str): User query.
        top_k (int): Number of results to retrieve.

    Returns:
        list: Retrieved chunks with metadata.
    """
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")
    tokens = tokenizer.encode(query, add_special_tokens=False)

    # Truncate query if it exceeds the model's token limit
    if len(tokens) > 512:
        print(f"Query exceeds token limit ({len(tokens)} tokens). Truncating...")
        tokens = tokens[:512 - 2]  # Reserve space for special tokens
        query = tokenizer.decode(tokens, skip_special_tokens=True)

    results = vector_store.similarity_search(query, k=top_k)
    print(f"Retrieved {len(results)} results:")
    for i, result in enumerate(results):
        print(f"Result {i + 1}: {result.page_content} (Source: {result.metadata.get('file_name', 'Unknown')})")
    return results
