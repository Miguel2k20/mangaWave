import customtkinter
from MangaApiClient import MangaApiClient

app = customtkinter.CTk()
app.geometry("650x400")
app.title("MangaWave")
customtkinter.set_appearance_mode("dark")

app.minsize(950, 500)

def getInputValue():
    print(MangaApiClient.getManga(entry.get()))

title = customtkinter.CTkLabel(
    master=app, 
    text="O que vamos ler hoje?", 
    font=("arial", 20)
)

entry = customtkinter.CTkEntry(
    master=app, 
    placeholder_text="Que mangá você está buscando?", 
    width=450,
    font=("arial", 15)
)

btn = customtkinter.CTkButton(
    master=app, 
    text="Buscar", 
    command=getInputValue
)

mangaResults =  customtkinter.CTkScrollableFrame(
    master=app, 
    width=900,
    height = 300,
    fg_color="#fff"
)


title.pack(anchor="center", pady=(20, 5))  # Espaçamento maior em cima, menor embaixo
entry.pack(anchor="center", pady=(5, 5))   # Espaçamento pequeno em cima e embaixo
btn.pack(anchor="center", pady=(5, 20))  
mangaResults.pack(expand=True)

app.mainloop()