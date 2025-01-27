from transformers import pipeline

def generate_response_with_context(query, retrieved_chunks):
    """
    Generates a response using Flan-T5 XL.
    """
    context = "\n".join([f"Source: {chunk.metadata['file_name']}\n{chunk.page_content}" for chunk in retrieved_chunks])

    generator_pipeline = pipeline("text2text-generation", model="google/flan-t5-xl", tokenizer="google/flan-t5-xl")

    prompt = (
        f"Use the context below to answer the question accurately:\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Provide a concise and precise answer, including the source document name if relevant."
    )
    response = generator_pipeline(prompt, max_length=200)
    return response[0]["generated_text"]
