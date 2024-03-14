import customtkinter

app = customtkinter.CTk()
app.geometry("400x440")

MainTab = customtkinter.CTkTabview(app)
MainTab.pack(padx=20, pady=20)

MainTab.add("Lei de Ohm")
MainTab.add("Lei de Kirchhoff")
MainTab.add("Díodo/Transistor")

# add widgets on tabs
#MainTab.label = customtkinter.CTkLabel(master=self.tab("Lei de Ohm"))
#MainTab.label.grid(row=0, column=0, padx=20, pady=20)

checkbox_1 = customtkinter.CTkCheckBox (MainTab.tab("Lei de Ohm"), text="1K") 
checkbox_1.pack(padx=0, pady=20) 
checkbox_2 = customtkinter.CTkCheckBox (MainTab.tab("Lei de Ohm"), text="2K") 
checkbox_2.pack(padx=0, pady=20)
checkbox_3 = customtkinter.CTkCheckBox (MainTab.tab("Lei de Ohm"), text="3K") 
checkbox_3.pack(padx=0, pady=20)

checked_checkbox_2 = checkbox_2.get()
button = customtkinter.CTkButton(MainTab.tab("Lei de Ohm"), text="OK")
button.pack(padx=10, pady=10)

button_cancel = customtkinter.CTkButton(MainTab.tab("Lei de Ohm"), text="Cancelar")
button_cancel.pack(padx=10, pady=10)

checked_checkbox_1 = checkbox_1.get()

if checked_checkbox_1 == 0:
    option = checked_checkbox_1
    print(option)
else:
    print("merda")

app.mainloop()