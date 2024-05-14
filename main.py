import os
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import pandas as pd
import random

from helpers.loader import CSVLoader
from helpers.ai_helper import AIHelper
from helpers.database import Database


### Set the environment variables
# os.environ["OPENAI_API_KEY"]
# os.environ["MONGODB_ATLAS_CLUSTER_URI"]
# os.environ["DB_NAME"]
# os.environ["COLLECTION_NAME"]
# os.environ["ATLAS_VECTOR_SEARCH_INDEX_NAME"]



# from langchain_community.document_loaders import DataFrameLoader

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = './uploads'

db = Database()
ai_helper = AIHelper(db)
csvLoader = CSVLoader(ai_helper, db)


## ===================
## Load the CSV file
## TODO: add upload button and use it
# csvLoader = CSVLoader(ai_helper, db)
# csvLoader.upload_csv("./cvs/Resume.csv")
## ===================

# get from db
rows = db.get_unique_records()


# query = "What is this candidate's Daniel Williams? Please return the answer in a concise manner, no more than 250 words. If not found, return 'Not provided'"
query = "What are the primary roles and responsibilities Daniel Taylor has undertaken throughout his career?"

# docs = ai_helper.get_relevant_docs(query)
# print(docs)

result = ai_helper.chain_invoke(query)
print(result)

@app.route('/')
def cv_list():
    return render_template('cv_list.html', cvs=rows)

@app.route('/cv/<int:cv_id>')
def cv_detail(cv_id):
    # Render the CV detail template
    
    for cv in rows:
        if cv["ID"] == cv_id:
            break
    
    return render_template('cv_detail.html', cv=cv)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            redirect('/')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            csvLoader.upload_csv(filepath)    
            
            return redirect('/')
        else:
            flash('Allowed file types are .csv')
            redirect('/')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)