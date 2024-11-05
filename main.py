import customtkinter
from MangaApiClient import MangaApiClient

def button_callback():
    print("button clicked")

app = customtkinter.CTk()
app.geometry("500x400")
customtkinter.set_appearance_mode("dark")

def getInputValue():
    print(MangaApiClient.getManga(entry.get()))

entry = customtkinter.CTkEntry(master=app, placeholder_text="Que mangá você está buscando?", width=300) 
btn = customtkinter.CTkButton(master=app, text="Buscar", command=getInputValue)

entry.pack(anchor="s", expand=True, pady=10)
btn.pack(anchor="n", expand=True)

app.mainloop()