import tkinter as tk

window = tk.Tk()
window.title("MangaWave")


label = tk.Label(window, text="Olá teste foda")
label.pack()

def on_button_click():
    label.config(text="SHIT!")

button = tk.Button(window, text="Clica ai bro", command=on_button_click)
button.pack()

window.mainloop()
