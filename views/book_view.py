# Здесь должно быть представление для работы с книгами согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

class BookView(ttk.Frame):
    def __init__(self, parent, book_controller) -> None:
        super().__init__(parent)
        self.book_controller = book_controller
        self.create_widgets()
        self.refresh_books()

    def create_widgets(self) -> None:
        # Main container
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for books
        self.tree = ttk.Treeview(self, columns=('id', 'title', 'author', 'isbn', 'year', 'quantity', 'available'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('author', text='Author')
        self.tree.heading('isbn', text='ISBN')
        self.tree.heading('year', text='Year')
        self.tree.heading('quantity', text='Qty')
        self.tree.heading('available', text='Avail')
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('quantity', width=50, anchor='center')
        self.tree.column('available', width=50, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="Refresh", command=self.refresh_books).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Borrow", command=self.borrow_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Return", command=self.return_book).pack(side=tk.LEFT, padx=5)

        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="Go", command=self.search_books).pack(side=tk.LEFT, padx=5)

        # Form for adding/editing books
        form_frame = ttk.LabelFrame(self, text="Book Form")
        form_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.author_entry = ttk.Entry(form_frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="ISBN:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.isbn_entry = ttk.Entry(form_frame)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="Year:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.year_entry = ttk.Entry(form_frame)
        self.year_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="Quantity:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=4, column=1, padx=5, pady=5, sticky='we')

        btn_subframe = ttk.Frame(form_frame)
        btn_subframe.grid(row=5, column=0, columnspan=2, pady=5)

        ttk.Button(btn_subframe, text="Save", command=self.save_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_subframe, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        form_frame.columnconfigure(1, weight=1)
        self.current_book_id: Optional[int] = None

    def refresh_books(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        books = self.book_controller.get_all_books()
        for book in books:
            self.tree.insert('', tk.END, values=(
                book.id,
                book.title,
                book.author,
                book.isbn,
                book.year,
                book.quantity,
                book.available
            ))

    def add_book(self) -> None:
        self.current_book_id = None
        self.clear_form()

    def delete_selected(self) -> None:
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return
        
        book_id = int(self.tree.item(selected, 'values')[0])
        if messagebox.askyesno("Confirm", "Delete this book?"):
            try:
                self.book_controller.delete_book(book_id)
                self.refresh_books()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

    def borrow_book(self) -> None:
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return

        book_id = int(self.tree.item(selected, 'values')[0])
        try:
            if self.book_controller.borrow_book(book_id):
                messagebox.showinfo("Success", "Book borrowed successfully")
                self.refresh_books()
            else:
                messagebox.showwarning("Warning", "No available copies to borrow")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to borrow book: {str(e)}")

    def return_book(self) -> None:
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return

        book_id = int(self.tree.item(selected, 'values')[0])
        try:
            if self.book_controller.return_book(book_id):
                messagebox.showinfo("Success", "Book returned successfully")
                self.refresh_books()
            else:
                messagebox.showwarning("Warning", "All copies are already returned")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def search_books(self) -> None:
        query = self.search_entry.get()
        if not query:
            self.refresh_books()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        books = self.book_controller.search_books(query)
        for book in books:
            self.tree.insert('', tk.END, values=(
                book.id,
                book.title,
                book.author,
                book.isbn,
                book.year,
                book.quantity,
                book.available
            ))

    def clear_form(self) -> None:
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.current_book_id = None

    def save_book(self) -> None:
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        year = self.year_entry.get()
        quantity = self.quantity_entry.get()

        if not all([title, author, isbn, year, quantity]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            year = int(year)
            quantity = int(quantity)

            if self.current_book_id:
                self.book_controller.update_book(
                    self.current_book_id,
                    title=title,
                    author=author,
                    isbn=isbn,
                    year=year,
                    quantity=quantity
                )
                messagebox.showinfo("Success", "Book updated successfully")
            else:
                self.book_controller.add_book(title, author, isbn, year, quantity)
                messagebox.showinfo("Success", "Book added successfully")
            
            self.refresh_books()
            self.clear_form()
        except ValueError:
            messagebox.showerror("Error", "Year and Quantity must be numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save book: {str(e)}")