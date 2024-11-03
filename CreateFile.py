from MangaApiClient import MangaApiClient
from PIL import Image
from Helpers import Helpers

import os
import shutil
import requests
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
                match clientResponse.lower():
                    case "y":
                        shutil.rmtree(diretoryManga)
                        os.makedirs(diretoryManga)
                        CreateFile.downloadMangasPages(diretoryManga)
                        response = "Mangá está pronto! Boa leitura"
                        break
                    case "n":
                        response = "Mangá está pronto! Boa leitura"
                        break
                    case _:
                        print("Resposta inválida. Por favor, responda apenas com 'Y' ou 'N'.")

        return response
    
    @staticmethod
    def downloadMangasPages(diretoryManga):

        urlList = MangaApiClient.getMangasPages("852b134e-d94d-46e4-b58b-44bb422b8642")
        
        for index, item in enumerate(urlList, start=1):
            try:
                response = requests.get(item)
                response.raise_for_status()
                mangaPageName = f"page-{index}.jpg"
                savePath = os.path.join(diretoryManga, mangaPageName)
                with open(savePath, 'wb') as file:
                    file.write(response.content)
                    print(f"Image saved to {diretoryManga}/{mangaPageName}")
            except requests.RequestException as e:
                print(f"Failed to download {savePath}: {e}")

    @staticmethod
    def pdfGenerator(directory):

        if os.path.exists(directory):

            pdfName = f"{directory.split('/')[2]}-{directory.split('/')[3]}-{directory.split('/')[4]}.pdf"
            PDFdirectory = f"{os.path.join(*directory.split('/')[:3])}/pdfs/"

            if not os.path.exists(PDFdirectory):
                os.makedirs(PDFdirectory)
       
            PDFdirectory = os.path.join(PDFdirectory, pdfName)

            if os.path.isfile(PDFdirectory):

                while True:
                    clientResponse = input(f"O PDF {pdfName} já existe, deseja gerar novamente? Y or N: ")
                    match clientResponse.lower():
                        case "y":
                            os.remove(PDFdirectory)
                            break
                        case "n":
                            print("Não criou uma nova")
                            return f"Boa leitura! Lembrando que seu pdf está em {PDFdirectory}"
                        case _:
                            print("Resposta inválida. Por favor, responda apenas com 'Y' ou 'N'.")
                        
            
            filesManga = sorted(os.listdir(directory), key=lambda x: int(x.split("-")[1].split(".")[0]))
        
            filesManga = [
                os.path.join(directory, item) 
                for item in filesManga
            ]
            
            images = [Helpers.add_padding(Image.open(img), 50) for img in filesManga]

            images[0].save(
                PDFdirectory, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
            )
            
            return f"PDF gerado em {PDFdirectory}"
        
        else:
            return "Diretório não encontrado"
