# Здесь должно быть представление для работы с займами согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import Optional

class LoanView(ttk.Frame):
    def __init__(self, parent, loan_controller, book_controller, reader_controller) -> None:
        super().__init__(parent)
        self.loan_controller = loan_controller
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_loans()

    def create_widgets(self) -> None:
        # Main container
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for loans
        self.tree = ttk.Treeview(self, columns=('id', 'book_id', 'reader_id', 'loan_date', 'return_date', 'status'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('book_id', text='Book ID')
        self.tree.heading('reader_id', text='Reader ID')
        self.tree.heading('loan_date', text='Loan Date')
        self.tree.heading('return_date', text='Return Date')
        self.tree.heading('status', text='Status')
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('book_id', width=70, anchor='center')
        self.tree.column('reader_id', width=70, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="Refresh", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Create Loan", command=self.create_loan).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Return Selected", command=self.return_selected).pack(side=tk.LEFT, padx=5)

        # Filter frame
        filter_frame = ttk.LabelFrame(self, text="Filters")
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        self.filter_var = tk.StringVar(value="all")
        
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, value="all", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Active", variable=self.filter_var, value="active", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Overdue", variable=self.filter_var, value="overdue", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Returned", variable=self.filter_var, value="returned", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)

        # Form for creating loans
        form_frame = ttk.LabelFrame(self, text="Loan Form")
        form_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Book:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.book_combobox = ttk.Combobox(form_frame, state='readonly')
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="Reader:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.reader_combobox = ttk.Combobox(form_frame, state='readonly')
        self.reader_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="Days to return:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.days_entry = ttk.Spinbox(form_frame, from_=1, to=30, width=5)
        self.days_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.days_entry.set(14)

        btn_subframe = ttk.Frame(form_frame)
        btn_subframe.grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(btn_subframe, text="Create", command=self.save_loan).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_subframe, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        form_frame.columnconfigure(1, weight=1)
        self.load_combobox_data()

    def refresh_loans(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filter_type = self.filter_var.get()
        if filter_type == "all":
            loans = self.loan_controller.get_all_loans()
        elif filter_type == "active":
            loans = [loan for loan in self.loan_controller.get_all_loans() if not loan.is_returned]
        elif filter_type == "overdue":
            loans = self.loan_controller.get_overdue_loans()
        else:  # returned
            loans = [loan for loan in self.loan_controller.get_all_loans() if loan.is_returned]

        for loan in loans:
            status = "Returned" if loan.is_returned else "Overdue" if loan.is_overdue() else "Active"
            self.tree.insert('', tk.END, values=(
                loan.id,
                loan.book_id,
                loan.reader_id,
                loan.loan_date.strftime('%Y-%m-%d'),
                loan.return_date.strftime('%Y-%m-%d'),
                status
            ))

    def create_loan(self) -> None:
        self.clear_form()

    def return_selected(self) -> None:
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a loan first")
            return

        loan_id = int(self.tree.item(selected, 'values')[0])
        if messagebox.askyesno("Confirm", "Mark this loan as returned?"):
            try:
                self.loan_controller.return_book(loan_id)
                self.refresh_loans()
                messagebox.showinfo("Success", "Loan marked as returned")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def load_combobox_data(self) -> None:
        # Load books
        books = self.book_controller.get_all_books()
        book_options = [f"{book.id}: {book.title}" for book in books]
        self.book_combobox['values'] = book_options
        if book_options:
            self.book_combobox.current(0)

        # Load readers
        readers = self.reader_controller.get_all_readers()
        reader_options = [f"{reader.id}: {reader.name}" for reader in readers]
        self.reader_combobox['values'] = reader_options
        if reader_options:
            self.reader_combobox.current(0)

    def clear_form(self) -> None:
        if self.book_combobox['values']:
            self.book_combobox.current(0)
        if self.reader_combobox['values']:
            self.reader_combobox.current(0)
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, "14")

    def save_loan(self) -> None:
        book_str = self.book_combobox.get()
        reader_str = self.reader_combobox.get()
        days = self.days_entry.get()

        if not all([book_str, reader_str, days]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            book_id = int(book_str.split(':')[0])
            reader_id = int(reader_str.split(':')[0])
            days = int(days)

            loan_date = datetime.now()
            return_date = loan_date + timedelta(days=days)

            self.loan_controller.create_loan(book_id, reader_id, loan_date, return_date)
            messagebox.showinfo("Success", "Loan created successfully")
            self.refresh_loans()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create loan: {str(e)}")
