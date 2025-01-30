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
        
        volumes = mangas['data']

        main_column = ft.Column(scroll=ft.ScrollMode.AUTO)

        # Primeiro for loop é referente aos volumes 
        for vol_num in sorted(volumes.keys(), key=lambda x: int(x)):
            
            chapters = volumes[vol_num]

            # Div pai dos volumes
            volume_container = ft.Container(
                content=ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Volume {vol_num}",
                                size=20, 
                            ),

                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.PICTURE_AS_PDF,
                                    tooltip=f"Baixar Volume {vol_num} em formato PDF"
                                ),
                                ft.IconButton(
                                    icon=ft.icons.MENU_BOOK,
                                    tooltip=f"Baixar Volume {vol_num} em formato Mobi"
                                ),
                            ])
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    # Container dos capitulos
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row([
                                    ft.Column([
                                        ft.Text(
                                            f"Capítulo {chapter['attributes']['chapter']}",
                                            size=10, 
                                        ),
                                        ft.Text(
                                            f"Titulo: {chapter['attributes']['title'] or "Sem título"}",
                                            size=12, 
                                        )
                                    ])
                                ]) for chapter in chapters
                            ],
                        ),
                    ),

                    ft.Divider(height=1),
                ]) 
            )
            main_column.controls.append(volume_container)

        resultschapters.content = main_column
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
