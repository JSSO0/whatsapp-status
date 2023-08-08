import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from tkinter.filedialog import askopenfilename, asksaveasfilename
from driver import GetStatus
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import threading
import time


class UI():
    
    def __init__(self):        
        self.root = tk.Tk()
        self.driver = GetStatus()

        self.root.geometry("550x550")
        self.root.resizable(False, False)
        self.root.title("WhatsApp Status")
        self.root.iconbitmap("Project\logo.ico")

        self.create_ui_elements()

    def create_ui_elements(self):
        self.create_header_frame()
        self.create_message_list()
        self.create_input_frame()

    def create_header_frame(self):
        self.header_frame = tk.Frame(self.root, bg="#25D366")
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        self.title_label = tk.Label(self.header_frame, text="WhatsApp Status", font=("Helvetica", 16), fg="white", bg="#25D366")
        self.title_label.pack(side=tk.LEFT, expand=True)

        self.style = ttk.Style()
        self.style.configure("Login.TButton", padding=3, relief="solid", borderwidth=3, font=("Helvetica", 12), background="#25D366")
        self.login_button = ttk.Button(self.header_frame, text="Login", style="Login.TButton", command=lambda: self.login())
        self.login_button.pack(side=tk.RIGHT)
        
        self.link_label = ttk.Button(self.header_frame, text="Github repository", style="Login.TButton")
        self.link_label.pack(side=tk.RIGHT)
        self.link_label.bind("<Button-1>", lambda event: self.driver.github())

    def create_message_list(self):
        self.message_frame = tk.Frame(self.root, bg="white")
        self.message_frame.pack(fill=tk.BOTH, expand=True)

        self.message_scrollbar = tk.Scrollbar(self.message_frame)
        self.message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_list = tk.Listbox(self.message_frame, yscrollcommand=self.message_scrollbar.set)
        self.message_list.pack(fill=tk.BOTH, expand=True)

        self.message_scrollbar.config(command=self.message_list.yview)

    def create_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg="#F7F7F7", bd=5)
        self.input_frame.pack(fill=tk.X, pady=10)

        self.input_entry = tk.Entry(self.input_frame, font=("Helvetica", 20))
        self.input_entry.pack(fill=tk.X, expand=True, padx=5, pady=3)
        self.input_entry.bind("<Return>", self.add_message)

        self.style.configure("Round.TButton", padding=3, relief="solid", borderwidth=0, font=("Helvetica", 12), shape="circle", background="#F7F7F7", corner_radius=10)
        self.upload_button = ttk.Button(self.input_frame, text="Upload File", style="Round.TButton", command=self.upload_file)
        self.downloadall_button = ttk.Button(self.input_frame, text="Download File", style="Round.TButton", command=self.download_all)
        self.upload_button.pack(side=tk.LEFT, pady=1, padx=1)
        self.downloadall_button.pack(side=tk.RIGHT, pady=1, padx=1)

    def upload_file(self):
        file_path = askopenfilename()
        if file_path.endswith(('.csv', '.xlsx')):
            self.data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

            arr = np.array(self.data.columns[0])
            data_list = self.data[arr].tolist()

            self.resultCSV = {}
            for index, n in enumerate(data_list, 1):
                isDuplicate, duplicateIndex = False, 0

                if n in self.resultCSV:
                    isDuplicate = True
                    duplicateIndex = list(self.resultCSV.keys()).index(n)

                self.message_list.insert(tk.END, f"{index} - Validando {n}...")
                self.message_list.see(tk.END)
                self.root.update()

                status = self.check(n) if not isDuplicate else "Número duplicado."
                self.resultCSV[duplicateIndex] = status
                self.resultCSV[n] = status
                print(self.resultCSV[n])

                self.root.update()

            self.driver.login()

            self.message_list.insert(tk.END, "", f"Sua verificação terminou para {len(data_list)} numeros.", "")
            self.message_list.insert(tk.END, "Agora você pode baixar os resultados.")
            self.message_list.see(tk.END)
            self.root.update()

    def download_all(self):
        self.data['Status'] = list(self.resultCSV.values())
        file_path = asksaveasfilename(defaultextension='.csv', initialfile='Results.csv')
        self.data.to_csv(file_path, index=False)

    def checkOne(self):
        self.input_entry.unbind("<Return>")
        self.popup = tk.Toplevel(self.root)
        self.setup_popup_window(self.popup, "Single Check")

        title_label = tk.Label(self.popup, text="Username:", bg='#25D366', fg='white', font=("TkDefaultFont", 14))
        title_label.pack(pady=(10, 0))

        self.popup_entry = tk.Entry(self.popup, font=("TkDefaultFont", 14), bg='#fff', fg='black')
        self.popup_entry.pack()

        self.popup.bind("<Return>", lambda event, entry=self.popup_entry: self.popup_action(event))

    def setup_popup_window(self, window, title):
        window.title(title)
        window.iconbitmap("Project\logo.ico")
        window.geometry("200x100")
        window.configure(bg='#25D366')
        window.resizable(0, 0)

        x = (self.root.winfo_screenwidth() - window.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - window.winfo_reqheight()) / 2
        window.geometry("+%d+%d" % (x, y))

        window.grab_set()

    def popup_action(self, event):
        popup_text = self.popup_entry.get()
        self.message_list.insert(tk.END, popup_text)
        self.popup.destroy()
        self.root.bind("<Return>", lambda event, entry=self.input_entry: self.add_message(event))

    def add_message(self, event):
        text = self.input_entry.get()
        self.check(text)

    def check(self, id):
        id = str(id)
        
        if len(id) == 11 or len(id) == 13 or len(id) == 12:
            if len(id) == 13:
                number = id
            else:
                number = "55" + id
            
            status = self.driver.run(number)
        else:
            status = "Número inválido"
        
        return status