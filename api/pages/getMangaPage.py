import flet as ft
from controller.MangaApiClient import MangaApiClient
from pprint import pprint

def main(page: ft.Page):

    inputManga = ft.TextField(
        label="Nome Do Mangá",
        bgcolor='#3d444d',
        color='#ffffff'
    )

    progressRow = ft.Row(
        controls=[
            ft.ProgressRing(width=16, height=16, stroke_width = 2), 
            ft.Text("Procurando Seu mangá...")
        ],
        visible = False
    )

    pageTitle = ft.Text(
        value='Resultados para Naruto', 
        size=30,
        visible = False
    )

    resultsManga = ft.Row(
        controls=[],
        wrap=True,
        visible=False,
        scroll=ft.ScrollMode.AUTO,
        height=600
    )


    def button_clicked(e):
        progressRow.visible = True
        resultsManga.visible = False
        page.update()

        mangaData = MangaApiClient.getManga(inputManga.value)

        if mangaData:
            pageTitle.value = f"Resultado de {inputManga.value} ({mangaData['total']} resultado{'s' if mangaData['total'] > 1 else ''})"
            resultsManga.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Image(src=manga['cover_art'], width=0.20 * page.window_width, height=300),
                        ft.Text(manga['title'], size=18),
                        ft.Text(f"Idiomas Disponiveis: {', '.join(manga['lenguangesEnsabled'])}", size=14)
                    ], 
                    alignment="center", horizontal_alignment="center"),
                    padding=10,
                    width=0.3 * page.window_width,
                    border_radius=10,
                    bgcolor="#3d444d"
                ) for manga in mangaData['data'].values()
            ]

            resultsManga.visible = True
        else:
            pageTitle.value = f"Resultado de {inputManga.value}"
        
        progressRow.visible = False
        pageTitle.visible = True
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
                            width=0.4 * page.window_width,
                        ),
                        ft.ElevatedButton(
                            text="Pesquisar", 
                            on_click=button_clicked,
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
