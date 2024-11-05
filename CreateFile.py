from MangaApiClient import MangaApiClient
from PIL import Image
from Helpers import Helpers
from pathlib import Path

import os
import shutil
import requests
import subprocess

desktop_path = Path.home()


class CreateFile: 

    @staticmethod
    def pasteCreate(mangaObject):
        
        diretoryManga = os.path.join(desktop_path, mangaObject)

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
    def downloadMangasPages(path):

        urlList = MangaApiClient.getMangasPages("852b134e-d94d-46e4-b58b-44bb422b8642")
        
        for index, item in enumerate(urlList, start=1):
            try:
                response = requests.get(item)
                response.raise_for_status()
                mangaPageName = f"page-{index}.jpg"
                savePath = os.path.join(path, mangaPageName)
                with open(savePath, 'wb') as file:
                    file.write(response.content)
                    print(f"Image saved to {path}/{mangaPageName}")
            except requests.RequestException as e:
                print(f"Failed to download {savePath}: {e}")

    @staticmethod
    def pdfGenerator(path):

        mangaDirectory = os.path.join(desktop_path, path) 

        if os.path.exists(mangaDirectory):
        
            pdfName = f"{path.split('/')[1]}-{path.split('/')[2]}-{path.split('/')[3]}.pdf"
            pdfOutputDirectory  = os.path.join(desktop_path, path.split('/')[0], path.split('/')[1], "pdfs", path.split('/')[4])

            if not os.path.exists(pdfOutputDirectory ):
                os.makedirs(pdfOutputDirectory )
       
            pdfFilePath = os.path.join(pdfOutputDirectory, pdfName)

            if os.path.isfile(pdfFilePath):

                while True:
                    clientResponse = input(f"O PDF {pdfName} já existe, deseja gerar novamente? Y or N: ")
                    match clientResponse.lower():
                        case "y":
                            os.remove(pdfFilePath)
                            break
                        case "n":
                            print("Não criou uma nova")
                            return f"Boa leitura! Lembrando que seu pdf está em {pdfFilePath}"
                        case _:
                            print("Resposta inválida. Por favor, responda apenas com 'Y' ou 'N'.")
                        
            filesManga = sorted(os.listdir(mangaDirectory), key=lambda x: int(x.split("-")[1].split(".")[0]))
            
            filesManga = [
                os.path.join(mangaDirectory, item) 
                for item in filesManga
            ]

            images = [Helpers.add_padding(Image.open(img), 50) for img in filesManga]

            images[0].save(
                pdfFilePath, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
            )
            
            return f"PDF gerado em {pdfFilePath}"
        
        else:
            return "Diretório não encontrado"
    
    @staticmethod
    def mobiGenerator(path):
        
        mangaDirectory = os.path.join(desktop_path, path) 

        if os.path.exists(mangaDirectory):

            mobiName = f"{path.split('/')[1]}-{path.split('/')[2]}-{path.split('/')[3]}.mobi"
            mobiOutputDirectory  = os.path.join(desktop_path, path.split('/')[0], path.split('/')[1], "mobis", path.split('/')[4])

            if not os.path.exists(mobiOutputDirectory):
                os.makedirs(mobiOutputDirectory)

            mobiFilePath = os.path.join(mobiOutputDirectory, mobiName)

            if os.path.isfile(mobiFilePath):
                while True:
                    clientResponse = input(f"O arquivo MOBI {mobiFilePath} já existe, deseja gerar novamente? Y ou N: ")
                    match clientResponse.lower():
                        case "y":
                            os.remove(mobiFilePath) 
                            break
                        case "n":
                            return f"Boa leitura! Seu MOBI está em {mobiFilePath}"
                        case _:
                            print("Resposta inválida. Por favor, responda apenas com 'Y' ou 'N'.")

            filesManga = []
            for item in os.listdir(mangaDirectory):
                if item.endswith('.png') or item.endswith('.jpg'):
                    parts = item.split("-")
                    if len(parts) > 1 and parts[1].split(".")[0].isdigit():
                        index = int(parts[1].split(".")[0])
                        filesManga.append((index, item))


            filesManga.sort(key=lambda x: x[0]) 
            filesManga = [os.path.join(mangaDirectory, item[1]) for item in filesManga]
            htmlFilePath = os.path.join(mobiOutputDirectory, mobiName.replace('.mobi', '.html'))

            with open(htmlFilePath, 'w') as f:
                f.write('<html><body>')
                for img_path in filesManga:
                    img = Helpers.adjust_image_orientation(Image.open(img_path))  
                    img = Helpers.add_padding(img, 50)  
                    temp_img_name = os.path.basename(img_path).replace('.png', '_temp.png').replace('.jpg', '_temp.jpg')
                    temp_img_path = os.path.join(mobiOutputDirectory, temp_img_name)
                    img.save(temp_img_path)
                    f.write(f'<img src="{temp_img_name}" style="width:100%; margin: 0 auto; display: block;"/>')
                f.write('</body></html>')

            try:
                subprocess.run(['ebook-convert', htmlFilePath, mobiFilePath], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Erro na conversão para MOBI: {e}")

            if os.path.isfile(htmlFilePath):
                os.remove(htmlFilePath)

            for img_path in filesManga:
                temp_img_name = os.path.basename(img_path).replace('.png', '_temp.png').replace('.jpg', '_temp.jpg')
                temp_img_path = os.path.join(mobiOutputDirectory, temp_img_name)
                if os.path.isfile(temp_img_path):
                    os.remove(temp_img_path)

            return f"MOBI gerado em {mobiFilePath}"
        else:
            return "Diretório não encontrado"
        