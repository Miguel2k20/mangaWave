import flet as ft
from flet import View, Page, AppBar, ElevatedButton, Text
from flet import RouteChangeEvent, CrossAxisAlignment, MainAxisAlignment

def main(page: Page):
    page.title = 'MangaWave'

    def route_change(e: RouteChangeEvent):
        page.views.clear()

        # Página Home
        if page.route == '/':
            page.views.append(
                View(
                    route='/',
                    controls=[
                        AppBar(title=Text('MangaWave - Menu')),
                        Text(value='Como posso ajudar?', size=30),
                        ElevatedButton(
                            text='Buscar Manga',
                            on_click=lambda _: page.go('/mangas-get'),
                        ),
                        ElevatedButton(
                            text='Meus Mangas baixados',
                            on_click=lambda _: page.go('/mangas-list'),
                        ),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        # Página De Busca De Mangas
        elif page.route == '/mangas-get':
            page.views.append(
                View(
                    route='/mangas-get',
                    controls=[
                        AppBar(title=Text('MangaWave - Busca')),
                        Text(value='Na teoria, vou por a lista de mangas aqui', size=30),
                        ElevatedButton(
                            text='Voltamo la pra home?',
                            on_click=lambda _: page.go('/'),
                        ),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == '/mangas-list':
            page.views.append(
                View(
                    route='/mangas-list',
                    controls=[
                        AppBar(title=Text('MangaWave - Lista De Mangas Salvos')),
                        Text(value='Sua lista de mangas ai carai', size=30),
                        ElevatedButton(
                            text='Voltamo la pra home?',
                            on_click=lambda _: page.go('/'),
                        ),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    page.on_route_change = route_change

    page.go(page.route)

ft.app(main)
