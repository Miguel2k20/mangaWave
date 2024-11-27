import customtkinter
from getMangaInterface import main

def button_callback():
    print("button pressed")
    main()

app = customtkinter.CTk()
app.title("MangaWave")
app.geometry("950x650")
app.minsize(950, 650)
customtkinter.set_appearance_mode("dark")

menuSpace = customtkinter.CTkFrame(
    app,
    height=500,
    border_color="#fff",
    border_width=1
)

menuSpace.pack(expand=True)

maintitle = customtkinter.CTkLabel(
    menuSpace,
    text="Bem Vindo ao MangaWave",
    font=("Arial", 24)
)

entry = customtkinter.CTkEntry(
    menuSpace, 
    placeholder_text="Que Manga nós vamos ler hoje?",
    width=350
)

buttonSearch = customtkinter.CTkButton(
    menuSpace,
    text="Buscar", 
    command=button_callback
)

buttonAnime = customtkinter.CTkButton(
    menuSpace,
    text="Seus Mangas", 
    command=button_callback
)

app.grid_columnconfigure(0, weight=0) 
app.grid_columnconfigure(1, weight=1) 
app.grid_columnconfigure(2, weight=0) 


maintitle.grid(
    row=0,
    column=1,
    columnspan=2,
    pady=(25, 10),
    padx=50
)

entry.grid(
    row=1,
    column=1,
    columnspan=2,
    pady=(10, 10),
    padx=50
)

buttonSearch.grid(
    row=2,
    column=1, 
    padx=(80,0),
    pady=(0,25) 
)

buttonAnime.grid(
    row=2,
    column=2, 
    padx=(0,80),
    pady=(0,25) 
)

app.mainloop()
