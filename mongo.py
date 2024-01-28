import pymongo
import requests

client = pymongo.MongoClient('mongodb+srv://zhaoleon03:Kul9CcMGhImcPhjC@cluster0.gxmrbvy.mongodb.net/?retryWrites=true&w=majority')
db = client['RAG-Hackathon']
embeddings = db['File Embeddings']

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
    return r.json()['data'][0]['embedding']

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

# print(generate_embedding("cat"))

# for doc in embeddings.find():
#     print(doc['name'])

# embeddings.insert_one({"name": "cat", "embedding": generate_embedding("cat")})

# from openai import OpenAI

# TOGETHER_API_KEY = '02f64462e7d099ceadef8761a30afe2779db1027eddfec587869f4ea28a97013'

# client = OpenAI(
#     api_key=TOGETHER_API_KEY,
#     base_url = 'https://api.together.xyz/'
# )

# client.

# print(generate_embedding("import math"))

print(generate_matches("import math"))


results = embeddings.aggregate([
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": generate_embedding("import math"),
            "numCandidates": 5,
            "limit": 2
        }
    }
])

# print(list(results))
for doc in list(results):
    print(doc['name'])
