# Reflection Report 

## Description Of The Document I Selected

The document I selected is the Wikipedia article on **Quantum Computing**. It dives into the field of computing based on the principles of quantum mechanics, explaining how quantum computers use qubits and phenomena like superposition and entanglement to perform certain calculations much faster than classical computers. The article covers the theory behind quantum computation, key algorithms, potential applications, and the current state of research and development. It also discusses challenges like error correction and hardware limitations. This article provides a solid and detailed foundation on a cutting-edge technology that’s poised to revolutionize computing, making it an ideal text for exploring advanced AI and retrieval methods.


## Five Deep Dive Questions & AI Answers

### 1. What is the embedding dimensionality, and why does it matter?

**Answer:**
Embedding dimensionality refers to the size of the vector that represents each text chunk after encoding by the model (e.g., SentenceTransformer). It matters because it directly affects the accuracy and efficiency of similarity searches in FAISS. Higher dimensions can capture more semantic detail but increase computational cost, while too low a dimension may lose important information. The FAISS index must be initialized with the correct embedding dimension to function properly.

---

### 2. How does the FAISS IndexFlatL2 search work in this system?

**Answer:**
FAISS IndexFlatL2 performs a brute-force nearest neighbor search based on Euclidean (L2) distance between embeddings. When a question is encoded, its vector is compared against all stored chunk vectors, returning the closest matches. Though not the fastest for huge datasets, IndexFlatL2 provides exact similarity results, which helps ensure the retrieved chunks are truly relevant.

---

### 3. What impact does chunk overlap have on retrieval and answer quality?

**Answer:**
Chunk overlap ensures that text near the boundaries of chunks is repeated in adjacent chunks. This avoids losing important context that might be split between chunks, improving retrieval relevance and answer completeness. However, too much overlap can cause redundancy and increase index size, so a balance is necessary to maximize both efficiency and quality.

---

### 4. How is prompt design important in combining retrieved chunks with the question?

**Answer:**
Prompt design shapes how the language model interprets and uses retrieved context to answer the question. A well-crafted prompt clearly presents the relevant information (retrieved chunks) and explicitly instructs the model on the task (e.g., “Answer the question based on the context below”). Good prompt structure helps the model generate accurate, focused, and coherent answers.

---

### 5. Why do we encode the user question using the same model as the chunks?

**Answer:**
Using the same embedding model for both the document chunks and the user question ensures that their vector representations lie in the same semantic space. This consistency is critical for meaningful similarity comparisons in FAISS, allowing the system to retrieve chunks that truly relate to the question’s meaning rather than just matching superficial word features.


## Reflection on Chunk Size & Overlap Impact on Answer Quality

**Chunk Size** and **Chunk Overlap** are crucial parameters when splitting long documents for embedding and retrieval. Their values directly affect the granularity of context available during question answering, which influences the relevance and completeness of generated answers.

#### Chunk Size

* **Larger chunk sizes** (e.g., 800–1000 tokens):

  * Pros: More context in each chunk, so the model has broader information per retrieval.
  * Cons: May include irrelevant or distracting details, reducing focus on the most pertinent information.
  * Can slow down embedding and search due to longer text per chunk.

* **Smaller chunk sizes** (e.g., 200–400 tokens):

  * Pros: More focused and concise chunks, easier for the model to attend to relevant info.
  * Cons: Risk of missing important context that spans across chunks.
  * Might increase the number of chunks and overall complexity.

#### Chunk Overlap

* **Higher overlap** (e.g., 50–100 tokens):

  * Pros: Ensures important information at chunk boundaries is not lost, improving context continuity.
  * Cons: More redundant data, slightly increasing embedding size and search time.
  * Can improve answer quality when questions relate to information spanning chunk edges.

* **Lower or zero overlap**:

  * Pros: Less redundancy, smaller index size.
  * Cons: Risk of losing context at chunk boundaries, potentially leading to incomplete or less accurate answers.

#### Overall Observations

* Moderate chunk sizes (around 400–600 tokens) with an overlap of 10–20% (e.g., 50 tokens overlap on 500 chunk size) often balance detail and efficiency well.
* Too large chunks can dilute focus; too small chunks may fragment meaning.
* Overlap helps maintain semantic continuity but has diminishing returns beyond a certain point.
* Empirical testing with my dataset and questions is important to find the sweet spot.


