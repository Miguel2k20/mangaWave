import requests
from PIL import Image

from pathlib import Path
from collections import defaultdict


base_url = "https://api.mangadex.org"
base_image_url = "https://uploads.mangadex.org"
desktop_path = Path.home()

class Helpers:

    # Esse método basicamente vai tirar tudo oq é desnecessário da api fornecida
    @staticmethod
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
    @staticmethod
    def getCoverImage(mangaId, coverId, size):
        
        response = requests.get(
            f"{base_url}/cover/{coverId}",
        ).json()
        
        fileName = response["data"]['attributes']['fileName']

        coverUrl = f"{base_image_url}/covers/{mangaId}/{fileName}.{size}.jpg"
        
        return coverUrl
    
     # Esse método vai organizar os mangás por capitulo (Isso já está sendo feito na query da api, mas fiz isso pra faciliar no meu front) 
    @staticmethod
    def reorganizeManga(mangalist):

        volumes = defaultdict(list)

        for chapter in mangalist["data"]:
            volume = chapter['attributes']['volume']
            volumes[volume].append(chapter)

        sorted_volumes = {
            volume: sorted(chapters, key=lambda x: int(float(x['attributes']['chapter'])) if x['attributes']['chapter'].replace('.', '', 1).isdigit() else float('inf'))
            for volume, chapters in sorted(volumes.items(), key=lambda x: int(float(x[0])) if x[0].replace('.', '', 1).isdigit() else float('inf'))
        }

        return sorted_volumes
    
    # Essa funcao vai apenas montar a url da imagem
    @staticmethod
    def pagesUrl(apiResponse): 

        baseUrl = f"https://uploads.mangadex.org/data/{apiResponse["hash"]}/"

        pagesArray = list()

        for item in apiResponse["data"]:
            pagesArray.append(f"{baseUrl}{item}")
        
        return pagesArray
    
    # Feito pra criar uma string contendo um diretorio para armazenar os mangás
    @staticmethod
    def diretoryCreate(mangalist):
        mangalist = mangalist.json()

        mangatitle = [
            requests.get(f"{base_url}/manga/{relation['id']}")
            for relation in mangalist['data'][0]['relationships'] 
            if relation['type'] == 'manga'
        ]

        mangatitle = mangatitle[0].json()['data']['attributes']['title']['en'].lower()

        for manga in mangalist["data"]:
            manga["diretory"] = f"{desktop_path}/MangaWave/{mangatitle}/volume{manga['attributes']['volume']}/chapter{manga['attributes']['chapter']}/language-{manga['attributes']['translatedLanguage']}"
        
        return mangalist
    
    @staticmethod
    def add_padding(img, padding):

        new_width = img.width + 2 * padding
        new_height = img.height + 2 * padding

        new_img = Image.new("RGB", (new_width, new_height), (255, 255, 255))
        
        new_img.paste(img, (padding, padding))
        
        return new_img
    