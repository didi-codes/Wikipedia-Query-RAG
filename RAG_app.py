import logging
import warnings
from transformers import logging as hf_logging

# Set log levels
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)
hf_logging.set_verbosity_error()

# Filter out Python warnings
warnings.filterwarnings("ignore")

# Configuration variables
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 5

# Read the contents of Selected_Document.txt
with open("Selected_Document.txt", "r", encoding="utf-8") as file:
    text = file.read()

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize text splitter with custom separators and config
text_splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', ' ', ''],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

# Split the text into chunks
chunks = text_splitter.split_text(text)

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load the sentence transformer model
model = SentenceTransformer(model_name)

# Encode the chunks with the progress bar disabled
embeddings = model.encode(chunks, show_progress_bar=False)

# Convert embeddings to float32 NumPy array
embeddings_np = np.array(embeddings).astype("float32")

# Initialize FAISS index with correct dimension
dimension = embeddings_np.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the FAISS index
index.add(embeddings_np)

from transformers import pipeline

# Set up Hugging Face text-to-text generation pipeline on CPU
generator = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)

response = generator("Translate English to French: How are you?")
print(response[0]['generated_text'])

def retrieve_chunks(question, k=top_k):
    # Encode the question using the same model
    question_embedding = model.encode([question], show_progress_bar=False).astype("float32")
    
    # Search the FAISS index for top k similar chunks
    distances, indices = index.search(question_embedding, k)
    
    # Return the top-k matching chunks
    return [chunks[i] for i in indices[0] if i < len(chunks)]

def answer_question(question):
    # Retrieve relevant chunks
    relevant_chunks = retrieve_chunks(question)
    
    # Build a prompt with context
    context = "\n".join(relevant_chunks)
    prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {question}\nAnswer:"
    
    # Generate the answer
    result = generator(prompt)
    return result[0]["generated_text"]

if __name__ == "__main__":
    print("Enter 'exit' or 'quit' to end.")
    while True:
        question = input("Your question: ")
        if question.lower() in ("exit", "quit"):
            break
        print("Answer:", answer_question(question))
