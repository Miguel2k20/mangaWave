import flet as ft
from flet import RouteChangeEvent, CrossAxisAlignment, MainAxisAlignment


def main(page: ft.Page):
    page.title = 'MangaWave'

    def route_change(e: RouteChangeEvent):
        page.views.clear()

        # Página Home
        if page.route == '/':
            page.views.append(
                ft.View(
                    route='/',
                    controls=[
                        ft.AppBar(title=ft.Text('MangaWave - Home')),
                        ft.Text(
                            value='Bem vindo ao MangaWave!', 
                            size=30
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text='Buscar Manga',
                                    on_click=lambda _: page.go('/mangas-get'),
                                ),
                                ft.ElevatedButton(
                                    text='Meus Mangas baixados',
                                    on_click=lambda _: page.go('/mangas-list'),
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER
                        ),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        # Página De Busca De Mangas
        elif page.route == '/mangas-get':

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
                    ],
                    # vertical_alignment=MainAxisAlignment.CENTER,
                    # horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == '/mangas-list':
            page.views.append(
                ft.View(
                    route='/mangas-list',
                    controls=[
                        ft.AppBar(title=ft.Text('MangaWave - Lista De Mangas Salvos')),
                        ft.Text(value='Sua lista de mangas ai carai', size=30),
                        ft.ElevatedButton(
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


