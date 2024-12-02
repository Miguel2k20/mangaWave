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

    resultschapters = ft.Row(
        controls=[],
        wrap=True,
        visible=False,
        scroll=ft.ScrollMode.AUTO,
        height=0.7 * page.window_height
    )
    
    mangaChapters = MangaApiClient.getMangaList(idManga)

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
                progressRow,
                resultschapters
            ],
        )
    )
