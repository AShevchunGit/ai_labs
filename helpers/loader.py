import pandas as pd
import random
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class CSVLoader:
    def __init__(self,ai_helper, db):
        self.rows = None
        self.ai_helper = ai_helper
        self.db = db
        self.first_names = ["John", "Jane", "Sam", "Sally", "Mike", "Emily", "Jacob", "Olivia", "Daniel", "Sophia", 
                            "Oleksandr", "Anastasia", "Ivan", "Yulia", "Sergey", "Olena",  
                            "Jakub", "Agnieszka", "Mateusz", "Katarzyna", "Michał", "Anna",  
                            "Max", "Sophie", "Lukas", "Maria", "Felix", "Anna"]  
        self.last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", 
                        "Shevchenko", "Kovalenko", "Boyko", "Tkachenko", "Kozak", "Bondarenko", 
                        "Nowak", "Kowalski", "Wiśniewski", "Dąbrowski", "Lewandowski", "Wójcik",  
                        "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer"]  
        self.used_names = set()        
        

    def generate_candidate_name(self):
        while True:
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            name = first_name + ' ' + last_name
            if name not in self.used_names:
                self.used_names.add(name)
                return name

    def load_csv(self, file_path, rows=40):
        # Read the CSV file and store the CVs in a DataFrame
        rows = pd.read_csv(file_path).head(rows)
        rows['Candidate_Name'] = rows.apply(lambda row: self.generate_candidate_name(), axis=1)
        
        rows['Content'] = rows.apply(lambda row:  row['Candidate_Name']+"\n\n"+row.Resume_str, axis=1)
        self.rows = rows
        return rows
    
    def upload_csv(self, file_path="./cvs/Resume.csv"):
        rows = self.load_csv(file_path, 40)
        
        loader = DataFrameLoader(rows, page_content_column="Content")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )

        docs = loader.load_and_split(text_splitter=text_splitter)
        self.db.insert_vectors(docs, self.ai_helper.get_embedings())
