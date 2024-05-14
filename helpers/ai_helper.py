
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient

from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain

class AIHelper:
    def __init__(self, db):
        self.llm = ChatOpenAI(model="gpt-4")
        self.mongo_cluster_url = os.environ["MONGODB_ATLAS_CLUSTER_URI"] 
        self.db_name = os.environ["DB_NAME"]
        self.collection_name = os.environ["COLLECTION_NAME"]
        self.search_index_name = os.environ["ATLAS_VECTOR_SEARCH_INDEX_NAME"]
        self.db = db


    def get_prompt(self,input):
        context =  [
                ('system', 'You are helpful assistant. Help me with the question having the context:\n\n"{context}"'),
                ('human', input),
            ]

        return ChatPromptTemplate.from_messages(context)

    def get_chain(self, llm, prompt):
        return create_stuff_documents_chain(llm, prompt)

    def chain_invoke(self, query):
        prompt = self.get_prompt(query)
        documents = self.get_relevant_docs(query)

        chain = self.get_chain(self.llm, prompt)
        return chain.invoke({"context": documents})

    def get_retriever(self):
        return db.get_retriever(self.get_embedings())

    def get_relevant_docs(self, query):
        retriver = self.db.get_retriever(self.get_embedings()) 
        return retriver.invoke(query)

    def get_embedings(self):
        return OpenAIEmbeddings(disallowed_special=())
