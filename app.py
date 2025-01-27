from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from file_processor import extract_texts_from_folder
from index_builder import build_faiss_index, query_faiss
from generator import generate_response_with_context
from chunker import chunk_text_with_metadata  # Fix the import
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Disable tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

DATA_FOLDER = "data"

print("Extracting text and metadata from files...")
documents = extract_texts_from_folder(DATA_FOLDER)
if not documents:
    print("No documents found in the folder.")
    exit(1)

print("Chunking documents...")
for doc in documents:
    doc["chunks"] = chunk_text_with_metadata(doc["text"], {"file_name": doc["file_name"]})  # Fixed the usage

print("Building FAISS vectorstore...")
vector_store = build_faiss_index(documents)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_api(request: QueryRequest):
    try:
        # Retrieve chunks
        retrieved_chunks = query_faiss(vector_store, request.query)
        if not retrieved_chunks:
            return JSONResponse(content={"answer": "No relevant information found."}, status_code=200)

        # Generate response
        answer = generate_response_with_context(request.query, retrieved_chunks)
        return JSONResponse(content={"answer": answer}, status_code=200)
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"answer": "An error occurred while processing your request."}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
