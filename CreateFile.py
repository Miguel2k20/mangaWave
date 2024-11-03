from MangaApiClient import MangaApiClient
import aspose.words as aw

import os
import requests
import shutil

class CreateFile: 

    @staticmethod
    def pasteCreate(mangaObject):
        
        diretoryManga = mangaObject

        if not os.path.exists(diretoryManga):   
            os.makedirs(diretoryManga)
            CreateFile.downloadMangasPages(diretoryManga)
            response = "Mangá está pronto! Boa leitura"
        else:
            while True:
                clientResponse = input("Já existe um mangá relacionado, deseja deleta-lo para baixar o atual? Y or N: ")
                if(clientResponse.lower() == "y"):
                    shutil.rmtree(diretoryManga)
                    os.makedirs(diretoryManga)
                    CreateFile.downloadMangasPages(diretoryManga)
                    response = "Mangá está pronto! Boa leitura"
                    break
                elif(clientResponse.lower() == "n"):
                    response = "Mangá está pronto! Boa leitura"
                    break
                else:
                    print("Resposta inválida. Por favor, responda apenas com 'Y' ou 'N'.")

        return response
    
    @staticmethod
    def downloadMangasPages(diretoryManga):

        urlList = MangaApiClient.getMangasPages("852b134e-d94d-46e4-b58b-44bb422b8642")
        
        for item in urlList:
            try:
                response = requests.get(item)
                response.raise_for_status()
                mangaPageName = item.split('/')[-1]
                savePath = os.path.join(diretoryManga, mangaPageName)
                with open(savePath, 'wb') as file:
                    file.write(response.content)
                    print(f"Image saved to {diretoryManga}/{mangaPageName}")
            except requests.RequestException as e:
                print(f"Failed to download {savePath}: {e}")

    @staticmethod
    def pdfGenerator(diretory):
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
