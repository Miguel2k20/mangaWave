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

    resultschapters = ft.Container(
        content=ft.Column(
            controls=[], 
        ),
        visible=False,
        height=0.7 * page.window_height,
        width=page.window_width
    )

    mangaChapters = MangaApiClient.getMangaList(idManga)

    def printResult(mangas):
        progressRow.visible = False

        chapters = mangas['data']


        resultschapters.content = ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            value=f"Volume: {key}", 
                            size=24, 
                            weight="bold"
                        ),
                        [
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        value=f"Cap {chapter['attributes']['chapter']}",
                                        size=12
                                    ),
                                    ft.Text(
                                        value=f"Capítulo {chapter['attributes']['title']}",
                                        size=15
                                    )
                                ]
                            ) for chapter in chapters
                        ]
                    ]
                ) for key, chapters in chapters.items()
            ],
            scroll=ft.ScrollMode.AUTO
        )

        resultschapters.visible = True
        page.update()

    if mangaChapters:
        printResult(mangaChapters)
    
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
                # ft.Text(value='Naruto!', size=30),
                progressRow,
                resultschapters
            ],
        )
    )
