import flet as ft
from controller.MangaApiClient import MangaApiClient
import json

def main(page: ft.Page, idManga):


    progressRow = ft.Row(
        controls=[
            ft.ProgressRing(width=16, height=16, stroke_width=2), 
            ft.Text("Buscando seus capítulos...")
        ],
        visible=True
    )
    
    mangaChapters = MangaApiClient.getMangaList(idManga)
    print(json.dumps(mangaChapters, indent=4))

    page.views.append(
        ft.View(
            route='/manga-list-page',
            controls=[
                ft.AppBar(
                    title=ft.Text('MangaWave - Buscar Manga'),
                    leading=ft.IconButton(
                        icon="ARROW_BACK_IOS",
                        on_click=lambda _: page.go('/mangas-get'),
                    ),
                ),
                ft.Text(value='Naruto!', size=30),
                progressRow
            ],
        )
    )
