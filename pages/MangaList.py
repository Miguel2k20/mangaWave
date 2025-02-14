import flet as ft
from controller.MangaApiClient import MangaApiClient
from controller.Helpers import Helpers

def main(page: ft.Page):

    inputManga = ft.TextField(
        label="Nome Do Mangá",
        bgcolor='#3d444d',
        color='#ffffff'
    )

    progressRow = ft.Row(
        controls=[
            ft.ProgressRing(width=16, height=16, stroke_width=2), 
            ft.Text("Procurando Seu mangá...")
        ],
        visible=False
    )

    pageTitle = ft.Text(
        value='Resultados para Naruto', 
        size=30,
        visible=False
    )

    resultsManga = ft.Row(
        controls=[],
        wrap=True,
        visible=False,
        scroll=ft.ScrollMode.AUTO,
        height=0.7 * page.height  # Corrigido aqui
    )

    def getMangaList(offset=0):
        progressRow.visible = True
        resultsManga.visible = False
        page.update()

        mangaData = MangaApiClient.getManga(inputManga.value, offset)
        if mangaData:
            printResult(inputManga.value, mangaData, (offset // mangaData['limit']) + 1)  # Passa a página atual
        else:
            pageTitle.value = f"Resultado de {inputManga.value}"

        progressRow.visible = False
        pageTitle.visible = True
        page.update()

    def navegatePaginate(page_number, mangaData):
        offset = (page_number - 1) * mangaData['limit']
        getMangaList(offset)  

    def goToList(e):
        route = f"/manga-list-page?id={e}"
        page.go(route)
        

    def printResult(title, result, current_page=1):  # Adiciona current_page como parâmetro
        pageTitle.value = f"Resultado de {title} ({result['total']} resultado{'s' if result['total'] > 1 else ''})"
        paginate = Helpers.paginateGenerate(result['total'], result['limit'], result['offset'])

        resultsManga.controls = [
            ft.Container(
                on_click=lambda e, index=index: goToList(index),
                content=ft.Column([
                    ft.Image(src=manga['cover_art'], width=0.20 * page.width, height=300),  # Corrigido aqui
                    ft.Text(manga['title'], size=18),
                    ft.Text(f"Idiomas Disponiveis: {', '.join([lang for lang in manga['lenguangesEnsabled'] if lang in ['en', 'pt-br']])}", size=14)
                ], 
                alignment="center", horizontal_alignment="center"),
                padding=10,
                width=0.32 * page.width,  # Corrigido aqui
                height=450,
                border_radius=10,
                bgcolor="#3d444d"
            ) for index, manga in result['data'].items()
        ]

        if paginate and paginate[0] != paginate[1]:
            buttonsPage = [
                ft.ElevatedButton(
                    text=str(pageNumber),
                    on_click=lambda e, page_number=pageNumber: navegatePaginate(page_number, result),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE if pageNumber == current_page else ft.Colors.GREY,  
                        color=ft.Colors.WHITE if pageNumber == current_page else ft.Colors.BLACK
                    )
                ) for pageNumber in range(paginate[0], paginate[1] + 1)
            ]
            resultsManga.controls.append(
                ft.Row(
                    controls=buttonsPage,
                    alignment=ft.MainAxisAlignment.CENTER  # Centraliza os botões de paginação
                )
            )

        resultsManga.visible = True
        page.update()

    page.views.append(
        ft.View(
            route='/mangas-get',
            controls=[
                ft.AppBar(
                    title=ft.Text('MangaWave - Buscar Manga'),
                    leading=ft.IconButton(
                        icon="ARROW_BACK_IOS",
                        on_click=lambda _: page.go('/'),
                    ),
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=inputManga,
                            width=0.4 * page.width,  # Corrigido aqui
                        ),
                        ft.ElevatedButton(
                            text="Pesquisar", 
                            on_click=lambda e: getMangaList(0),
                            icon="SEARCH",
                        )
                    ]
                ),
                progressRow,
                pageTitle,
                resultsManga
            ]
        )
    )