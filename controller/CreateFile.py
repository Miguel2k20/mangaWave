from .MangaApiClient import MangaApiClient
from .Helpers import Helpers
from PIL import Image
from pathlib import Path

import os
import shutil
import requests
import subprocess

desktop_path = Path.home()


class CreateFile: 

    @staticmethod
    def pasteCreate(mangaObject):
        diretoryManga = os.path.join(desktop_path, mangaObject['diretory'])
        idManga = mangaObject['id']
        if not os.path.exists(diretoryManga):   
            os.makedirs(diretoryManga)
            CreateFile.downloadMangasPages(diretoryManga, idManga)

        return True
    
    @staticmethod
    def downloadMangasPages(path, idManga):
        
        urlList = MangaApiClient.getMangasPages(idManga)
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
                return False
        
        return True

    @staticmethod
    def pdfGenerator(mangaObject):

        diretory = mangaObject['diretory']

        mangaDirectory = os.path.join(desktop_path, diretory) 

        pdf_output_directory = os.path.join(desktop_path, diretory.split('/')[0], diretory.split('/')[1], "pdfs", diretory.split('/')[4])
        
        pdf_name = f"{diretory.split('/')[1]}-{diretory.split('/')[2]}-{diretory.split('/')[3]}.pdf"

        tempDiretory = None

        if os.path.exists(pdf_output_directory):
            file_diretory = os.path.join(pdf_output_directory, pdf_name)
            if os.path.exists(file_diretory):
                os.remove(file_diretory)

        if not os.path.exists(mangaDirectory):
            
            idManga = mangaObject['id']
            tempDiretory_path = pdf_output_directory
            tempDiretory = os.path.join(desktop_path, tempDiretory_path) 

            os.makedirs(tempDiretory, exist_ok=True)

            if not CreateFile.downloadMangasPages(tempDiretory, idManga):
                return False

            mangaDirectory = tempDiretory
        
        pdfFilePath = os.path.join(pdf_output_directory, pdf_name)

        # Preciso resolver o erro aqui
        filesManga = sorted(
            [f for f in os.listdir(mangaDirectory) if os.path.isfile(os.path.join(mangaDirectory, f))],
            key=lambda x: int(x.split("-")[1].split(".")[0])
        )

        filesManga = [
            os.path.join(mangaDirectory, item) 
            for item in filesManga
        ]

        images = [Helpers.add_padding(Image.open(img), 50) for img in filesManga]

        images[0].save(
            pdfFilePath, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )

        if tempDiretory:
            Helpers.clearJpgGarbage(tempDiretory)

        return True
    
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
        