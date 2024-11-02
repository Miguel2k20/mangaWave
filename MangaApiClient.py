import requests
from pathlib import Path
import json
from Helpers import Helpers

base_url = "https://api.mangadex.org"

class MangaApiClient: 
    
    # Busca de mangás em geral
    def getManga(title):

        response = requests.get(
            f"{base_url}/manga",
            params={
                "title": title,
                "limit": 5,
                "offset": 0 
            }
        )

        customResponse = Helpers.responseCustom(response.json())

        formatted_output = json.dumps(customResponse, indent=4)

        return formatted_output
    
    # Método que busca todos os mangás disponivel do títuloda busca
    def getMangaList(manga_id):

        apiResponse = requests.get(
            f"{base_url}/manga/{manga_id}/feed",
            params={
                "translatedLanguage[]": ["pt-br", "en"],
                "order[volume]": "asc",
                "order[chapter]": "asc",
                "limit": 25,
                "offset": 0
            },
        )

        Finalresponse = Helpers.diretoryCreate(apiResponse)
        Finalresponse = Helpers.reorganizeManga(Finalresponse)

        return json.dumps(Finalresponse, indent=4)
    
    # Esse méotodo busca as paginas relacionada ao capitulo do mangá
    def getMangasPages(hash):

        response = requests.get(
            f"{base_url}/at-home/server/{hash}"
        )

        response = response.json()
        response = Helpers.pagesUrl(response["chapter"])

        return response
    