import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment

def main(page: ft.Page):
    page.views.append(
        ft.View(
            route='/',
            controls=[
                ft.AppBar(title=ft.Text('MangaWave - Home')),
                ft.Text(
                    value='Bem-vindo ao MangaWave!', 
                    size=30
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text='Buscar Manga',
                            on_click=lambda _: page.go('/mangas-get'),
                        ),
                        ft.ElevatedButton(
                            text='Meus Mangas Baixados',
                            on_click=lambda _: page.go('/mangas-list'),
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
            ],
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )
