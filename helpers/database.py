

import os
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
# from langchain_openai import OpenAIEmbeddings

class Database:
    def __init__(self):
        self.mongo_cluster_url = os.environ["MONGODB_ATLAS_CLUSTER_URI"] 
        self.db_name = os.environ["DB_NAME"]
        self.collection_name = os.environ["COLLECTION_NAME"]
        self.search_index_name = os.environ["ATLAS_VECTOR_SEARCH_INDEX_NAME"]
        
        self.client = MongoClient(self.mongo_cluster_url)
        self.collection = self.client[self.db_name][self.collection_name]  
        
    def get_collection(self):
        return self.collection    
        
    def get_unique_records(self):
        pipeline = [
            {"$group": {"_id": {"ID": "$ID", "Candidate_Name": "$Candidate_Name", "Resume_html": "$Resume_html"}}},
            {"$project": {"ID": "$_id.ID", "Candidate_Name": "$_id.Candidate_Name", "Resume_html": "$_id.Resume_html", "_id": 0}}
        ]
        return list(self.get_collection().aggregate(pipeline))
        
    def insert_vectors(self, docs, embedding):
        return MongoDBAtlasVectorSearch.from_documents(
                documents=docs,
                embedding=embedding,
                collection=self.get_collection(),
                index_name=self.search_index_name,
            )
        
    def get_retriever(self, embeddin):
        vector_search = MongoDBAtlasVectorSearch.from_connection_string(
            self.mongo_cluster_url,
            self.db_name + "." + self.collection_name,
            embeddin, #OpenAIEmbeddings()
            index_name=self.search_index_name,
        )
        return vector_search.as_retriever()