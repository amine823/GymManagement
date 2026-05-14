import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import database as db
import csv


class AttendanceTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.selected_attendance_id = None
        self.member_map = {}
        self.setup_ui()
        self.load_members()
        self.load_data()
    
    def setup_ui(self):
        #header
        header_frame = ctk.CTkFrame(self.frame, fg_color="#34495e", corner_radius=15, height=100)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="📅 Attendance Management",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        #form
        form_card = ctk.CTkFrame(self.frame, corner_radius=15)
        form_card.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(form_card, text="Record Attendance", 
                    font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=4, pady=(20, 15), padx=20, sticky="w"
        )
        
        #member
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
        
        #check-in
        ctk.CTkLabel(form_card, text="Check-in Time * (YYYY-MM-DD HH:MM:SS)", 
                    font=ctk.CTkFont(size=13)).grid(
            row=2, column=0, sticky="w", padx=20, pady=10
        )
        self.checkin_var = ctk.StringVar(value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ctk.CTkEntry(form_card, textvariable=self.checkin_var, width=250, height=35).grid(
            row=2, column=1, padx=10, pady=10, sticky="w"
        )
        
        #check-out
        ctk.CTkLabel(form_card, text="Check-out Time (Optional)", 
                    font=ctk.CTkFont(size=13)).grid(
            row=2, column=2, sticky="w", padx=20, pady=10
        )
        self.checkout_var = ctk.StringVar()
        ctk.CTkEntry(form_card, textvariable=self.checkout_var, width=250, height=35).grid(
            row=2, column=3, padx=10, pady=10, sticky="w"
        )
        
        #set current time button
        ctk.CTkButton(
            form_card, text="⏰ Set Current Time",
            command=lambda: self.checkout_var.set(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            width=200, height=35, fg_color="#3498db", hover_color="#2980b9"
        ).grid(row=3, column=3, padx=10, pady=5, sticky="w")
        
        # buttons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=4, pady=20)
        
        ctk.CTkButton(
            btn_frame, text="➕ Record Attendance", command=self.add_attendance,
            width=160, height=40, fg_color="#0a582b", hover_color="#13783D",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🗑️ Delete", command=self.delete_attendance,
            width=140, height=40, fg_color="#771b11", hover_color="#983d33",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🔄 Clear", command=self.clear_form,
            width=140, height=40, fg_color="#2E4648", hover_color="#559ea3",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🔄 Refresh", command=self.load_data,
            width=140, height=40, fg_color="#18496a", hover_color="#3a81b0",
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
        
        ctk.CTkLabel(table_card, text="📋 Attendance Records", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(
            pady=(20, 10), padx=20, anchor="w"
        )
        
        tree_frame = ctk.CTkFrame(table_card)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scroll_y = ctk.CTkScrollbar(tree_frame, orientation="vertical")
        scroll_x = ctk.CTkScrollbar(tree_frame, orientation="horizontal")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Member", "Check-in Time", "Check-out Time"),
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
            ("ID", 80),
            ("Member", 250),
            ("Check-in Time", 200),
            ("Check-out Time", 200)
        ]
        
        for col, width in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=width)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#34495e", foreground="white",
                       borderwidth=0, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
    
    def load_members(self):
        members = db.get_members_for_dropdown()
        self.member_map = {f"{m[1]} (ID: {m[0]})": m[0] for m in members}
        self.member_combo.configure(values=list(self.member_map.keys()))
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = db.get_all_attendance()
        for record in records:
            display_record = list(record)
            if display_record[3] is None:
                display_record[3] = "🔴 Currently in gym"
            self.tree.insert("", "end", values=display_record)
    
    def validate_datetime(self, datetime_str):
        try:
            datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    
    def add_attendance(self):
        if not self.member_var.get():
            messagebox.showerror("Error", "Please select a member!")
            return
        
        if not self.validate_datetime(self.checkin_var.get()):
            messagebox.showerror("Error", "Invalid check-in time! Use YYYY-MM-DD HH:MM:SS")
            return
        
        checkout = self.checkout_var.get().strip()
        if checkout and not self.validate_datetime(checkout):
            messagebox.showerror("Error", "Invalid check-out time!")
            return
        
        member_id = self.member_map[self.member_var.get()]
        
        success = db.add_attendance(
            member_id,
            self.checkin_var.get(),
            checkout if checkout else None
        )
        
        if success:
            messagebox.showinfo("Success", "Attendance recorded!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to record.")
    
    def delete_attendance(self):
        if not self.selected_attendance_id:
            messagebox.showwarning("Warning", "Select a record!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this record?"):
            success = db.delete_attendance(self.selected_attendance_id)
            if success:
                messagebox.showinfo("Success", "Deleted!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed.")
    
    def clear_form(self):
        self.member_var.set("")
        self.checkin_var.set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.checkout_var.set("")
        self.selected_attendance_id = None
        self.load_members()
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.selected_attendance_id = values[0]
    
    def sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    
    def export_to_csv(self):
        try:
            filename = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Member", "Check-in Time", "Check-out Time"])
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)['values'])
            
            messagebox.showinfo("Success", f"Attendance list exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
