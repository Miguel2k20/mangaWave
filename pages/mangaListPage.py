import flet as ft
from flet import MainAxisAlignment, CrossAxisAlignment

def main(page: ft.Page):

    # NAAAAAAAAAAAAO É AQUIIIIIIIIIIIIIIIIIIIII
    page.views.append(
        ft.View(
            route='/mangas-list',
            controls=[
                ft.AppBar(title=ft.Text('NÃO É AQUIIIIII - Lista de Mangas Salvos')),
                ft.Text(value='Naruto!', size=30),
            ],
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )
