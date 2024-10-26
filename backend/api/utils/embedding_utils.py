from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEncoder
from langchain_openai import OpenAIEmbeddings
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

def get_split_text(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    text_documents = "\n".join([page.page_content for page in pages])
    
    return text_splitter.split_text(text_documents)

def generate_embedding(text: str):
    return embedder.embed_query(text)
    