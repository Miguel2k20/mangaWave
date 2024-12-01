import flet as ft

def main(page: ft.Page):
    
    inputManga = ft.TextField(
        label="Nome Do Mangá",
        bgcolor='#3d444d',
        color='#ffffff'
    )

    def button_clicked(e):
        print(inputManga.value)

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
                            width=0.89 * page.window_width
                        ),
                        ft.ElevatedButton(
                            text="Pesquisar", 
                            on_click=button_clicked,
                            icon="SEARCH",
                            expand=True,
                        )
                    ]
                )
            ]
        )
    )
