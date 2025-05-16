from pinecone import Pinecone
from openai import OpenAI

# ----------------------
# Configuration
# ----------------------
openai_api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API Key
pinecone_api_key = "YOUR_PINECONE_API_KEY"  # Replace with your Pinecone API Key
index_name = "YOUR_INDEX_NAME"  # Replace with your Pinecone Index Name
namespace = "YOUR_NAMESPACE"  # Replace with your Namespace or leave as "__default__"

# Initialize OpenAI and Pinecone Clients
client = OpenAI(api_key=openai_api_key)
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# ----------------------
# Generate Embedding for User Question
def get_query_embedding(question):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[question]
    )
    return response.data[0].embedding

# ----------------------
# Retrieve Relevant Chunks from Pinecone
def test_retrieval(question, top_k=5):
    print(f"\nTesting retrieval for: {question}\n")
    query_embedding = get_query_embedding(question)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

    if not results["matches"]:
        print("No matches found.\n")
        return

    for idx, match in enumerate(results["matches"], 1):
        print(f"--- Match {idx} ---")
        print(f"Score: {match['score']}")
        print(f"ID: {match['id']}")
        print("Content:")
        print(match['metadata'].get('text', '[No text found]'))
        print("\n")

# ----------------------
# Example Usage
if __name__ == "__main__":
    user_question = "Enter your sample question here"
    test_retrieval(user_question, top_k=5)
