from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import json

# Load embeddings
embedding = HuggingFaceEmbeddings()

# Function to load data from a JSON file
def load_data_from_json(file_path='cleaned_faqs.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Assuming each FAQ has 'question' and 'answer' fields
    docs = []
    for category, faqs in data.items():
        for faq in faqs:
            content = f"Question: {faq['question']} Answer: {faq['answer']}"
            docs.append(content)

    return docs

# Load data from JSON
print("Loading data from JSON")
data = load_data_from_json("faqs.json")  # Load JSON file

# Store embeddings in FAISS
print("Loading embeddings into vector database")
db = FAISS.from_texts(data, embedding)

# Save FAISS index locally
print("Saving index")
db.save_local('faiss_index')  # Save FAISS index with a specific name

print("Embedding and FAISS storage completed")