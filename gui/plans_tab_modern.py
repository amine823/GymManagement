import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import database as db
import utils.validators as val
import csv


class PlansTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.selected_plan_id = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        #header
        header_frame = ctk.CTkFrame(self.frame, fg_color="#16a085", corner_radius=15, height=100)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="💳 Subscription Plans Management",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        # formsection
        form_card = ctk.CTkFrame(self.frame, corner_radius=15)
        form_card.pack(fill="x", padx=20, pady=10)
        
        form_title = ctk.CTkLabel(
            form_card,
            text="Plan Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.grid(row=0, column=0, columnspan=4, pady=(20, 15), padx=20, sticky="w")
        
        ctk.CTkLabel(form_card, text="Plan Name *", font=ctk.CTkFont(size=13)).grid(
            row=1, column=0, sticky="w", padx=20, pady=10
        )
        self.plan_name_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.plan_name_var, width=500, height=35).grid(
            row=1, column=1, columnspan=3, padx=10, pady=10, sticky="w"
        )
        
        ctk.CTkLabel(form_card, text="Duration (Months) *", font=ctk.CTkFont(size=13)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        self.duration_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.duration_var, width=200, height=35).grid(
            row=2, column=1, padx=10, pady=10, sticky="w"
        )
        
        ctk.CTkLabel(form_card, text="Price (TND) *", font=ctk.CTkFont(size=13)).grid(
            row=2, column=2, sticky="w", padx=20, pady=10
        )
        self.price_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.price_var, width=200, height=35).grid(
            row=2, column=3, padx=10, pady=10, sticky="w"
        )
        
        # description
        ctk.CTkLabel(form_card, text="Description", font=ctk.CTkFont(size=13)).grid(
            row=3, column=0, sticky="nw", padx=20, pady=10
        )
        self.description_text = ctk.CTkTextbox(form_card, height=80, width=500)
        self.description_text.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky="w")
        
        # buttons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=4, pady=20)
        
        ctk.CTkButton(
            btn_frame, text="➕ Add Plan", command=self.add_plan,
            width=140, height=40, fg_color="#0a582b", hover_color="#13783D",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="✏️ Update", command=self.update_plan,
            width=140, height=40, fg_color="#546f1a", hover_color="#7da032",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🗑️ Delete", command=self.delete_plan,
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
        
        # treeView Section
        table_card = ctk.CTkFrame(self.frame, corner_radius=15)
        table_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        table_title = ctk.CTkLabel(
            table_card,
            text="📋 Plans List",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        table_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        #treeView with scrollbars
        tree_frame = ctk.CTkFrame(table_card)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scroll_y = ctk.CTkScrollbar(tree_frame, orientation="vertical")
        scroll_x = ctk.CTkScrollbar(tree_frame, orientation="horizontal")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Plan Name", "Duration (Months)", "Price (TND)", "Description"),
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
        
        # Configure columns
        columns_config = [
            ("ID", 60),
            ("Plan Name", 250),
            ("Duration (Months)", 150),
            ("Price (TND)", 120),
            ("Description", 400)
        ]
        
        for col, width in columns_config:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=width)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#16a085", foreground="white",
                       borderwidth=0, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        plans = db.get_all_plans()
        for plan in plans:
            self.tree.insert("", "end", values=plan)
    
    def validate_form(self):
        if not val.validate_not_empty(self.plan_name_var.get()):
            messagebox.showerror("Validation Error", "Plan name is required!")
            return False
        
        if not val.validate_integer(self.duration_var.get(), min_val=1):
            messagebox.showerror("Validation Error", "Duration must be a positive integer!")
            return False
        
        if not val.validate_number(self.price_var.get(), min_val=0.01):
            messagebox.showerror("Validation Error", "Price must be a positive number!")
            return False
        
        return True
    
    def add_plan(self):
        if not self.validate_form():
            return
        
        description = self.description_text.get("1.0", "end").strip()
        
        success = db.add_plan(
            self.plan_name_var.get().strip(),
            int(self.duration_var.get()),
            float(self.price_var.get()),
            description
        )
        
        if success:
            messagebox.showinfo("Success", "Plan added successfully!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to add plan. Plan name might already exist.")
    
    def update_plan(self):
        if not self.selected_plan_id:
            messagebox.showwarning("Warning", "Please select a plan to update!")
            return
        
        if not self.validate_form():
            return
        
        description = self.description_text.get("1.0", "end").strip()
        
        success = db.update_plan(
            self.selected_plan_id,
            self.plan_name_var.get().strip(),
            int(self.duration_var.get()),
            float(self.price_var.get()),
            description
        )
        
        if success:
            messagebox.showinfo("Success", "Plan updated successfully!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to update plan.")
    
    def delete_plan(self):
        if not self.selected_plan_id:
            messagebox.showwarning("Warning", "Please select a plan to delete!")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "⚠️ Are you sure you want to delete this plan?\n"
            "This may affect existing subscriptions."
        )
        
        if confirm:
            success = db.delete_plan(self.selected_plan_id)
            if success:
                messagebox.showinfo("Success", "Plan deleted successfully!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to delete plan. It may be in use.")
    
    def clear_form(self):
        self.plan_name_var.set("")
        self.duration_var.set("")
        self.price_var.set("")
        self.description_text.delete("1.0", "end")
        self.selected_plan_id = None
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_plan_id = values[0]
            self.plan_name_var.set(values[1])
            self.duration_var.set(values[2])
            self.price_var.set(values[3])
            self.description_text.delete("1.0", "end")
            self.description_text.insert("1.0", values[4] if values[4] else "")
    
    def sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    
    def export_to_csv(self):
        try:
            filename = f"plans_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Plan Name", "Duration (Months)", "Price (TND)", "Description"])
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    writer.writerow(values)
            
            messagebox.showinfo("Success", f"Plans list exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
