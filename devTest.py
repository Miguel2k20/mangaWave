from MangaApiClient import MangaApiClient
from CreateFile import CreateFile
from pathlib import Path
desktop_path = Path.home()

def getMangaTeste():
    title = input("Fale ai o mangá que ce quer: ")
    print("Procurando seu manga....")
    print(MangaApiClient.getManga(title))

def getMangaListTeste():
    print("Sugestão: 6b1eb93e-473a-4ab3-9922-1a66d2a29a4a é o id do mangá do Naruto")
    idManga = "6b1eb93e-473a-4ab3-9922-1a66d2a29a4a"
    print(MangaApiClient.getMangaList(idManga))

def getMangasPagesTeste():
    print("Sugestão: 0725c4e1-0af9-480d-8c4a-ab266ca0526b é o cap 601 do naruto")
    idPage = input("Passa o id do captitulo ai: ")
    print(MangaApiClient.getMangasPages(idPage))

def pasteCreateTeste():
    teste = f"{desktop_path}/MangaWave/naruto/volume63/chapter601"
    print(CreateFile.pasteCreate(teste))

while True:
    print("--- Bem vindo ao ambiente de teste do mangaWave ---")
    print("1: Buscar um mangá pelo titulo")
    print("2: Buscar os capítulos relacionado ao id mangá")
    print("3: Buscar as páginas relacionadas ao capítulo do mangá")
    print("4: Criação de pasta")
    print("5: Sair")

    option = int(input("Selecione o item que deseja testar: "))

    if option == 1:
        getMangaTeste()
    elif option == 2:
        getMangaListTeste()
    elif option == 3:
        getMangasPagesTeste()
    elif option == 4:
        pasteCreateTeste()
    elif option == 5:
        print("Até mais!")
        break
    else:
        print("Número inválido")
