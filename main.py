import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db

# Import all tab modules
from gui.dashboard_tab_modern import DashboardTab
from gui.members_tab_modern import MembersTab
from gui.plans_tab_modern import PlansTab
from gui.subscriptions_tab_modern import SubscriptionsTab
from gui.trainers_tab_modern import TrainersTab
from gui.attendance_tab_modern import AttendanceTab

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ModernGymApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("💪 Gym Management System")
        self.geometry("1400x900")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Test database connection
        if not self.test_database():
            return
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Initialize tabs dictionary
        self.tabs = {}
        self.current_tab = None
        
        # Show dashboard by default
        self.show_dashboard()
        
        # Center window
        self.center_window()
    
    def test_database(self):
        conn = db.Database.get_connection()
        if conn is None:
            messagebox.showerror(
                "Database Error",
                "❌ Cannot connect to database!\n\n"
                "Please check:\n"
                "• MySQL server is running\n"
                "• Database 'gym_management' exists\n"
                "• Credentials in config.py are correct"
            )
            self.destroy()
            return False
        conn.close()
        return True
    
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(9, weight=1)
        
        # Logo/Title
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="#8e44ad", corner_radius=10)
        logo_frame.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="ew")
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="💪 GYM\nMANAGER",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        logo_label.pack(pady=15)
        
        #navigation buttons
        self.nav_buttons = {}
            
        nav_items = [
            ("📊 Dashboard", self.show_dashboard, "#8e44ad"),
            ("👥 Members", self.show_members, "#1f538d"),
            ("📋 Subscriptions", self.show_subscriptions, "#27ae60"),
            ("💳 Plans", self.show_plans, "#16a085"),
            ("🏋️ Trainers", self.show_trainers, "#e67e22"),
            ("📅 Attendance", self.show_attendance, "#7cabe1"),
        ]
        
        for idx, (text, command, color) in enumerate(nav_items, start=2):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                font=ctk.CTkFont(size=15, weight="bold"),
                height=50,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=color,
                anchor="w",
                corner_radius=10
            )
            btn.grid(row=idx, column=0, padx=15, pady=5, sticky="ew")
            self.nav_buttons[text] = btn
        
        #separator
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="gray30")
        separator.grid(row=8, column=0, padx=20, pady=20, sticky="ew")
        
        #theme switcher
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.grid(row=10, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        ctk.CTkLabel(
            theme_frame,
            text="🎨 Appearance:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.theme_var = ctk.StringVar(value="Dark")
        theme_menu = ctk.CTkSegmentedButton(
            theme_frame,
            values=["Light", "Dark", "System"],
            command=self.change_theme,
            variable=self.theme_var,
            font=ctk.CTkFont(size=11)
        )
        theme_menu.pack(fill="x")
        
        #footer info
        footer_label = ctk.CTkLabel(
            self.sidebar,
            text="© 2026 Gym Manager\nAll rights reserved",
            font=ctk.CTkFont(size=9),
            text_color="gray50"
        )
        footer_label.grid(row=11, column=0, padx=20, pady=(0, 20))
    
    def create_main_content(self):
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)
    
    def hide_all_tabs(self):
        for tab_name, tab_obj in self.tabs.items():
            tab_obj.frame.pack_forget()
    
    def highlight_nav_button(self, active_text):
        colors = {
            "📊 Dashboard": "#8e44ad",
            "👥 Members": "#1f538d",
            "📋 Subscriptions": "#27ae60",
            "💳 Plans": "#16a085",
            "🏋️ Trainers": "#e67e22",
            "📅 Attendance": "#34495e"
        }
        
        for text, btn in self.nav_buttons.items():
            if text == active_text:
                btn.configure(fg_color=colors.get(text, "gray25"))
            else:
                btn.configure(fg_color="transparent")
    
    def change__treeview_header_color(self, value):
        #style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", 
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#1f538d", foreground="white",
                       borderwidth=0, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])        
    
    def show_dashboard(self):
        self.hide_all_tabs()
        self.highlight_nav_button("📊 Dashboard")
        
        #create tab if it doesn't exist
        if "dashboard" not in self.tabs:
            self.tabs["dashboard"] = DashboardTab(self.main_content)
        
        #show the tab
        self.tabs["dashboard"].frame.pack(fill="both", expand=True)
        self.tabs["dashboard"].load_statistics()
        self.current_tab = "dashboard"
    
    def show_members(self):
        self.hide_all_tabs()
        self.highlight_nav_button("👥 Members")
        
        #create tab if it doesn't exist
        if "members" not in self.tabs:
            self.tabs["members"] = MembersTab(self.main_content)
        
        #show the tab
        self.tabs["members"].frame.pack(fill="both", expand=True)
        self.tabs["members"].load_data()
        self.current_tab = "members"
    
    def show_subscriptions(self):
        """Show subscriptions"""
        self.hide_all_tabs()
        self.highlight_nav_button("📋 Subscriptions")
        
        #create tab if it doesn't exist
        if "subscriptions" not in self.tabs:
            self.tabs["subscriptions"] = SubscriptionsTab(self.main_content)
        
        #show the tab
        self.tabs["subscriptions"].frame.pack(fill="both", expand=True)
        self.tabs["subscriptions"].load_data()
        self.current_tab = "subscriptions"
    
    def show_plans(self):
        self.hide_all_tabs()
        self.highlight_nav_button("💳 Plans")
        
        #create tab if it doesn't exist
        if "plans" not in self.tabs:
            self.tabs["plans"] = PlansTab(self.main_content)
        
        #show the tab
        self.tabs["plans"].frame.pack(fill="both", expand=True)
        self.tabs["plans"].load_data()
        self.current_tab = "plans"
    
    def show_trainers(self):
        self.hide_all_tabs()
        self.highlight_nav_button("🏋️ Trainers")
        
        #create tab if it doesn't exist
        if "trainers" not in self.tabs:
            self.tabs["trainers"] = TrainersTab(self.main_content)
        
        #show the tab
        self.tabs["trainers"].frame.pack(fill="both", expand=True)
        self.tabs["trainers"].load_data()
        self.current_tab = "trainers"
    
    def show_attendance(self):
        self.hide_all_tabs()
        self.highlight_nav_button("📅 Attendance")
        
        #create tab if it doesn't exist
        if "attendance" not in self.tabs:
            self.tabs["attendance"] = AttendanceTab(self.main_content)
        
        #show the tab
        self.tabs["attendance"].frame.pack(fill="both", expand=True)
        self.tabs["attendance"].load_data()
        self.current_tab = "attendance"
    
    def change_theme(self, value):
        ctk.set_appearance_mode(value.lower())
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


def main():
    app = ModernGymApp()
    app.mainloop()

if __name__ == "__main__":
    main()
