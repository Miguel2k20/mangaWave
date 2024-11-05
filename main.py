import customtkinter

def button_callback():
    print("button clicked")

app = customtkinter.CTk()
app.geometry("500x400")

customtkinter.set_appearance_mode("dark")

button = customtkinter.CTkButton(app, text="my button", command=button_callback)
button.pack(padx=20, pady=20)

app.mainloop()