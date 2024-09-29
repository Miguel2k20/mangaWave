import requests

import json

base_url = "https://api.mangadex.org"

def getMangasPages():

    global base_url

    hash = "42e6ebbf-1d6b-4772-b534-b0c261f296fe"

    response = requests.get(
        f"{base_url}/at-home/server/{hash}"
    )

    response = response.json()

    formatted_output = json.dumps(response["chapter"], indent=4)

    return formatted_output
    
print(getMangasPages())