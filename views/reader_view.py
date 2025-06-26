# Здесь должно быть представление для работы с читателями согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import Optional

class ReaderView(ttk.Frame):
    def __init__(self, parent, reader_controller) -> None:
        super().__init__(parent)
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_readers()

    def create_widgets(self) -> None:
        # Main container
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview for readers
        self.tree = ttk.Treeview(self, columns=('id', 'name', 'email', 'phone'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('email', text='Email')
        self.tree.heading('phone', text='Phone')
        self.tree.column('id', width=50, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="Refresh", command=self.refresh_readers).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Reader", command=self.add_reader).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)

        # Form for adding/editing readers
        form_frame = ttk.LabelFrame(self, text="Reader Form")
        form_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.phone_entry = ttk.Entry(form_frame)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')

        btn_subframe = ttk.Frame(form_frame)
        btn_subframe.grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(btn_subframe, text="Save", command=self.save_reader).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_subframe, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        form_frame.columnconfigure(1, weight=1)
        self.current_reader_id: Optional[int] = None

    def refresh_readers(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        readers = self.reader_controller.get_all_readers()
        for reader in readers:
            self.tree.insert('', tk.END, values=(
                reader.id,
                reader.name,
                reader.email,
                reader.phone
            ))

    def add_reader(self) -> None:
        self.current_reader_id = None
        self.clear_form()

    def delete_selected(self) -> None:
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reader first")
            return

        reader_id = int(self.tree.item(selected, 'values')[0])
        if messagebox.askyesno("Confirm", "Delete this reader?"):
            try:
                self.reader_controller.delete_reader(reader_id)
                self.refresh_readers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete reader: {str(e)}")

    def clear_form(self) -> None:
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.current_reader_id = None

    def save_reader(self) -> None:
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        if not all([name, email, phone]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            if self.current_reader_id:
                self.reader_controller.update_reader(
                    self.current_reader_id,
                    name=name,
                    email=email,
                    phone=phone
                )
                messagebox.showinfo("Success", "Reader updated successfully")
            else:
                self.reader_controller.add_reader(name, email, phone)
                messagebox.showinfo("Success", "Reader added successfully")

            self.refresh_readers()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save reader: {str(e)}")


