import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from pinecone import Pinecone
import time

# ----------------------
# Configuration Section
# ----------------------
openai_api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API Key
pinecone_api_key = "YOUR_PINECONE_API_KEY"  # Replace with your Pinecone API Key
index_name = "YOUR_INDEX_NAME"  # Replace with your Pinecone Index Name
pdf_folder = r"YOUR_LOCAL_PDF_DIRECTORY_PATH"  # Example: r"C:\Path\To\Your\PDFs"

# ----------------------
# Resume Support - Set the Batch Number to Resume From
start_batch = 0  # Change this to resume from a later batch if interrupted
batch_size = 50  # Number of chunks to process per batch

# ----------------------
# Initialize Clients
client = OpenAI(api_key=openai_api_key)
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# ----------------------
# Safe PDF Extraction Function
def extract_text(file_path):
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"⚠️ Failed to process {file_path}: {e}")
        return None

# ----------------------
# Chunk Preparation
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_chunks = []

for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(pdf_folder, filename)
        print(f"Processing {filename}...")
        text = extract_text(file_path)
        if not text:
            continue
        splits = splitter.split_text(text)
        for i, chunk in enumerate(splits):
            all_chunks.append({
                "id": f"{filename}-{i}",
                "text": chunk,
                "metadata": {"source": filename}
            })

# ----------------------
# Embedding Generation with Retry Logic
def get_embedding(text, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=[text]
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠️ Embedding failed (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("❌ Skipping this chunk after multiple failed attempts.")
                return None

# ----------------------
# Upload to Pinecone in Batches with Resume Support
for i in range(start_batch * batch_size, len(all_chunks), batch_size):
    batch = all_chunks[i:i + batch_size]
    print(f"Uploading batch {i // batch_size + 1} of {len(all_chunks) // batch_size + 1}")
    vectors = []
    for item in batch:
        embedding = get_embedding(item["text"])
        if embedding is None:
            continue
        vectors.append({
            "id": item["id"],
            "values": embedding,
            "metadata": item["metadata"]
        })
    if vectors:
        try:
            index.upsert(vectors=vectors)
            print(f"✅ Uploaded {len(vectors)} vectors.")
        except Exception as e:
            print(f"❌ Failed to upload batch {i // batch_size + 1}: {e}")
            print("❗ Stopping script to prevent data loss. Please resume by updating start_batch.")
            break
    else:
        print("⚠️ No vectors in this batch to upload.")
    time.sleep(1)  # Prevent rate limit issues

print("✅ Script execution completed.")
