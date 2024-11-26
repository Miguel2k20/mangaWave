import customtkinter
import json
import io
import requests
from PIL import Image, ImageTk
from api.MangaApiClient import MangaApiClient
import math
import threading

def fetch_mangas(entry_text, offset, mangaResults, paginate, update_gui_callback):
    response = MangaApiClient.getManga(entry_text, offset=offset)
    data = response.get("data")
    total = response.get("total")  

    limit = 15  
    total_pages = math.ceil(total / limit)

    update_gui_callback(data, total_pages, mangaResults, paginate)

def update_gui(data, total_pages, mangaResults, paginate):
    for widget in mangaResults.winfo_children():
        widget.destroy()

    for manga_id, manga_info in data.items():
        frameResult = customtkinter.CTkFrame(
            mangaResults, 
            width=900, 
            height=100,
            fg_color = "#23272d"
        )

        frameResult.pack(expand=True)

        title = manga_info.get("title")

        cover_path = manga_info.get("cover_art")
        response = requests.get(cover_path)
        image_data = response.content  
        cover_image = Image.open(io.BytesIO(image_data))
        cover_photo = customtkinter.CTkImage(
            light_image=cover_image,
            size=(250,400)
        )
        cover_label = customtkinter.CTkLabel(
            frameResult,
            image=cover_photo,
            text=""
        )

        manga_title_label = customtkinter.CTkLabel(
            frameResult,
            text=f"{title}",
            text_color="#FFF",
            font=("arial", 25)
        )

        btn = customtkinter.CTkButton(
            frameResult, 
            text="Veja Mais", 
            font=("arial", 15),
            command=lambda manga_id=manga_id: getchaptersMangas(manga_id)
        )

        frameResult.pack(
            anchor="w",
            padx=10,
            pady=5,
            fill="both"
        )

        manga_title_label.pack(
            expand=True,
            pady=10,
            padx=10,
        )

        cover_label.pack(
            expand=True,
            pady=(0,10),
            padx=10,
        )

        btn.pack(
            anchor="center",
            pady=10
        )

    for widget in paginate.winfo_children():
        widget.destroy()

    for page in range(1, total_pages + 1):
        page_button = customtkinter.CTkButton(
            paginate, 
            text=str(page), 
            width=40,
            command=lambda page=page: getInputValue(offset=(page-1)*limit)  
        )
        page_button.pack(side="left", padx=5)

def start_manga_interface(app):
    def getchaptersMangas(mangaId):
        print(mangaId)

    def getInputValue(offset=0):
        entry_text = entry.get()
        
        threading.Thread(target=fetch_mangas, args=(entry_text, offset, mangaResults, paginate, update_gui), daemon=True).start()

    entrySpace =  customtkinter.CTkFrame(
        app, 
        width=925,
        height=15,
        fg_color = "#23272d"
    )

    entry = customtkinter.CTkEntry(
        entrySpace, 
        placeholder_text="Que mangá você está buscando?", 
        width=450,
        font=("arial", 15)
    )

    btn = customtkinter.CTkButton(
        entrySpace, 
        text="Buscar", 
        command=getInputValue
    )

    mangaResults =  customtkinter.CTkScrollableFrame(
        app, 
        width=900,
        height=550,
    )

    paginate = customtkinter.CTkFrame(
        app, 
        height=50,
        width=850,
    )

    entry.pack(
        side="left",
        padx=(5,0), 
    )   
    btn.pack(
        side="left",
        padx=5, 
    )  

    entrySpace.pack(
        expand=True,
        side="top"
    )
    mangaResults.pack(
        expand=True
    )
    paginate.pack(
        expand=True,
        side="bottom"
    )

def main():
    customtkinter.set_appearance_mode("dark")

    app = customtkinter.CTk()
    app.geometry("950x650")
    app.title("MangaWave")
    app.minsize(950, 650)

    start_manga_interface(app)

    app.mainloop()

main()
