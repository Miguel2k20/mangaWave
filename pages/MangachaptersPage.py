import flet as ft
from controller.MangaApiClient import MangaApiClient
from controller.Helpers import Helpers
from controller.CreateFile import CreateFile

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
        height=0.7 * page.height,
        width=page.width
    )

    mangaChapters = MangaApiClient.getMangaList(idManga)

    def downloadManga(mangaChapter, type, icon_button):
        icon_button.icon = ft.Icons.HOURGLASS_TOP
        page.update()

        match type:
            case 'PDF':
                CreateFile.pdfGenerator(mangaChapter) 
                success = False
                # success = CreateFile.pdfGenerator(mangaChapter) 
            case 'MOBI':
                print("Ainda paixin")
                success = False  # Simula falha
            case 'JPG':
                success = CreateFile.pasteCreate(mangaChapter) 

        if success:
            icon_button.icon = ft.Icons.CHECK_CIRCLE
        else:
            icon_button.icon = ft.Icons.ERROR  
        page.update()

    def navegatePaginate(page_number, mangaData):
        offset = (page_number - 1) * mangaData['limit']
        mangaChapters = MangaApiClient.getMangaList(idManga, offset)
        printResult(mangaChapters, page_number)

    def printResult(mangas, current_page=1):
        progressRow.visible = False
        volumes = mangas['data']
        main_column = ft.Column(scroll=ft.ScrollMode.AUTO)
        processed_chapters = []
        paginate = Helpers.paginateGenerate(mangas['total'], mangas['limit'], mangas['offset'])

        def custom_sort_key(key):
            return int(key) if key.isdigit() else float('inf')

        for vol_num in sorted(volumes.keys(), key=custom_sort_key):
            chapters = volumes[vol_num]
            chapter_column = ft.Column()
            capters_id = []

            for chapter in chapters:
                chapter_volume = chapter['attributes']['volume']
                chapter_number = chapter['attributes']['chapter']
                if (chapter_volume, chapter_number) in processed_chapters:
                    continue 

                processed_chapters.append((chapter_volume, chapter_number))
                capters_id.append(chapter['id'])

                # Cria os botões antes de usá-los no lambda
                pdf_button = ft.IconButton(
                    icon=ft.Icons.PICTURE_AS_PDF,
                    tooltip=f"Baixar capítulo {chapter['attributes']['chapter']} em formato PDF"
                )
                mobi_button = ft.IconButton(
                    icon=ft.Icons.TABLET_ANDROID,
                    tooltip=f"Baixar capítulo {chapter['attributes']['chapter']} em formato Mobi"
                )
                jpg_button = ft.IconButton(
                    icon=ft.Icons.IMAGE,
                    tooltip=f"Baixar as imagens do capítulo {chapter['attributes']['chapter']} separadamente"
                )

                # Define os eventos de clique após a criação dos botões
                pdf_button.on_click = lambda e, chapter=chapter, button=pdf_button: downloadManga(chapter, 'PDF', button)
                mobi_button.on_click = lambda e, chapter=chapter, button=mobi_button: downloadManga(chapter, 'MOBI', button)
                jpg_button.on_click = lambda e, chapter=chapter, button=jpg_button: downloadManga(chapter, 'JPG', button)

                chapter_column.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Row([
                                    pdf_button, 
                                    mobi_button, 
                                    jpg_button
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
                        bgcolor=ft.Colors.GREY_900,
                        padding=ft.padding.symmetric(horizontal=10),
                        border_radius=10,
                    )
                )

            volume_container = ft.Container(
                content=ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(f"Volume - {vol_num}", size=20),
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
                    chapter_column,
                    ft.Divider(height=1)
                ]),
                margin=ft.margin.only(bottom=5),
            )
            main_column.controls.append(volume_container)

        if paginate and paginate[0] != paginate[1]:
            buttonsPage = [
                ft.ElevatedButton(
                    text=str(pageNumber),
                    on_click=lambda e, page_number=pageNumber: navegatePaginate(page_number, mangas),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE if pageNumber == current_page else ft.Colors.GREY,  
                        color=ft.Colors.WHITE if pageNumber == current_page else ft.Colors.BLACK
                    )
                ) for pageNumber in range(paginate[0], paginate[1] + 1)
            ]
            main_column.controls.append(
                ft.Row(
                    controls=buttonsPage,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )

        resultschapters.content = main_column
        resultschapters.visible = True
        page.update()

    if mangaChapters:
        printResult(mangaChapters)
    
    page.views.append(
        ft.View(
            route='/manga-list-page',
            controls=[
                ft.AppBar(
                    title=ft.Text('MangaWave - Nome do Manga foda-se'),
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