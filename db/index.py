import argparse
import pymongo
import os
import time

from embed import generate_embedding

parser = argparse.ArgumentParser(description='Compute embeddings for a directory')
parser.add_argument('--path', type=str, help='path of directory to embed')

args = parser.parse_args()
dir_path = args.path

client = pymongo.MongoClient('mongodb+srv://zhaoleon03:Kul9CcMGhImcPhjC@cluster0.gxmrbvy.mongodb.net/?retryWrites=true&w=majority')
db = client['RAG-Hackathon']
embeddings = db['File Embeddings']

VALID_EXTENSIONS = [
    '.py',
    '.txt'
]

print(f'Embedding directory: {dir_path}')
for root, dirs, files in os.walk(dir_path):
    for file in files:
        time.sleep(0.01)

        if not any(file.endswith(ext) for ext in VALID_EXTENSIONS):
            continue

        with open(os.path.join(root, file), 'r') as f:
            # print(root, file)
            file_text = f.read()
            if file_text:
                print(f'Writing {file}')
                embedding = generate_embedding(file_text)
                embeddings.insert_one({"name": os.path.join(root, file), "embedding": embedding})
