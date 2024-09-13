

import requests
import json

base_url = "https://api.mangadex.org"

def getManga(title):

    global base_url

    title = title

    response = requests.get(
        f"{base_url}/manga",
        params={"title": title}
    )
    
    customResponse = responseCustomApi(response.json())

    formatted_output = json.dumps(customResponse, indent=4)

    return formatted_output

def responseCustomApi(mangasData):

    arrayMangasInfos = {}

    for item in mangasData["data"]:

        coverArtId = next((rel["id"] for rel in item["relationships"] if rel["type"] == "cover_art"), None)
        
        mangaId = item["id"]

        arrayMangasInfos[mangaId] = {
            "type": item["type"],
            "title": item["attributes"]["title"]["en"],
            "cover_art": getCoverImage(mangaId, coverArtId, 512),
            "status": item["attributes"]["status"],
            "lenguangesEnsabled": item["attributes"]["availableTranslatedLanguages"]
        }

    mangasData["data"] = arrayMangasInfos

    return mangasData

# Size deve ser 512 ou 256
def getCoverImage(mangaId, coverId, size):
    
    global base_url

    response = requests.get(
        f"{base_url}/cover/{coverId}",
    ).json()
    
    fileName = response["data"]["attributes"]["fileName"]

    coverUrl = f"https://uploads.mangadex.org/covers/{mangaId}/{fileName}.{size}.jpg"
    
    return coverUrl

title = "Naruto"
print(getManga(title))
