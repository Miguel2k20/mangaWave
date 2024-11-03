from MangaApiClient import MangaApiClient
from PIL import Image

import os
import requests
import shutil
import json

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
    def pdfGenerator(directory):

        if os.path.exists(directory):

            PDFdirectory = f"{os.path.join(*directory.split('/')[:3])}/pdfs"

            if not os.path.exists(PDFdirectory):
                os.makedirs(PDFdirectory)
            else:
                return "O PDF já Existe"
                        
            filesManga = os.listdir(directory)
            filesManga = [ 
                os.path.join(directory, item)
                for item in filesManga 
            ]

            images = [Image.open(img) for img in filesManga]

            pdfName = f"{directory.split('/')[2]}-{directory.split('/')[3]}-{directory.split('/')[4]}.pdf"
            mangaPDF = os.path.join(PDFdirectory, pdfName)

            images[0].save(
                mangaPDF, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
            )
            
            return f"PDF gerado em {mangaPDF}"
        
        else:
            return "Diretório não encontrado"
