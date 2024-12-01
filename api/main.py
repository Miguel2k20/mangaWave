import flet as ft
from pages.main import home_page
from pages.main import manga_get_page
from pages.main import manga_list_page


def main(page: ft.Page):
    page.title = 'MangaWave'

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        match page.route:
            case '/':
                home_page(page)
            case '/mangas-get':
                manga_get_page(page)
            case '/mangas-list':
                manga_list_page(page)
                
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(main)
