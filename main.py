import flet as ft
from pages.homePage import main as home_page
from pages.MangaList import main as manga_get_page
from pages.MangachaptersPage import main as manga_list_page



def main(page: ft.Page):
    
    page.title = 'MangaWave'
    page.theme_mode = "dark"

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        match page.route.split("?")[0]:
            case '/':
                home_page(page)
            case '/mangas-get':
                manga_get_page(page)
            case '/manga-list-page':
                params = page.route.split("?")[1] if "?" in page.route else ""
                params_dict = dict(param.split("=") for param in params.split("&") if "=" in param)
                id_value = params_dict.get("id", None)
                manga_list_page(page, id_value)
            # case '/manga-list-page':
            #     manga_list_page(page)

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(main)
