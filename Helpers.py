import requests
import json
from pathlib import Path
from collections import defaultdict


base_url = "https://api.mangadex.org"
base_image_url = "https://uploads.mangadex.org"
desktop_path = Path.home()

class Helpers:

    # Esse método basicamente vai tirar tudo oq é desnecessário da api fornecida
    def responseCustom(mangasData):

        arrayMangasInfos = {}

        for item in mangasData["data"]:

            coverArtId = next((rel["id"] for rel in item["relationships"] if rel["type"] == "cover_art"), None)
            
            mangaId = item["id"]

            arrayMangasInfos[mangaId] = {
                "type": item['type'],
                "title": item['attributes']['title']['en'],
                "cover_art": Helpers.getCoverImage(mangaId, coverArtId, 256),
                "status": item['attributes']['status'],
                "lenguangesEnsabled": item['attributes']['availableTranslatedLanguages']
            }

        mangasData['data'] = arrayMangasInfos

        return mangasData
    
    # Esse método vai buscar as imagens da capa do mangás, existe 2 resoluções atualmente: 512 ou 256
    def getCoverImage(mangaId, coverId, size):
        
        response = requests.get(
            f"{base_url}/cover/{coverId}",
        ).json()
        
        fileName = response["data"]['attributes']['fileName']

        coverUrl = f"{base_image_url}/covers/{mangaId}/{fileName}.{size}.jpg"
        
        return coverUrl
    
     # Esse método vai organizar os mangás por capitulo (Isso já está sendo feito na query da api, mas fiz isso pra faciliar no meu front) 
    def reorganizeManga(mangalist):

        volumes = defaultdict(list)

        for chapter in mangalist:
            volume = chapter['attributes']['volume']
            volumes[volume].append(chapter)

        sorted_volumes = {
            volume: sorted(chapters, key=lambda x: int(x['attributes']['chapter']))
            for volume, chapters in sorted(volumes.items(), key=lambda x: int(x[0]))
        }

        formatted_output = json.dumps(sorted_volumes, indent=4)

        return formatted_output
    
    # Essa funcao vai apenas montar a url da imagem
    def pagesUrl(apiResponse): 

        baseUrl = f"https://uploads.mangadex.org/data/{apiResponse["hash"]}/"

        pagesArray = list()

        for item in apiResponse["data"]:
            pagesArray.append(f"{baseUrl}{item}")
        
        return pagesArray
    
    def repositoryCreate(mangalist):
        mangalist = mangalist.json()

        mangatitle = [
            requests.get(f"{base_url}/manga/{relation['id']}")
            for relation in mangalist['data'][0]['relationships'] 
            if relation['type'] == 'manga'
        ]

        mangatitle = mangatitle[0].json()['data']['attributes']['title']['en'].lower()

        for manga in mangalist["data"]:
            manga["repository"] = f"{desktop_path}/MangaWave/{mangatitle}/volume{manga['attributes']['volume']}/chapter{manga['attributes']['chapter']}"
        
        return mangalist