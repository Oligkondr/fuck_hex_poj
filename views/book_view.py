# Здесь должно быть представление для работы с книгами согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox

class BookView(ttk.Frame):
    def __init__(self, parent, book_controller) -> None:
        super().__init__(parent)
        self.book_controller = book_controller
        self.create_widgets()
        self.refresh_books()

    def create_widgets(self) -> None:
        # Строка поиска
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=5, padx=5)

        ttk.Label(search_frame, text="Search").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_books())

        # Таблица с книгами
        columns = ("id", "title", "author", "isbn", "year", "quantity", "available")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(expand=True, fill="both")

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="Add Book", command=self.add_book).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Delete Book", command=self.delete_selected).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Borrow Book", command=self.borrow_selected).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Return Book", command=self.return_selected).pack(
            side="left", padx=5
        )

    def refresh_books(self) -> None:
        query = self.search_var.get().strip()
        if query:
            books = self.book_controller.search_books(query)
        else:
            books = self.book_controller.get_all_books()

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for book in books:
            self.tree.insert(
                "",
                "end",
                values=(
                    book.id,
                    book.title,
                    book.author,
                    book.isbn,
                    book.year,
                    book.quantity,
                    getattr(
                        book, "available", book.quantity
                    ),  # available может быть атрибутом
                ),
            )

    def add_book(self) -> None:
        def add_book():
            title = title_var.get().strip()
            author = author_var.get().strip()
            isbn = isbn_var.get().strip()
            year = year_var.get().strip()
            quantity = quantity_var.get().strip()

            if (
                not title
                or not author
                or not isbn
                or not year.isdigit()
                or not quantity.isdigit()
            ):
                messagebox.showerror("Error", "Please enter valid data")
                return

            self.book_controller.add_book(title, author, isbn, int(year), int(quantity))
            self.refresh_books()
            add_win.destroy()

        add_win = tk.Toplevel(self)
        add_win.title("Add book")

        container = tk.Frame(add_win, padx=20, pady=20)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Title:").pack()
        title_var = tk.StringVar()
        ttk.Entry(container, textvariable=title_var).pack(pady=(0, 10))

        ttk.Label(container, text="Author:").pack()
        author_var = tk.StringVar()
        ttk.Entry(container, textvariable=author_var).pack(pady=(0, 10))

        ttk.Label(container, text="ISBN:").pack()
        isbn_var = tk.StringVar()
        ttk.Entry(container, textvariable=isbn_var).pack(pady=(0, 10))

        ttk.Label(container, text="Year:").pack()
        year_var = tk.StringVar()
        ttk.Entry(container, textvariable=year_var).pack(pady=(0, 10))

        ttk.Label(container, text="Quantity:").pack()
        quantity_var = tk.StringVar()
        ttk.Entry(container, textvariable=quantity_var).pack(pady=(0, 10))

        ttk.Button(container, text="Add Book", command=add_book).pack()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No book selected")
            return

        for sel in selected:
            book_id = self.tree.item(sel)["values"][0]
            self.book_controller.delete_book(book_id)
        self.refresh_books()

    def borrow_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No book selected to issue")
            return

        for sel in selected:
            book_id = self.tree.item(sel)["values"][0]
            success = self.book_controller.borrow_book(book_id)
            if not success:
                messagebox.showerror(
                    "Error", f"Cannot borrow. Book (ID {book_id}) is not available"
                )
        self.refresh_books()

    def return_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No book selected to return")
            return

        for sel in selected:
            book_id = self.tree.item(sel)["values"][0]
            success = self.book_controller.return_book(book_id)
            if not success:
                messagebox.showerror("Error", f"Cannot return book ID {book_id}")
        self.refresh_books()
