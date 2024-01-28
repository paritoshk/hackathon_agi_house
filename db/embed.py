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
