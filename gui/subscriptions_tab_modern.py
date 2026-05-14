import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import database as db
import utils.validators as val
import csv


class SubscriptionsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.selected_subscription_id = None
        self.member_map = {}
        self.plan_map = {}
        self.setup_ui()
        self.load_dropdowns()
        self.load_data()
    
    def setup_ui(self):
        #header
        header_frame = ctk.CTkFrame(self.frame, fg_color="#27ae60", corner_radius=15, height=100)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="📋 Subscriptions Management",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        # form
        form_card = ctk.CTkFrame(self.frame, corner_radius=15)
        form_card.pack(fill="x", padx=20, pady=10)
        
        form_title = ctk.CTkLabel(
            form_card,
            text="Subscription Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.grid(row=0, column=0, columnspan=4, pady=(20, 15), padx=20, sticky="w")
        
        # member
        ctk.CTkLabel(form_card, text="Member *", font=ctk.CTkFont(size=13)).grid(
            row=1, column=0, sticky="w", padx=20, pady=10
        )
        self.member_var = ctk.StringVar()
        self.member_combo = ctk.CTkComboBox(
            form_card,
            variable=self.member_var,
            width=500,
            height=35,
            state="readonly"
        )
        self.member_combo.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="w")
        
        ctk.CTkLabel(form_card, text="Plan *", font=ctk.CTkFont(size=13)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        self.plan_var = ctk.StringVar()
        self.plan_combo = ctk.CTkComboBox(
            form_card,
            variable=self.plan_var,
            width=500,
            height=35,
            state="readonly"
        )
        self.plan_combo.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="w")
        self.plan_combo.configure(command=self.on_plan_selected)
        
        ctk.CTkLabel(form_card, text="Start Date * (YYYY-MM-DD)", font=ctk.CTkFont(size=13)).grid(
            row=3, column=0, sticky="w", padx=20, pady=10
        )
        self.start_date_var = ctk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ctk.CTkEntry(form_card, textvariable=self.start_date_var, width=200, height=35).grid(
            row=3, column=1, padx=10, pady=10, sticky="w"
        )
        
        ctk.CTkLabel(form_card, text="End Date * (YYYY-MM-DD)", font=ctk.CTkFont(size=13)).grid(
            row=3, column=2, sticky="w", padx=20, pady=10
        )
        self.end_date_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.end_date_var, width=200, height=35).grid(
            row=3, column=3, padx=10, pady=10, sticky="w"
        )
        
        ctk.CTkLabel(form_card, text="Payment Status *", font=ctk.CTkFont(size=13)).grid(
            row=4, column=0, sticky="w", padx=20, pady=10
        )
        self.payment_status_var = ctk.StringVar(value="Paid")
        status_combo = ctk.CTkComboBox(
            form_card,
            values=["Paid", "Pending", "Overdue"],
            variable=self.payment_status_var,
            width=200,
            height=35,
            state="readonly"
        )
        status_combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        #buttons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=4, pady=20)
        
        ctk.CTkButton(
            btn_frame, text="➕ Add Subscription", command=self.add_subscription,
            width=150, height=40, fg_color="#0a582b", hover_color="#13783D",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="✏️ Update", command=self.update_subscription,
            width=140, height=40, fg_color="#546f1a", hover_color="#7da032",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🗑️ Delete", command=self.delete_subscription,
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
        
        # treeView
        table_card = ctk.CTkFrame(self.frame, corner_radius=15)
        table_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        table_title = ctk.CTkLabel(
            table_card,
            text="📋 Subscriptions List",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        table_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        tree_frame = ctk.CTkFrame(table_card)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scroll_y = ctk.CTkScrollbar(tree_frame, orientation="vertical")
        scroll_x = ctk.CTkScrollbar(tree_frame, orientation="horizontal")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Member", "Plan", "Start Date", "End Date", "Payment Status"),
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
        
        columns_config = [
            ("ID", 60),
            ("Member", 200),
            ("Plan", 200),
            ("Start Date", 120),
            ("End Date", 120),
            ("Payment Status", 120)
        ]
        
        for col, width in columns_config:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=width)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#27ae60", foreground="white",
                       borderwidth=0, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
    
    def load_dropdowns(self):
        members = db.get_members_for_dropdown()
        self.member_map = {f"{m[1]} (ID: {m[0]})": m[0] for m in members}
        self.member_combo.configure(values=list(self.member_map.keys()))
        
        plans = db.get_plans_for_dropdown()
        self.plan_map = {f"{p[1]} (ID: {p[0]})": p[0] for p in plans}
        self.plan_combo.configure(values=list(self.plan_map.keys()))
    
    def on_plan_selected(self, choice):
        if not choice or not self.start_date_var.get():
            return
        
        try:
            plan_id = self.plan_map[choice]
            plans = db.get_all_plans()
            
            for plan in plans:
                if plan[0] == plan_id:
                    duration_months = plan[2]
                    start_date = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d')
                    end_date = start_date + timedelta(days=duration_months * 30)
                    self.end_date_var.set(end_date.strftime('%Y-%m-%d'))
                    break
        except:
            pass
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        subscriptions = db.get_all_subscriptions()
        for sub in subscriptions:
            self.tree.insert("", "end", values=sub)
    
    def validate_form(self):
        if not self.member_var.get():
            messagebox.showerror("Validation Error", "Please select a member!")
            return False
        
        if not self.plan_var.get():
            messagebox.showerror("Validation Error", "Please select a plan!")
            return False
        
        if not val.validate_date(self.start_date_var.get()):
            messagebox.showerror("Validation Error", "Invalid start date! Use YYYY-MM-DD")
            return False
        
        if not val.validate_date(self.end_date_var.get()):
            messagebox.showerror("Validation Error", "Invalid end date! Use YYYY-MM-DD")
            return False
        
        try:
            start = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d')
            end = datetime.strptime(self.end_date_var.get(), '%Y-%m-%d')
            if end <= start:
                messagebox.showerror("Validation Error", "End date must be after start date!")
                return False
        except:
            messagebox.showerror("Validation Error", "Invalid date format!")
            return False
        
        return True
    
    def add_subscription(self):
        if not self.validate_form():
            return
        
        member_id = self.member_map[self.member_var.get()]
        plan_id = self.plan_map[self.plan_var.get()]
        
        success = db.add_subscription(
            member_id, plan_id,
            self.start_date_var.get(),
            self.end_date_var.get(),
            self.payment_status_var.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Subscription added successfully!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to add subscription.")
    
    def update_subscription(self):
        if not self.selected_subscription_id:
            messagebox.showwarning("Warning", "Please select a subscription!")
            return
        
        if not self.validate_form():
            return
        
        member_id = self.member_map[self.member_var.get()]
        plan_id = self.plan_map[self.plan_var.get()]
        
        success = db.update_subscription(
            self.selected_subscription_id,
            member_id, plan_id,
            self.start_date_var.get(),
            self.end_date_var.get(),
            self.payment_status_var.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Subscription updated!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to update.")
    
    def delete_subscription(self):
        if not self.selected_subscription_id:
            messagebox.showwarning("Warning", "Please select a subscription!")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                      "Delete this subscription?")
        if confirm:
            success = db.delete_subscription(self.selected_subscription_id)
            if success:
                messagebox.showinfo("Success", "Deleted successfully!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to delete.")
    
    def clear_form(self):
        self.member_var.set("")
        self.plan_var.set("")
        self.start_date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.end_date_var.set("")
        self.payment_status_var.set("Paid")
        self.selected_subscription_id = None
        self.load_dropdowns()
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.selected_subscription_id = values[0]
            messagebox.showinfo("Selection", 
                              f"Subscription #{values[0]} selected.\n"
                              "Re-select member and plan from dropdowns to update.")
    
    def sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    
    def export_to_csv(self):
        try:
            filename = f"subscriptions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Member", "Plan", "Start Date", "End Date", "Payment Status"])
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    writer.writerow(values)
            
            messagebox.showinfo("Success", f"Subscriptions list exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
