import requests
import json
from Helpers import Helpers

base_url = "https://api.mangadex.org"

class MangaApiClient: 
    
    # Busca de mangás em geral
    def getManga(title):

        apiResponse = requests.get(
            f"{base_url}/manga",
            params={
                "title": title,
                "limit": 5,
                "offset": 0,
            }
        )

        if apiResponse.status_code == 200 and len(apiResponse.json()["data"]) > 0:
            customResponse = Helpers.responseCustom(apiResponse.json())
            finalResponse = json.dumps(customResponse, indent=4)
        else: 
            finalResponse = "Não encontramos nenhum mangá com o nome fornecido."

        return finalResponse
    
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

        if apiResponse.status_code == 200 and len(apiResponse.json()["data"]) > 0:
            finalResponse = Helpers.diretoryCreate(apiResponse)
            finalResponse = Helpers.reorganizeManga(finalResponse)
        else:
            finalResponse = "Não encontramos nenhum mangá com o ID fornecido."
        
        return json.dumps(finalResponse, indent=4)
    
    # Esse méotodo busca as paginas relacionada ao capitulo do mangá
    def getMangasPages(hash):

        apiResponse = requests.get(
            f"{base_url}/at-home/server/{hash}"
        )
        
        if apiResponse.status_code == 200:
            apiResponse = apiResponse.json()
            finalResponse = Helpers.pagesUrl(apiResponse["chapter"])
        else:
            finalResponse = "Não encontramos nenhum mangá com o ID fornecido."

        return finalResponse
    