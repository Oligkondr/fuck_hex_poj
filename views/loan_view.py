import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class LoanView(ttk.Frame):
    def __init__(self, parent, loan_controller, book_controller, reader_controller) -> None:
        super().__init__(parent)
        self.loan_controller = loan_controller
        self.book_controller = book_controller
        self.reader_controller = reader_controller

        self.create_widgets()
        self.refresh_loans()

    def create_widgets(self) -> None:
        # Фильтр по статусу займов
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill='x', pady=5)

        ttk.Label(filter_frame, text="Filter:").pack(side='left', padx=5)

        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, value="all", command=self.refresh_loans).pack(side='left')
        ttk.Radiobutton(filter_frame, text="Active", variable=self.filter_var, value="active", command=self.refresh_loans).pack(side='left')
        ttk.Radiobutton(filter_frame, text="Overdue", variable=self.filter_var, value="overdue", command=self.refresh_loans).pack(side='left')

        # Таблица с займами
        columns = ("loan_id", "book_title", "reader_name", "loan_date", "return_date", "is_returned")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").capitalize())
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(expand=True, fill='both')

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', pady=5)

        ttk.Button(btn_frame, text="Create Loan", command=self.create_loan).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Return Selected", command=self.return_selected).pack(side='left', padx=5)

    def refresh_loans(self) -> None:
        filter_status = self.filter_var.get()
        if filter_status == "all":
            loans = self.loan_controller.get_all_loans()
        elif filter_status == "active":
            loans = [loan for loan in self.loan_controller.get_all_loans() if not getattr(loan, 'is_returned', False)]
        elif filter_status == "overdue":
            loans = self.loan_controller.get_overdue_loans()
        else:
            loans = []

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for loan in loans:
            book = self.book_controller.get_book(loan.book_id)
            reader = self.reader_controller.get_reader(loan.reader_id)
            self.tree.insert('', 'end', values=(
                loan.id,
                book.title if book else "Unknown",
                reader.name if reader else "Unknown",
                loan.loan_date.strftime("%Y-%m-%d") if loan.loan_date else "",
                loan.return_date.strftime("%Y-%m-%d") if loan.return_date else "",
                "Yes" if getattr(loan, 'is_returned', False) else "No"
            ))

    def create_loan(self) -> None:
        def save():
            try:
                book_id = int(book_var.get())
                reader_id = int(reader_var.get())
                loan_date = datetime.strptime(loan_date_var.get(), "%Y-%m-%d")
                return_date = datetime.strptime(return_date_var.get(), "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid data (dates format: YYYY-MM-DD)")
                return

            if return_date <= loan_date:
                messagebox.showerror("Error", "Return date must be after loan date")
                return

            loan_id = self.loan_controller.create_loan(book_id, reader_id, loan_date, return_date)
            if loan_id:
                messagebox.showinfo("Success", f"Loan created with ID {loan_id}")
                self.refresh_loans()
                create_win.destroy()
            else:
                messagebox.showerror("Error", "Failed to create loan")

        create_win = tk.Toplevel(self)
        create_win.title("Create Loan")

        ttk.Label(create_win, text="Book ID:").pack(pady=2)
        book_var = tk.StringVar()
        ttk.Entry(create_win, textvariable=book_var).pack(pady=2)

        ttk.Label(create_win, text="Reader ID:").pack(pady=2)
        reader_var = tk.StringVar()
        ttk.Entry(create_win, textvariable=reader_var).pack(pady=2)

        ttk.Label(create_win, text="Loan Date (YYYY-MM-DD):").pack(pady=2)
        loan_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(create_win, textvariable=loan_date_var).pack(pady=2)

        ttk.Label(create_win, text="Return Date (YYYY-MM-DD):").pack(pady=2)
        return_date_var = tk.StringVar(value=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
        ttk.Entry(create_win, textvariable=return_date_var).pack(pady=2)

        ttk.Button(create_win, text="Save", command=save).pack(pady=10)

    def return_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No loan selected")
            return

        for sel in selected:
            loan_id = self.tree.item(sel)['values'][0]
            success = self.loan_controller.return_book(loan_id)
            if not success:
                messagebox.showerror("Error", f"Cannot return loan ID {loan_id}")
        self.refresh_loans()
