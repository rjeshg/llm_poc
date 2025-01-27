from pdfminer.high_level import extract_text
import os


def extract_text_with_metadata(file_path):
    """
    Extracts text from a file and includes metadata such as the file name.

    Args:
        file_path (str): Path to the file.

    Returns:
        dict: Extracted text and metadata.
    """
    metadata = {"file_name": os.path.basename(file_path)}
    text = ""

    if file_path.endswith(".pdf"):
        try:
            text = extract_text(file_path)
        except Exception as e:
            print(f"Error extracting text from PDF: {file_path}, {e}")
    elif file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading text file: {file_path}, {e}")
    else:
        print(f"Unsupported file type: {file_path}")

    metadata["text"] = text
    return metadata


def extract_texts_from_folder(folder_path):
    """
    Extracts text and metadata from all supported files in a folder.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        list: List of documents with text and metadata.
    """
    all_documents = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.startswith("."):  # Skip hidden files
            continue

        document = extract_text_with_metadata(file_path)
        if document["text"].strip():
            all_documents.append(document)
        else:
            print(f"No text extracted from file: {file_name}")

    return all_documents
