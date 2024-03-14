import sys
import os
main_dir = os.path.dirname( __file__ )
modules_dir = os.path.join( main_dir, '..')
sys.path.append( modules_dir )

import shift_register as SR
import time

import customtkinter
from tkinter import messagebox
from common_functions import CommonFunctions
import platform

#import schemdraw
#import schemdraw.elements as elm

# Check operating system
def check_os(status):
    match status:
        case "Linux":
            visualizador = "start"
            return visualizador
        case "Windows":
            visualizador = "xdg-open"
            return visualizador
        case "Darwin": # Verifica se é Mac
            visualizador = "open"  # macOS
            return visualizador
status = platform.system()
check_os(status)

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

#current_measure760  = 0b0010
rele_1K = 0b1010
# bit a ZERO activa o relé

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.selected_value = None  # Inicialmente, nenhum valor está selecionado
        self.common_functions = CommonFunctions() 
        
        self.geometry("500x350")
        self.title("VISIR")  
        
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Lei de Ohm")
        self.tabview.add("Lei de Kirchhoff")
        self.tabview.add("Díodo/Transistor")
        
        self.instructions_intro = customtkinter.CTkLabel(self.tabview.tab("Lei de Ohm"), text="Escolha só uma opção\nblá, blá, wiskas saquetas", corner_radius=6)
        self.instructions_intro.grid(row=0, column=0, padx=10, pady=10, sticky="ew") 

        self.instructions_intro = customtkinter.CTkLabel(self.tabview.tab("Lei de Kirchhoff"), text="Escolha só uma opção\nblá, blá, wiskas saquetas", corner_radius=6)
        self.instructions_intro.grid(row=0, column=0, padx=10, pady=10, sticky="ew") 
        
        self.checkbox_frame_Ohm = CheckboxFrame(self.tabview.tab("Lei de Ohm"), values=["1K", "2K", "3K"])
        self.checkbox_frame_Ohm.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.checkbox_frame_Kirchhoff = CheckboxFrame(self.tabview.tab("Lei de Kirchhoff"), values=["10K", "20K", "30K"])
        self.checkbox_frame_Kirchhoff.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")     
        
        self.button = customtkinter.CTkButton(self, text="OK/SEGUINTE", command=self.button_callback)
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        # Botão "Cancelar" que fecha a janela atual
        
        self.button_cancel = customtkinter.CTkButton(self, text="Cancelar", command=self.quit)
        self.button_cancel.grid(row=2, column=1, padx=10, pady=10)
        
    def button_callback(self):
        checked_checkboxes = self.checkbox_frame_Ohm.get()
        if len(checked_checkboxes) != 1:
            messagebox.showerror("Erro", "Selecione apenas uma opção.")
        else:
            option = checked_checkboxes[0]  # Obtém a opção selecionada
            SR.register_clear()
            time.sleep(1)
            SR.SRoutput(rele_1K)
            self.common_functions.option_output(option)

    def safe_close(self):
        if self.winfo_exists():  # Verificar se a janela ainda existe
            self.withdraw()  # Esconder a janela
            self.destroy()  # Destruir a janela
            
class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.checkboxes = []

        for i, value in enumerate(values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = [checkbox.cget("text") for checkbox in self.checkboxes if checkbox.get() == 1]
        return checked_checkboxes


app = MainWindow()
app.mainloop()
