# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.book_view import BookView
from views.reader_view import ReaderView
from views.loan_view import LoanView

class MainWindow(tk.Tk):
    def __init__(self, book_controller, reader_controller, loan_controller) -> None:
        super().__init__()
        self.title("Library Management System")
        self.geometry("1000x700")

        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.loan_controller = loan_controller

        self.create_menu()
        self.create_notebook()

    def create_menu(self) -> None:
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_notebook(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Book tab
        book_frame = ttk.Frame(notebook)
        self.book_view = BookView(book_frame, self.book_controller)
        notebook.add(book_frame, text="Books")

        # Reader tab
        reader_frame = ttk.Frame(notebook)
        self.reader_view = ReaderView(reader_frame, self.reader_controller)
        notebook.add(reader_frame, text="Readers")

        # Loan tab
        loan_frame = ttk.Frame(notebook)
        self.loan_view = LoanView(loan_frame, self.loan_controller, 
                                 self.book_controller, self.reader_controller)
        notebook.add(loan_frame, text="Loans")