import argparse
import pymongo
import os
import time
import requests

def generate_embedding(query: str):
    url = "https://api.together.xyz/v1/embeddings"

    payload = {
        "model": "togethercomputer/m2-bert-80M-8k-retrieval",
        "input": query
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer 02f64462e7d099ceadef8761a30afe2779db1027eddfec587869f4ea28a97013"
    }


    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        print(f'Failed to get embedding for {query}')
        print(r.json())
    # print(r.status_code)
    return r.json()['data'][0]['embedding']


# parser = argparse.ArgumentParser(description='Compute embeddings for a directory')
# parser.add_argument('--path', type=str, help='path of directory to embed')

# args = parser.parse_args()
# dir_path = args.path
client = pymongo.MongoClient('mongodb+srv://zhaoleon03:Kul9CcMGhImcPhjC@cluster0.gxmrbvy.mongodb.net/?retryWrites=true&w=majority')
db = client['RAG-Hackathon']
embeddings = db['File Embeddings']

def generate_matches(query: str):
    global embeddings

    results = embeddings.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": generate_embedding(query),
                "numCandidates": 5,
                "limit": 2
            }
        }
    ])

    ret = list(results)
    num_keep = min(5, len(ret))
    paths = []
    for doc in ret:
        paths.append(doc['name'])

    return paths[:num_keep]

if __name__ == '__main__':
    dir_path = "../files/mongo-python-driver"


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
