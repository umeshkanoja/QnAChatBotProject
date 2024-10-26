import os
from api.models import Embedding
from pgvector.django import CosineDistance
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from .embedding_utils import generate_embedding


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
)

template = """
Answer the question based on the context below. If you can't 
answer the question, reply "Sorry, I can only help with the questions related to uploaded documents".

Context: {context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

def get_similar_embeddings(embedding, user):
    return Embedding.objects.filter(author=user).order_by(CosineDistance("embedding", embedding))[:5]

def get_openai_response(user, question: str):
    question_embedding = generate_embedding(question)
    similar_embeddings = get_similar_embeddings(question_embedding, user)
    context = "\n".join([embedding.text for embedding in similar_embeddings]) if similar_embeddings else ""
    return chain.invoke({"context": context, "question": question})