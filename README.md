# 🧠 RAG PDF Uploader - Build Your Own Retrieval-Augmented Generation (RAG) Knowledge Base

This repository contains a **ready-to-use Python script** that processes your **local PDF files**, converts them into **embeddings**, and **uploads them to Pinecone** for building a **Retrieval-Augmented Generation (RAG) chatbot**.

---

## 🚀 What This Script Does

1. **Extracts Text** from your **PDF files** on your computer.
2. **Splits the Text into Chunks** so that the chatbot can find small, relevant pieces of information.
3. **Generates Embeddings** (mathematical representations of meaning) using OpenAI’s `text-embedding-ada-002` model.
4. **Uploads the Embeddings** to your **Pinecone vector database**.
5. **Supports Resume Functionality** in case your process is interrupted.

---

## 🛠️ Prerequisites

1. **Python 3.8+**
2. **OpenAI API Key**  
   Get your key here: https://platform.openai.com/api-keys
3. **Pinecone API Key and Index**  
   Set up your account here: https://www.pinecone.io/

---

## 🧑‍💻 Installation

1. **Clone this repository or download the script.**

2. **Install Dependencies:**
   ```bash
   pip install pinecone openai langchain pdfplumber tiktoken

⚙️ Configuration
In the script, update the following values:

openai_api_key = "YOUR_OPENAI_API_KEY"
pinecone_api_key = "YOUR_PINECONE_API_KEY"
index_name = "YOUR_INDEX_NAME"
pdf_folder = r"YOUR_LOCAL_PDF_DIRECTORY_PATH"


YOUR_OPENAI_API_KEY – From your OpenAI account.

YOUR_PINECONE_API_KEY – From your Pinecone account.

YOUR_INDEX_NAME – The name of the index you created on Pinecone.

YOUR_LOCAL_PDF_DIRECTORY_PATH – Full path to the folder where your PDFs are stored.
Example for Windows:
pdf_folder = r"C:\Users\YourName\Documents\MyPDFs"

▶️ How to Run
Open Command Prompt or Terminal.

Navigate to the folder containing the script.

Run the script:
python upload_to_pinecone.py




♻️ Resume Support
If your process stops or your computer sleeps:

Note the last batch number printed in the logs.

Update the start_batch variable in the script:

start_batch = YOUR_LAST_SUCCESSFUL_BATCH_NUMBER


📝 Example Use Case
You have a folder with 500 legal PDFs.
You want to make them searchable in your AI chatbot.

✅ This script will:

Read all your PDFs.

Convert them into searchable AI-friendly data.

Upload them to Pinecone for RAG-based chatbots or support agents.

📖 What is RAG?
RAG (Retrieval-Augmented Generation) is a method that:

Retrieves relevant data from your knowledge base.

Generates human-like answers using a Language Model (like GPT).

This method prevents hallucinations and makes your chatbot fact-based and reliable.

✅ Why Use a Vector Database?
Traditional databases search by exact keywords.
Vector databases search by meaning.

Example:

Searching for "legal contracts" will also find "binding agreements" in a vector database.

That’s why Pinecone is essential for building AI-powered search systems.

💡 Next Steps
Build a chatbot frontend to query your data.

Connect the retrieval pipeline using the same Pinecone index.

Implement grounded prompting to improve response accuracy.

📬 Questions?
Feel free to comment on my YouTube video or reach out to me on [Your Contact Channel].

Happy Building! 🚀



