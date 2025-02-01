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
        height=0.7 * page.height,  # Substituído por page.height
        width=page.width  # Substituído por page.width
    )

    mangaChapters = MangaApiClient.getMangaList(idManga)

    def printResult(mangas):
        progressRow.visible = False
        
        volumes = mangas['data']

        main_column = ft.Column(scroll=ft.ScrollMode.AUTO)
        processed_chapters = []

        # Primeiro for loop é referente aos volumes 
        def custom_sort_key(key):
            if key.isdigit():
                return int(key)
            else:
                return float('inf')

        for vol_num in sorted(volumes.keys(), key=custom_sort_key):
            chapters = volumes[vol_num]
            chapter_column = ft.Column()
            capters_id = []

            # For loop dos capítulos
            for chapter in chapters:
                # Evita repetição de capítulos de grupos diferentes
                chapter_volume = chapter['attributes']['volume']
                chapter_number = chapter['attributes']['chapter']
                if (chapter_volume, chapter_number) in processed_chapters:
                    continue 
                
                processed_chapters.append((chapter_volume, chapter_number, ))
                capters_id.append(chapter['id'])

                chapter_column.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.PICTURE_AS_PDF,
                                        tooltip=f"Baixar capítulo {chapter['attributes']['chapter']} em formato PDF"
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.MENU_BOOK,
                                        tooltip=f"Baixar capítulo {chapter['attributes']['chapter']} em formato Mobi"
                                    ),
                                ]),
                                ft.Column([
                                    ft.ListTile(
                                        title=ft.Text(f"Capítulo {chapter['attributes']['chapter']}"),
                                        subtitle=ft.Text(chapter['attributes']['title'] or "Sem título"),
                                    ),
                                ]),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor="#3d444d",
                        padding=ft.padding.symmetric(horizontal=10),
                        border_radius=10,
                    )
                )

            # Container de cada volume
            volume_container = ft.Container(
                content=ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"Volume - {vol_num}",
                                size=20, 
                            ),
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.PICTURE_AS_PDF,
                                    tooltip=f"Baixar Volume {vol_num} em formato PDF"
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.MENU_BOOK,
                                    tooltip=f"Baixar Volume {vol_num} em formato Mobi"
                                ),
                            ]),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    chapter_column,  # Aqui eu adiciono os capítulos que foram processados anteriormente
                    ft.Divider(height=1)
                ]),
                margin=ft.margin.only(bottom=5),
            )
            main_column.controls.append(volume_container)

        resultschapters.content = main_column
        resultschapters.visible = True
        page.update()

    if mangaChapters:
        printResult(mangaChapters)
    
    # print(json.dumps(mangaChapters, indent=4))

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
                progressRow,
                resultschapters
            ],
        )
    )