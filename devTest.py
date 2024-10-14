import MangaApiClient

print("Bem vindo ao mangaWave")

title = input("Fale ai o mangá que ce quer: ")

print("Procurando seu manga....")

print(MangaApiClient.getManga(title))

idManga = input("Passa o id do mangá ai: ")

print(MangaApiClient.getMangaList(idManga))

idPage = input("Passa o id do captitulo ai: ")

print(MangaApiClient.getMangasPages(idPage))