import flet as ft
from pages.homePage import main as home_page
from pages.getMangaPage import main as manga_get_page
from pages.getMangaPage import main as manga_list_page


def main(page: ft.Page):
    
    page.title = 'MangaWave'
    page.theme_mode = "dark"

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
