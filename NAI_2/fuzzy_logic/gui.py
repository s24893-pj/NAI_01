import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_classificator import PdfClassificator


class Application:
    def __init__(self):
        self.pdf_classificator = PdfClassificator()
        self.root = tk.Tk()
        self.root.title("Organizator CV PDF")
        self.root.geometry("500x350")
        self.root.configure(bg="#f7f7f7")

    def select_destination_folder(self) -> None:
        """
        Funkcja do wyboru folderu zawierającego CV

        :return:
        """
        self.pdf_classificator.cv_folder_path = filedialog.askdirectory(title="Wybierz folder zawierający CV")
        if self.pdf_classificator.cv_folder_path:
            messagebox.showinfo(
                "Folder wybrany",
                f"Wybrany folder: {self.pdf_classificator.cv_folder_path}",
            )
        else:
            messagebox.showwarning(
                "Brak folderu",
                "Nie wybrano folderu",
            )

    def open_gui(self) -> None:
        """
        Inicjalizacja GUI aplikacji

        :return:
        """
        header_label = tk.Label(
            self.root,
            text="Organizator CV PDF",
            font=("Helvetica", 18, "bold"),
            fg="#333",
            bg="#f7f7f7",
        )

        destination_button = tk.Button(
            self.root,
            text="Wybierz folder",
            command=self.select_destination_folder,
            font=("Helvetica", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
        )

        organize_button = tk.Button(
            self.root,
            text="Organizuj CV",
            command=lambda: self.pdf_classificator.classify_all_cvs(),
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
        )

        footer_label = tk.Label(
            self.root,
            text="Pliki zostaną zapisane w wybranym katalogu docelowym",
            font=("Helvetica", 10),
            bg="#f7f7f7",
            fg="#666",
        )

        header_label.pack(pady=20)
        destination_button.pack(pady=10)
        organize_button.pack(pady=20)
        footer_label.pack(side="bottom", pady=10)

        self.root.mainloop()
