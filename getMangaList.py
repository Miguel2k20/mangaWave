import requests
from collections import defaultdict
import json

def getMangaList():

    manga_id = "d1a9fdeb-f713-407f-960c-8326b586e6fd"  # id do mangá do vagabond

    languages = ["pt-br"]

    base_url = "https://api.mangadex.org"

    apiResponse = requests.get(
        f"{base_url}/manga/{manga_id}/feed",
        params={"translatedLanguage[]": languages},
    )

    reorganizeManga(apiResponse.json()["data"])

    # Formata o retorno de maneira legível

    # formatted_output = json.dumps(apiResponse.json()["data"], indent=4)
    
    # formatted_output = apiResponse

    return reorganizeManga(apiResponse.json()["data"])

def reorganizeManga(mangalist):

    volumes = defaultdict(list)

    for chapter in mangalist:
        volume = chapter["attributes"]["volume"]
        volumes[volume].append(chapter)

    sorted_volumes = {
        volume: sorted(chapters, key=lambda x: int(x["attributes"]["chapter"]))
        for volume, chapters in sorted(volumes.items(), key=lambda x: int(x[0]))
    }

    formatted_output = json.dumps(sorted_volumes, indent=4)

    return formatted_output

print(getMangaList())
