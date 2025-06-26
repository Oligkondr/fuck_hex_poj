import tkinter as tk
from tkinter import ttk, messagebox

class ReaderView(ttk.Frame):
    def __init__(self, parent, reader_controller) -> None:
        super().__init__(parent)
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_readers()

    def create_widgets(self) -> None:
        # Таблица с читателями
        columns = ("id", "name", "email", "phone")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150, anchor='center')
        self.tree.pack(expand=True, fill='both')

        # Кнопки управления
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', pady=5)

        ttk.Button(btn_frame, text="Add Reader", command=self.add_reader).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="View Loans", command=self.view_loans_selected).pack(side='left', padx=5)

    def refresh_readers(self) -> None:
        readers = self.reader_controller.get_all_readers()

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for reader in readers:
            self.tree.insert('', 'end', values=(
                reader.id,
                reader.name,
                reader.email,
                reader.phone
            ))

    def add_reader(self) -> None:
        def save():
            name = name_var.get().strip()
            email = email_var.get().strip()
            phone = phone_var.get().strip()

            if not name or not email or not phone:
                messagebox.showerror("Error", "All fields are required")
                return

            self.reader_controller.add_reader(name, email, phone)
            self.refresh_readers()
            add_win.destroy()

        add_win = tk.Toplevel(self)
        add_win.title("Add Reader")

        ttk.Label(add_win, text="Name:").pack(pady=2)
        name_var = tk.StringVar()
        ttk.Entry(add_win, textvariable=name_var).pack(pady=2)

        ttk.Label(add_win, text="Email:").pack(pady=2)
        email_var = tk.StringVar()
        ttk.Entry(add_win, textvariable=email_var).pack(pady=2)

        ttk.Label(add_win, text="Phone:").pack(pady=2)
        phone_var = tk.StringVar()
        ttk.Entry(add_win, textvariable=phone_var).pack(pady=2)

        ttk.Button(add_win, text="Save", command=save).pack(pady=10)

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No reader selected")
            return

        for sel in selected:
            reader_id = self.tree.item(sel)['values'][0]
            self.reader_controller.delete_reader(reader_id)
        self.refresh_readers()

    def view_loans_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No reader selected")
            return

        reader_id = self.tree.item(selected[0])['values'][0]
        loans = self.reader_controller.get_reader_loans(reader_id)

        loans_win = tk.Toplevel(self)
        loans_win.title(f"Loans for Reader ID {reader_id}")

        columns = ("loan_id", "book_title", "loan_date", "return_date", "status")
        tree = ttk.Treeview(loans_win, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").capitalize())
            tree.column(col, width=120, anchor='center')
        tree.pack(expand=True, fill='both')

        for loan in loans:
            tree.insert('', 'end', values=(
                loan.get('loan_id'),
                loan.get('book_title'),
                loan.get('loan_date'),
                loan.get('return_date'),
                loan.get('status'),
            ))
