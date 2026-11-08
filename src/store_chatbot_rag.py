from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
import sys
import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas as pd

load_dotenv()

client = genai.Client()

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True    # generate new embeddings

    def __call__(self, input: Documents):
        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"


        # perhaps the api in the lecture is old but i have to create a list of contents for the response to work
        contents = []
        for text in input:
            part = types.Content(
                parts = [ types.Part(text = text) ]
            )
            contents.append(part)

        # generate/search for the embeddings
        response = client.models.embed_content(
            model = "gemini-embedding-2",
            contents = contents,
            config = types.EmbedContentConfig(
                task_type = embedding_task
            )
        )

        # python list comprehension
        return [ e.values for e in response.embeddings ] # type: ignore


embed_function = GeminiEmbeddingFunction()
embed_function.document_mode = True     # generate new embeddings

chroma_client = chromadb.PersistentClient()
db = chroma_client.get_or_create_collection(name = "zoomies_clothes", embedding_function = embed_function)

with open("./data/zoomies.csv", "r") as file:
    clothing_data = pd.read_csv(file)
    ids = list(clothing_data.product_id)
    documents = list(clothing_data.product_description)

db.upsert(
    ids = ids,
    documents = documents
)


embed_function.document_mode = False    # use generated embeddings

# query = "What are the best hoodies for running in an alaskan winter?"
# result = db.query(
#     query_texts = [ query ],
#     n_results = 5   # get the top 5 results for each query
# )

# [ all_items ] = result["documents"] # type: ignore
# print(all_items)

chat = client.chats.create(model = "gemini-3.8-flash")

try:
    with open("./prompts/store_chatbot_rag.txt", "r") as f:
        system_instruction = f.read()
except:
    print("Missing system prompt")
    sys.exit()

config = GenerateContentConfig(
    system_instruction = system_instruction
)

while True:
    question = input("> ")

    # do a RAG search to find some matching results for the question
    result = db.query(
        query_texts = [ question ],
        n_results = 5   # get the top 5 results for each query
    )

    [ all_documents ] = result["documents"] # type: ignore
    print(all_documents)


    # use an LLM to create an easily-readable response
    prompt_with_rag = f"""The user has the following question:

    USER_QUESTION: {question}

    Here is information from the product database that may help answer the user's question.
    """

    for document in all_documents:
        prompt_with_rag += f"\nPRODUCT: {document.replace("\n", " ")}"

    print(prompt_with_rag)

    response = chat.send_message(prompt_with_rag, config = config)

    print(response.text)