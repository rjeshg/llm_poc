import weaviate

client = weaviate.Client(
    url="http://localhost:8080"
)

class_name = "DocumentChunk"

try:
    # Check if the class exists
    schema = client.schema.get()
    classes = schema.get("classes", [])
    if any(cls.get("class") == class_name for cls in classes):
        print(f"Deleting existing class '{class_name}'...")
        client.schema.delete_class(class_name)
        print(f"Class '{class_name}' deleted successfully.")
    else:
        print(f"Class '{class_name}' does not exist. Nothing to delete.")
except Exception as e:
    print(f"Error deleting class '{class_name}': {e}")
