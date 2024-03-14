import customtkinter
from tkinter import messagebox
import subprocess

import schemdraw
import schemdraw.elements as elm

# Caminho para o visualizador de imagens (pode variar dependendo do seu sistema operacional)
#visualizador = "xdg-open"  # Linux
# visualizador = "open"  # macOS
visualizador = "start"  # Windows

import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class OhmWindow(customtkinter.CTk):
    def __init__(self, title, values):
        super().__init__()
        
        self.common_functions = CommonFunctions()  
        # Criar uma instância de CommonFunctions para poder chamar outra função definida numa class 

        self.geometry("300x200")
        self.title("Lei Ohm")

        self.checkbox_frame = CheckboxFrame(self, "Escolha", values=values)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="OK", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10)

        self.button_cancel = customtkinter.CTkButton(self, text="Cancelar", command=self.destroy)
        self.button_cancel.grid(row=1, column=1, padx=10, pady=10)

    def button_callback(self):
        checked_checkboxes = self.checkbox_frame.get()
        if len(checked_checkboxes) != 1:
            messagebox.showerror("Erro", "Selecione apenas uma opção.")
        else:
            option = checked_checkboxes[0]  # Obtém a opção selecionada
            self.common_functions.option_output(option)

class KirchhoffWindow(customtkinter.CTk):
    def __init__(self, title, values):
        super().__init__()
        self.common_functions = CommonFunctions()  
        # Criar uma instância de CommonFunctions para poder chamar outra função definida numa class 

        self.geometry("300x200")
        self.title("Lei de Kirchhoff")

        self.checkbox_frame = CheckboxFrame(self, "Escolha", values=values)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")        
        
        self.button = customtkinter.CTkButton(self, text="OK", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10)
        
        self.button_cancel = customtkinter.CTkButton(self, text="Cancelar", command=self.destroy)
        self.button_cancel.grid(row=1, column=1, padx=10, pady=10)

    def button_callback(self):
        checked_checkboxes = self.checkbox_frame.get()
        if len(checked_checkboxes) != 1:
            messagebox.showerror("Erro", "Selecione apenas uma opção.")
        else:
            option = checked_checkboxes[0]  # Obtém a opção selecionada
            self.common_functions.option_output(option)


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.selected_value = None  # Inicialmente, nenhum valor está selecionado

        self.geometry("500x350")
        self.title("VISIR")
        self.grid_columnconfigure((0), weight=1)
        
        self.checkbox_frame = CheckboxFrame(self, "Circuitos", values=["Lei de Ohm", "Lei de Kirchhoff", "DíodoTransistor"])
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="OK/Seguinte", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        # Botão "Cancelar" que fecha a janela atual
        
        self.button_cancel = customtkinter.CTkButton(self, text="Cancelar", command=self.destroy)
        self.button_cancel.grid(row=1, column=1, padx=10, pady=10)

        #self.toplevel_window = None

    def button_callback(self):
        checked_checkboxes = self.checkbox_frame.get()
        if len(checked_checkboxes) != 1:
            messagebox.showerror("Erro", "Selecione apenas uma opção.")
        else:
            option = checked_checkboxes[0]  # Obtém a opção selecionada
        if option == "Lei de Ohm":
            self.new_window_Ohm = OhmWindow("Mais opções - Lei de Ohm", values=["1K", "2K", "3K"])
            self.new_window_Ohm.mainloop()
        elif option == "Lei de Kirchhoff":
            new_window_Kirchhoff = KirchhoffWindow("Mais opções - Lei de Kirchhoff", values=["10K", "20K", "30K"])
            new_window_Kirchhoff.mainloop()
        elif option == "DíodoTransistor":
            pass

class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.checkboxes = []

        title_label = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = [checkbox.cget("text") for checkbox in self.checkboxes if checkbox.get() == 1]
        return checked_checkboxes

class CommonFunctions:
    def option_output(self, option):
        self.draw_scheme(option)
        caminho_imagem = "esquemaOhm.jpg"
        subprocess.Popen([visualizador, caminho_imagem], shell=True)
        #subprocess.run(["python", "Menu//scheme.py"]) 
        print("OK")
        
    def draw_scheme(self, option):
        with schemdraw.Drawing(show=False) as d:
            d.config(unit=5) #tamanho do componente
            # Adicionando os elementos
            d += (V1 := elm.SourceV().label('Vin'))
            d += (I1 := elm.MeterA().right().label('Amp'))
            d += elm.Dot()
            d.push()
            d += (R1 := elm.Resistor().down().label(option, loc='bot'))
            d += elm.Dot()
            d.pop()
            d += (L1 := elm.Line())
            d += (Vol := elm.MeterV().down().label('Volt', loc='bot', rotate=True))
            d += (L2 := elm.Line().tox(V1.start))            
            #d.draw()
            d.save('esquemaOhm.jpg')


if __name__ == "__main__":
    app = App()
    app.mainloop()
