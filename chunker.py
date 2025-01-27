from transformers import AutoTokenizer
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)


def chunk_text_with_metadata(text, metadata, max_tokens=256):  # Reduced chunk size
    """
    Splits text into smaller chunks while preserving metadata.

    Args:
        text (str): The input text to be chunked.
        metadata (dict): Metadata associated with the text.
        max_tokens (int): Maximum token limit for the model.

    Returns:
        list: List of dictionaries containing chunks with their metadata.
    """
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")
    tokens = tokenizer.encode(text, add_special_tokens=False)

    chunks_with_metadata = []
    for i in range(0, len(tokens), max_tokens - 2):  # Reserve space for special tokens
        chunk_tokens = tokens[i:i + max_tokens - 2]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks_with_metadata.append({"text": chunk_text, "metadata": metadata})

    # Log the sizes of chunks
    for idx, chunk in enumerate(chunks_with_metadata):
        token_count = len(tokenizer.encode(chunk["text"], add_special_tokens=False))
        if token_count > max_tokens:
            logging.warning(f"Chunk {idx} exceeds max token limit: {token_count} tokens")
        else:
            logging.info(f"Chunk {idx} is within limit: {token_count} tokens")

    return chunks_with_metadata
