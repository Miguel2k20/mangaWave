from MangaApiClient import MangaApiClient
from CreateFile import CreateFile
from pathlib import Path
desktop_path = Path.home()

def getMangaTeste():
    title = input("Fale ai o mangá que você quer: ")
    print("Procurando seu manga....")
    return MangaApiClient.getManga(title)

def getMangaListTeste():
    print("Sugestão: 6b1eb93e-473a-4ab3-9922-1a66d2a29a4a é o id do mangá do Naruto")
    idManga = input("Informe o id do mangá que você deseja: ")
    return MangaApiClient.getMangaList(idManga)

def getMangasPagesTeste():
    print("Sugestão: 0725c4e1-0af9-480d-8c4a-ab266ca0526b é o cap 601 do naruto")
    idPage = input("Passa o id do captitulo ai: ")
    return MangaApiClient.getMangasPages(idPage)

def pasteCreateTeste():
    teste = f"{desktop_path}/MangaWave/vagabond/volume3/chapter25/language-pt-br"
    return CreateFile.pasteCreate(teste)

def pdfTest():
    teste = f"{desktop_path}/MangaWave/vagabond/volume3/chapter25/language-pt-br"
    return CreateFile.pdfGenerator(teste)

def mobiTest():
    teste = f"{desktop_path}/MangaWave/vagabond/volume3/chapter25/language-pt-br"
    return CreateFile.mobiGenerator(teste)

while True:
    print("--- Bem vindo ao ambiente de teste do mangaWave ---")
    print("1: Buscar um mangá pelo titulo")
    print("2: Buscar os capítulos relacionado ao id mangá")
    print("3: Buscar as páginas relacionadas ao capítulo do mangá")
    print("4: Criação de pasta")
    print("5: Criação de PDF")
    print("6: Croação de Mobi")
    print("7: Sair")

    option = int(input("Selecione o item que deseja testar: "))

    match option:
        case 1:
            print(getMangaTeste())
        case 2:
            print(getMangaListTeste())
        case 3:
            print(getMangasPagesTeste())
        case 4:
            print(pasteCreateTeste())
        case 5:
            print(pdfTest())
        case 6:
            print(mobiTest())
        case 7:
            print("Até mais!")
            break
        case _:
            print("Número inválido")
