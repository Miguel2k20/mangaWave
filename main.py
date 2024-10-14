import requests
import json
from collections import defaultdict

base_url = "https://api.mangadex.org"
base_image_url = "https://uploads.mangadex.org"

class main: 
    
    global base_url
    
    # Busca de mangás em geral
    def getManga(title):

        response = requests.get(
            f"{base_url}/manga",
            params={
                "title": title
            }
        )

        customResponse = main.responseCustom(response.json())

        formatted_output = json.dumps(customResponse, indent=4)

        return formatted_output
    
    # Esse método basicamente vai tirar tudo oq é desnecessário da api fornecida
    def responseCustom(mangasData):

        arrayMangasInfos = {}

        for item in mangasData["data"]:

            coverArtId = next((rel["id"] for rel in item["relationships"] if rel["type"] == "cover_art"), None)
            
            mangaId = item["id"]

            arrayMangasInfos[mangaId] = {
                "type": item["type"],
                "title": item["attributes"]["title"]["en"],
                "cover_art": main.getCoverImage(mangaId, coverArtId, 256),
                "status": item["attributes"]["status"],
                "lenguangesEnsabled": item["attributes"]["availableTranslatedLanguages"]
            }

        mangasData["data"] = arrayMangasInfos

        return mangasData
    
    # Esse método vai buscar as imagens da capa do mangás, existe 2 resoluções atualmente: 512 ou 256
    def getCoverImage(mangaId, coverId, size):
        
        response = requests.get(
            f"{base_url}/cover/{coverId}",
        ).json()
        
        fileName = response["data"]["attributes"]["fileName"]

        coverUrl = f"{base_image_url}/covers/{mangaId}/{fileName}.{size}.jpg"
        
        return coverUrl
    
    # Método que busca todos os mangás disponivel do títuloda busca
    def getMangaList(manga_id):
        apiResponse = requests.get(
            f"{base_url}/manga/{manga_id}/feed",
            params={
                "translatedLanguage[]": ["pt-br"],
                "order[volume]": "desc",
                "order[chapter]": "desc"
            },
        )
        return main.reorganizeManga(apiResponse.json()["data"])
    
    # Esse método vai organizar os mangás por capitulo (Isso já está sendo feito na query da api, mas fiz isso pra faciliar no meu front) 
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

    # Esse méotodo busca as paginas relacionada ao capitulo do mangá
    def getMangasPages(hash):

        response = requests.get(
            f"{base_url}/at-home/server/{hash}"
        )

        response = response.json()

        formatted_output = json.dumps(response["chapter"], indent=4)

        return formatted_output
    
print("mangawave")

title = input("Fale ai o mangá que ce quer: ")

print("Procurando seu manga....")

print(main.getManga(title))

idManga = input("Passa o id do mangá ai: ")

print(main.getMangaList(idManga))

idPage = input("Passa o id do captitulo ai: ")

print(main.getMangasPages(idPage))
