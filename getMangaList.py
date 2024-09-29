import requests
from collections import defaultdict
import json

def getMangaList():

    base_url = "https://api.mangadex.org"
    manga_id = "d1a9fdeb-f713-407f-960c-8326b586e6fd"  # id do mangá do vagabond
    languages = ["pt-br"]


    apiResponse = requests.get(
        f"{base_url}/manga/{manga_id}/feed",
        params={
            "translatedLanguage[]": languages,
            "order[volume]": "desc",
            "order[chapter]": "desc"
        },
    )
    # https://api.mangadex.org/manga/d1a9fdeb-f713-407f-960c-8326b586e6fd/feed?translatedLanguage[]=pt-br&limit=96&includes[]=scanlation_group&includes[]=user&order[volume]=desc&order[chapter]=desc&offset=0&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic

    reorganizeManga(apiResponse.json()["data"])

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
