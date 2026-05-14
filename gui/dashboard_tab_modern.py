import customtkinter as ctk
import database as db


class DashboardTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.setup_ui()
        self.load_statistics()
    
    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self.frame, fg_color="#8e44ad", corner_radius=15, height=100)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="📊 Dashboard & Statistics",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        # Statistics Cards Container
        self.stats_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=20)
        
        # Configure grid
        for i in range(5):
            self.stats_frame.grid_columnconfigure(i, weight=1)
        
        # Create stat card placeholders (will be filled in load_statistics)
        self.stat_cards = {}
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            self.frame,
            text="🔄 Refresh Statistics",
            command=self.load_statistics,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        refresh_btn.pack(pady=20)
        
        # Info section
        info_card = ctk.CTkFrame(self.frame, corner_radius=15)
        info_card.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        info_title = ctk.CTkLabel(
            info_card,
            text="💡 Quick Information",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        info_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        info_text = """
Welcome to Gym Management System !

✨ Features:
  • Complete member management with profiles
  • Subscription and payment tracking  
  • Trainer management and specializations
  • Real-time attendance monitoring
  • Beautiful modern interface with dark/light mode
  • CSV export for all data modules
  • Advanced search and filtering

✨✨ Quick Start:
  1. Use sidebar to navigate between modules
  2. Click on table rows to select and edit
  3. Use search bars for quick lookups
  4. Export data using CSV buttons

💡 Tips:
  • All changes save to database instantly
  • Click column headers to sort tables
  • Use theme switcher for preferred appearance
        """
        
        info_textbox = ctk.CTkTextbox(
            info_card,
            font=ctk.CTkFont(size=13),
            wrap="word",
            height=350
        )
        info_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        info_textbox.insert("1.0", info_text)
        info_textbox.configure(state="disabled")
    
    def create_stat_card(self, parent, icon, label, value, color, column):
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=15, height=150)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=45)
        )
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="white"
        )
        value_label.pack(pady=5)
        
        # Label
        label_label = ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        label_label.pack(pady=(5, 15))
        
        return value_label
    
    def load_statistics(self):
        # Clear existing cards
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Get statistics from database
        stats = db.get_statistics()
        
        # Create stat cards
        stat_data = [
            ("👥", "Total Members", stats['total_members'], "#072b43"),
            ("✅", "Active Members", stats['active_members'], "#1a4c6e"),
            ("🏋️", "Active Trainers", stats['active_trainers'], "#30678b"),
            ("💰", "Revenue (TND)", f"{stats['total_revenue']:.2f}", "#4f84a8"),
            ("📅", "Today's Visits", stats['today_attendance'], "#74a6c7"),
        ]
        
        for idx, (icon, label, value, color) in enumerate(stat_data):
            self.create_stat_card(self.stats_frame, icon, label, value, color, idx)
