
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import database as db
import utils.validators as val
import csv


class TrainersTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.selected_trainer_id = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        #header
        header_frame = ctk.CTkFrame(self.frame, fg_color="#e67e22", corner_radius=15, height=100)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="🏋️ Trainers Management",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        #search
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="🔍 Search:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(0, 10))
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search by name or specialization...",
            width=400,
            height=40
        )
        search_entry.pack(side="left", padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_trainers())
        
        ctk.CTkButton(
            search_frame, text="Clear", command=self.clear_search,
            width=100, height=40, fg_color="#e74c3c", hover_color="#c0392b"
        ).pack(side="left", padx=5)
        
        # form
        form_card = ctk.CTkFrame(self.frame, corner_radius=15)
        form_card.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(form_card, text="Trainer Information", 
                    font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=4, pady=(20, 15), padx=20, sticky="w"
        )
        
        # Row 1
        ctk.CTkLabel(form_card, text="First Name *", font=ctk.CTkFont(size=13)).grid(
            row=1, column=0, sticky="w", padx=20, pady=10
        )
        self.first_name_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.first_name_var, width=250, height=35).grid(
            row=1, column=1, padx=10, pady=10
        )
        
        ctk.CTkLabel(form_card, text="Last Name *", font=ctk.CTkFont(size=13)).grid(
            row=1, column=2, sticky="w", padx=20, pady=10
        )
        self.last_name_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.last_name_var, width=250, height=35).grid(
            row=1, column=3, padx=10, pady=10
        )
        
        # Row 2
        ctk.CTkLabel(form_card, text="Specialization *", font=ctk.CTkFont(size=13)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        self.specialization_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.specialization_var, width=250, height=35).grid(
            row=2, column=1, padx=10, pady=10
        )
        
        ctk.CTkLabel(form_card, text="Email", font=ctk.CTkFont(size=13)).grid(
            row=2, column=2, sticky="w", padx=20, pady=10
        )
        self.email_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.email_var, width=250, height=35).grid(
            row=2, column=3, padx=10, pady=10
        )
        
        # Row 3
        ctk.CTkLabel(form_card, text="Phone", font=ctk.CTkFont(size=13)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.phone_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.phone_var, width=250, height=35).grid(
            row=3, column=1, padx=10, pady=10
        )
        
        ctk.CTkLabel(form_card, text="Status *", font=ctk.CTkFont(size=13)).grid(
            row=3, column=2, sticky="w", padx=20, pady=10
        )
        self.status_var = ctk.StringVar(value="Active")
        ctk.CTkComboBox(
            form_card, values=["Active", "Inactive"],
            variable=self.status_var, width=250, height=35, state="readonly"
        ).grid(row=3, column=3, padx=10, pady=10)
        
        #buttons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=4, pady=20)
        
        ctk.CTkButton(
            btn_frame, text="➕ Add Trainer", command=self.add_trainer,
            width=140, height=40, fg_color="#0a582b", hover_color="#13783D",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="✏️ Update", command=self.update_trainer,
            width=140, height=40, fg_color="#546f1a", hover_color="#7da032",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🗑️ Delete", command=self.delete_trainer,
            width=140, height=40, fg_color="#771b11", hover_color="#983d33",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🔄 Clear", command=self.clear_form,
            width=140, height=40, fg_color="#2E4648", hover_color="#559ea3",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="📊 Export", command=self.export_to_csv,
            width=140, height=40, fg_color="#59266d", hover_color="#8e44ad",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        # treeView
        table_card = ctk.CTkFrame(self.frame, corner_radius=15)
        table_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        ctk.CTkLabel(table_card, text="📋 Trainers List", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(
            pady=(20, 10), padx=20, anchor="w"
        )
        
        tree_frame = ctk.CTkFrame(table_card)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scroll_y = ctk.CTkScrollbar(tree_frame, orientation="vertical")
        scroll_x = ctk.CTkScrollbar(tree_frame, orientation="horizontal")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "First Name", "Last Name", "Specialization", "Email", "Phone", "Hire Date", "Status"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        
        scroll_y.configure(command=self.tree.yview)
        scroll_x.configure(command=self.tree.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)
        
        columns = [
            ("ID", 60),("First Name" , 120),("Last Name",120),
            ("Specialization",200), ("Email",200),("Phone",100),
            ("Hire Date", 120),("Status",100)
        ]
        
        for col, width in columns:
            self.tree.heading(col, text=col, command=lambda c=col:self.sort_column(c, False))
            self.tree.column(col, width=width)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#e67e22", foreground="white",
                       borderwidth=0, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
    
    def load_data(self):
        """Load data"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        trainers = db.get_all_trainers()
        for trainer in trainers:
            self.tree.insert("", "end", values=trainer)
    
    def search_trainers(self):
        search_term = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            trainers = db.search_trainers(search_term)
        else:
            trainers = db.get_all_trainers()
        
        for trainer in trainers:
            self.tree.insert("", "end", values=trainer)
    
    def clear_search(self):
        self.search_var.set("")
        self.load_data()
    
    def validate_form(self):
        if not val.validate_not_empty(self.first_name_var.get()):
            messagebox.showerror("Error", "First name required!")
            return False
        
        if not val.validate_not_empty(self.last_name_var.get()):
            messagebox.showerror("Error", "Last name required!")
            return False
        
        if not val.validate_not_empty(self.specialization_var.get()):
            messagebox.showerror("Error", "Specialization required!")
            return False
        
        email = self.email_var.get().strip()
        if email and not val.validate_email(email):
            messagebox.showerror("Error", "Invalid email!")
            return False
        
        phone = self.phone_var.get().strip()
        if phone and not val.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone!")
            return False
        
        return True
    
    def add_trainer(self):
        if not self.validate_form():
            return
        
        success = db.add_trainer(
            self.first_name_var.get().strip(),
            self.last_name_var.get().strip(),
            self.specialization_var.get().strip(),
            self.email_var.get().strip(),
            self.phone_var.get().strip(),
            self.status_var.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Trainer added!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to add.")
    
    def update_trainer(self):
        if not self.selected_trainer_id:
            messagebox.showwarning("Warning", "Select a trainer!")
            return
        
        if not self.validate_form():
            return
        
        success = db.update_trainer(
            self.selected_trainer_id,
            self.first_name_var.get().strip(),
            self.last_name_var.get().strip(),
            self.specialization_var.get().strip(),
            self.email_var.get().strip(),
            self.phone_var.get().strip(),
            self.status_var.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Updated!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed.")
    
    def delete_trainer(self):
        if not self.selected_trainer_id:
            messagebox.showwarning("Warning", "Select a trainer!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this trainer?"):
            success = db.delete_trainer(self.selected_trainer_id)
            if success:
                messagebox.showinfo("Success", "Deleted!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed.")
    
    def clear_form(self):
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.specialization_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.status_var.set("Active")
        self.selected_trainer_id = None
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_trainer_id = values[0]
            self.first_name_var.set(values[1])
            self.last_name_var.set(values[2])
            self.specialization_var.set(values[3])
            self.email_var.set(values[4])
            self.phone_var.set(values[5])
            self.status_var.set(values[7])
    
    def sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    
    def export_to_csv(self):
        try:
            filename = f"records/trainers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "First Name", "Last Name", "Specialization",
                               "Email", "Phone", "Hire Date", "Status"])
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)['values'])
            
            messagebox.showinfo("Success", f"Trainers list exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
