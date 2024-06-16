from llama_index.core import load_index_from_storage, StorageContext
from llama_index.retrievers.bm25 import BM25Retriever  
from llama_index.core.tools import RetrieverTool  
from llama_index.core.retrievers import RouterRetriever 
from llama_index.core.postprocessor import SentenceTransformerRerank 
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import Settings
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from app_secrets import api_key, azure_endpoint, api_version

llm = AzureOpenAI(
    model="gpt-35-turbo-16k",
    deployment_name="DanielChatGPT16k",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-3-large",
    deployment_name="text-embedding-3-large",
    api_key="c09f91126e51468d88f57cb83a63ee36",
    azure_endpoint="https://chat-gpt-a1.openai.azure.com/",
    api_version="2023-12-01-preview",
)

Settings.llm = llm
Settings.embed_model = embed_model


def setup_retriever_tools(index):  
    """Create and configure retriever tools for vector and BM25 retrievers."""  

    vector_retriever = index.as_retriever(similarity_top_k=15)  
    bm25_retriever = BM25Retriever.from_defaults(index=index, similarity_top_k=15)  

    retriever_tools = [  
        # RetrieverTool.from_defaults(  
        #     retriever=vector_retriever,  
        #     description="Useful if searching about some similar or related details by performing similarity search",  
        # ),  
        RetrieverTool.from_defaults(  
            retriever=bm25_retriever,  
            description="Useful if searching about specific information by performing Keyword search",  
        )  
    ]
    return retriever_tools


def setup_query_engine(retriever_tools):  
    """Setup the query engine with the given retriever tools and KG retriever."""  

    retriever = RouterRetriever.from_defaults(  
        retriever_tools=retriever_tools,  
        select_multi=True, 
    )
  
    reranker = SentenceTransformerRerank(top_n=10, model="BAAI/bge-reranker-base")  
    query_engine = RetrieverQueryEngine(retriever, node_postprocessors=[reranker,MetadataReplacementPostProcessor(target_metadata_key="window")])

    return query_engine 

import os  
  
persist_dir = "./vector_store"  
# persist_dir = "./LDA_KOR_metadata_extraction\MNX_LDA_metadata_test_vector_store"  
  
# Check if the directory exists and is not empty  
if os.path.exists(persist_dir) and os.listdir(persist_dir):  
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)    
    index = load_index_from_storage(storage_context)  
    retriever_tools = setup_retriever_tools(index)  
    query_engine = setup_query_engine(retriever_tools)  
else:  
    print("The 'vector_store' directory is empty or does not exist. Skipping index loading and query engine setup.")  


def extract_detail(query):
    response = query_engine.query(query)
    return response.response

# persist_dir = "./vector_store"

# storage_context = StorageContext.from_defaults(persist_dir=persist_dir)  

# index = load_index_from_storage(storage_context)

# retriever_tools = setup_retriever_tools(index)

# query_engine = setup_query_engine(retriever_tools)

