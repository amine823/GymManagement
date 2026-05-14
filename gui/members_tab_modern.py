
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import database as db
import utils.validators as val
import csv


class MembersTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.selected_member_id = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the members tab UI"""
        # Header
        header_frame = ctk.CTkFrame(self.frame, fg_color="#1f538d", corner_radius=15, height=100)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="👥 Members Management",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        # Search Section
        search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Search:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search by name, email, or phone...",
            width=400,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        search_entry.pack(side="left", padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_members())
        
        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.clear_search,
            width=100,
            height=40,
            fg_color="#a31c0d",
            hover_color="#ac3123"
        )
        clear_btn.pack(side="left", padx=5)
        
        # Form Section
        form_card = ctk.CTkFrame(self.frame, corner_radius=15)
        form_card.pack(fill="x", padx=20, pady=10)
        
        form_title = ctk.CTkLabel(
            form_card,
            text="Member Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.grid(row=0, column=0, columnspan=4, pady=(20, 15), padx=20, sticky="w")
        
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
        ctk.CTkLabel(form_card, text="Email *", font=ctk.CTkFont(size=13)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        self.email_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.email_var, width=250, height=35).grid(
            row=2, column=1, padx=10, pady=10
        )
        
        ctk.CTkLabel(form_card, text="Phone", font=ctk.CTkFont(size=13)).grid(
            row=2, column=2, sticky="w", padx=20, pady=10
        )
        self.phone_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.phone_var, width=250, height=35).grid(
            row=2, column=3, padx=10, pady=10
        )
        
        # Row 3
        ctk.CTkLabel(form_card, text="Date of Birth * (YYYY-MM-DD)", font=ctk.CTkFont(size=13)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.dob_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.dob_var, width=250, height=35).grid(
            row=3, column=1, padx=10, pady=10
        )
        
        ctk.CTkLabel(form_card, text="Gender *", font=ctk.CTkFont(size=13)).grid(
            row=3, column=2, sticky="w", padx=20, pady=10
        )
        self.gender_var = ctk.StringVar(value="M")
        gender_combo = ctk.CTkComboBox(
            form_card,
            values=["M", "F", "Other"],
            variable=self.gender_var,
            width=250,
            height=35,
            state="readonly"
        )
        gender_combo.grid(row=3, column=3, padx=10, pady=10)
        
        # Row 4
        ctk.CTkLabel(form_card, text="Status *", font=ctk.CTkFont(size=13)).grid(
            row=4, column=0, sticky="w", padx=20, pady=10
        )
        self.status_var = ctk.StringVar(value="Active")
        status_combo = ctk.CTkComboBox(
            form_card,
            values=["Active", "Inactive", "Suspended"],
            variable=self.status_var,
            width=250,
            height=35,
            state="readonly"
        )
        status_combo.grid(row=4, column=1, padx=10, pady=10)
        
        # Action Buttons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=4, pady=20)
        
        ctk.CTkButton(
            btn_frame, text="➕ Add Member", command=self.add_member,
            width=140, height=40, fg_color="#0a582b", hover_color="#13783D",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="✏️ Update", command=self.update_member,
            width=140, height=40, fg_color="#546f1a", hover_color="#7da032",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🗑️ Delete", command=self.delete_member,
            width=140, height=40, fg_color="#771b11", hover_color="#983d33",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🔄 Clear Form", command=self.clear_form,
            width=140, height=40, fg_color="#2E4648", hover_color="#559ea3",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="📊 Export CSV", command=self.export_to_csv,
            width=140, height=40, fg_color="#59266d", hover_color="#8e44ad",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        # TreeView Section
        table_card = ctk.CTkFrame(self.frame, corner_radius=15)
        table_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        table_title = ctk.CTkLabel(
            table_card,
            text="📋 Members List",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        table_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        # TreeView with scrollbars
        tree_frame = ctk.CTkFrame(table_card)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollbars
        scroll_y = ctk.CTkScrollbar(tree_frame, orientation="vertical")
        scroll_x = ctk.CTkScrollbar(tree_frame, orientation="horizontal")
        
        # TreeView
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "First Name", "Last Name", "Email", "Phone", "DOB", "Gender", "Join Date", "Status"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        
        scroll_y.configure(command=self.tree.yview)
        scroll_x.configure(command=self.tree.xview)
        
        # Pack scrollbars and tree
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)
        
        # Configure columns
        columns_config = [
            ("ID", 60),
            ("First Name", 120),
            ("Last Name", 120),
            ("Email", 200),
            ("Phone", 100),
            ("DOB", 100),
            ("Gender", 80),
            ("Join Date", 100),
            ("Status", 100)
        ]
        
        for col, width in columns_config:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=width, anchor="center")
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", 
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#1f538d", foreground="white",
                       borderwidth=0, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
    
    def load_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and display members
        members = db.get_all_members()
        for member in members:
            self.tree.insert("", "end", values=member)
    
    def search_members(self):
        search_term = self.search_var.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            members = db.search_members(search_term)
        else:
            members = db.get_all_members()
        
        for member in members:
            self.tree.insert("", "end", values=member)
    
    def clear_search(self):
        self.search_var.set("")
        self.load_data()
    
    def validate_form(self):
        if not val.validate_not_empty(self.first_name_var.get()):
            messagebox.showerror("Validation Error", "First name is required!")
            return False
        
        if not val.validate_text_only_letters(self.first_name_var.get()):
            messagebox.showerror("Validation Error", "First name must contain only letters and spaces!")
            return False

        if not val.validate_not_empty(self.last_name_var.get()):
            messagebox.showerror("Validation Error", "Last name is required!")
            return False
        
        if not val.validate_text_only_letters(self.last_name_var.get()):
            messagebox.showerror("Validation Error", "First name must contain only letters and spaces!")
            return False

        if not val.validate_email(self.email_var.get()):
            messagebox.showerror("Validation Error", "Invalid email format!")
            return False
        
        phone = self.phone_var.get().strip()
        if phone and not val.validate_phone(phone):
            messagebox.showerror("Validation Error", "Invalid phone number! Use 8 digits starting with 2, 5, or 9")
            return False
        
        if not val.validate_date(self.dob_var.get()):
            messagebox.showerror("Validation Error", "Invalid date format! Use YYYY-MM-DD")
            return False
        
        if not self.gender_var.get():
            messagebox.showerror("Validation Error", "Please select gender!")
            return False
        
        return True
    
    def add_member(self):
        if not self.validate_form():
            return
        
        success = db.add_member(
            self.first_name_var.get().strip(),
            self.last_name_var.get().strip(),
            self.email_var.get().strip(),
            self.phone_var.get().strip(),
            self.dob_var.get().strip(),
            self.gender_var.get(),
            self.status_var.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Member added successfully!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to add member. Email might already exist.")
    
    def update_member(self):
        if not self.selected_member_id:
            messagebox.showwarning("Warning", "Please select a member to update!")
            return
        
        if not self.validate_form():
            return
        
        success = db.update_member(
            self.selected_member_id,
            self.first_name_var.get().strip(),
            self.last_name_var.get().strip(),
            self.email_var.get().strip(),
            self.phone_var.get().strip(),
            self.dob_var.get().strip(),
            self.gender_var.get(),
            self.status_var.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Member updated successfully!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to update member.")
    
    def delete_member(self):
        if not self.selected_member_id:
            messagebox.showwarning("Warning", "Please select a member to delete!")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this member?\n\n"
            "This will also delete all associated subscriptions and attendance records."
        )
        
        if confirm:
            success = db.delete_member(self.selected_member_id)
            if success:
                messagebox.showinfo("Success", "Member deleted successfully!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to delete member.")
    
    def clear_form(self):
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.dob_var.set("")
        self.gender_var.set("M")
        self.status_var.set("Active")
        self.selected_member_id = None
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_member_id = values[0]
            self.first_name_var.set(values[1])
            self.last_name_var.set(values[2])
            self.email_var.set(values[3])
            self.phone_var.set(values[4])
            self.dob_var.set(values[5])
            self.gender_var.set(values[6])
            self.status_var.set(values[8])
    
    def sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    
    def export_to_csv(self):
        try:
            filename = f"members_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "First Name", "Last Name", "Email", "Phone",
                               "Date of Birth", "Gender", "Join Date", "Status"])
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    writer.writerow(values)
            
            messagebox.showinfo("Success", f"Members list exported successfully to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
