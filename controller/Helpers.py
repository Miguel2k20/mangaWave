import requests
import math
from PIL import Image
from collections import defaultdict
import re
import os

base_url = "https://api.mangadex.org"
base_image_url = "https://uploads.mangadex.org"

class Helpers:

    # Esse método basicamente vai tirar tudo oq é desnecessário da api fornecida
    @staticmethod
    def responseCustom(mangasData):

        arrayMangasInfos = {}

        mangasData = mangasData.json()

        for item in mangasData["data"]:

            coverArtJpg = next(
                (
                    itemCover['attributes']['fileName']
                    for itemCover in item['relationships']
                    if itemCover['type'] == "cover_art"
                ),
                None
            )

            mangaId = item["id"]

            arrayMangasInfos[mangaId] = {
                "type": item['type'],
                "title": item['attributes']['title'].get('en') or item['attributes']['title'].get('ja'),
                "cover_art": Helpers.getCoverImage(mangaId, coverArtJpg, 256),
                "status": item['attributes'].get('status'),
                "lenguangesEnsabled": item['attributes'].get('availableTranslatedLanguages')
            }

        mangasData['data'] = arrayMangasInfos

        return mangasData
    
    # Esse método vai buscar as imagens da capa do mangás, existe 2 resoluções atualmente: 512 ou 256
    @staticmethod
    def getCoverImage(mangaId, coverArtJpg, size):
        coverUrl = f"{base_image_url}/covers/{mangaId}/{coverArtJpg}.{size}.jpg"
        return coverUrl
    
     # Esse método vai organizar os mangás por capitulo (Isso já está sendo feito na query da api, mas fiz isso pra faciliar no meu front) 
    @staticmethod
    def reorganizeManga(mangalist):
        
        volumes = defaultdict(list)

        for chapter in mangalist["data"]:
            volume = chapter['attributes'].get('volume') 
            if volume is None: 
                volume = "Volume Não Definido"
            volumes[volume].append(chapter)

        sorted_volumes = {
            volume: sorted(
                chapters,
                key=lambda x: (
                    int(float(x['attributes']['chapter']))
                    if x['attributes'].get('chapter') and x['attributes']['chapter'].replace('.', '', 1).isdigit()
                    else float('inf')
                )
            )
            for volume, chapters in sorted(
                volumes.items(),
                key=lambda x: (
                    int(float(x[0]))
                    if x[0] and x[0].replace('.', '', 1).isdigit()
                    else float('inf')
                )
            )
        }

        updated_mangalist = {**mangalist, "data": sorted_volumes}

        return updated_mangalist
    
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
        mangatitle = re.sub(r'[^a-z0-9\s]', '', mangatitle)

        for manga in mangalist["data"]:
            manga["diretory"] = f"MangaWave/{mangatitle}/volume{manga['attributes']['volume']}/chapter{manga['attributes']['chapter']}/language-{manga['attributes']['translatedLanguage']}"
            manga["diretory_temp"] = f"MangaWave/temp/{mangatitle}/volume{manga['attributes']['volume']}/chapter{manga['attributes']['chapter']}/language-{manga['attributes']['translatedLanguage']}"
        
        return mangalist
    
    @staticmethod
    def add_padding(img, padding):

        new_width = img.width + 2 * padding
        new_height = img.height + 2 * padding

        new_img = Image.new("RGB", (new_width, new_height), (255, 255, 255))
        
        new_img.paste(img, (padding, padding))
        
        return new_img
    
    @staticmethod
    def adjust_image_orientation(image):
        if image.width > image.height:
            rotated_image = image.rotate(90, expand=True)  
            return rotated_image
        return image
    
    @staticmethod
    def paginateGenerate(total, limit, offSet):
        if offSet == 0:
            atualPage = 1
        else :
            atualPage = math.ceil(offSet/limit)
        Totalpages = math.ceil(total/limit)
        startPage = max(1, atualPage - 3)
        endPage = min(Totalpages, atualPage + 8)

        return [startPage, endPage]
    
    @staticmethod
    def clearJpgGarbage(diretory):
        permitted_extensions = {'.mobi', '.pdf'}
        for file in os.listdir(diretory):
            diretory_file = os.path.join(diretory,file)
            if os.path.isfile(diretory_file):
                extension = os.path.splitext(file)[1].lower()
                if extension not in permitted_extensions:
                    os.remove(diretory_file)
                    