import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment

def main(page: ft.Page):
    page.views.append(
        ft.View(
            route='/mangas-list',
            controls=[
                ft.AppBar(title=ft.Text('MangaWave - Lista de Mangas Salvos')),
                ft.Text(value='Sua lista de mangas!', size=30),
                ft.ElevatedButton(
                    text='Voltar para Home',
                    on_click=lambda _: page.go('/'),
                ),
            ],
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )
