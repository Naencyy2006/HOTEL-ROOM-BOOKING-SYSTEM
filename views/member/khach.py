import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class HotelBookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -------------------------------------------------------------
        # 1. CẤU HÌNH CỬA SỔ DESKTOP & CĂN GIỮA
        # -------------------------------------------------------------
        self.title("Hotel Booking System - UTH")
        
        window_width = 1100
        window_height = 680

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(950, 600)

        # -------------------------------------------------------------
        # 2. TOP HEADER (HOTEL BOOKING SYSTEM | LOGIN | REGISTER)
        # -------------------------------------------------------------
        self.top_header = ctk.CTkFrame(self, height=55, corner_radius=0, fg_color="#1f538d")
        self.top_header.pack(fill="x", side="top")

        self.lbl_system_title = ctk.CTkLabel(
            self.top_header,
            text="Hotel Booking System",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.lbl_system_title.pack(side="left", padx=30, pady=10)

        # Khung Đăng nhập | Đăng ký bên phải
        self.auth_box = ctk.CTkFrame(self.top_header, fg_color="transparent")
        self.auth_box.pack(side="right", padx=30)

        self.btn_top_login = ctk.CTkButton(
            self.auth_box, text="Login", width=75, height=32, fg_color="transparent",
            hover_color="#14375e", font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_login_click
        )
        self.btn_top_login.pack(side="left")

        self.lbl_divider = ctk.CTkLabel(self.auth_box, text="|", text_color="white", font=ctk.CTkFont(size=16))
        self.lbl_divider.pack(side="left", padx=5)

        self.btn_top_register = ctk.CTkButton(
            self.auth_box, text="Register", width=75, height=32, fg_color="transparent",
            hover_color="#14375e", font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_register_click
        )
        self.btn_top_register.pack(side="left")

        # -------------------------------------------------------------
        # 3. KHOANG NỘI DUNG CHÍNH (MAIN CONTENT - FULL WIDTH)
        # -------------------------------------------------------------
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=20)

        # TIÊU ĐỀ CHÍNH
        self.hero_title = ctk.CTkLabel(
            self.main_content,
            text="FIND YOUR PERFECT ROOM",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.hero_title.pack(pady=(10, 25))

        # KHUNG TÌM KIẾM (SEARCH ROOMS BOX)
        self.search_card = ctk.CTkFrame(self.main_content, corner_radius=12, border_width=1, border_color="#cccccc")
        self.search_card.pack(fill="x", pady=(0, 30))

        # Hàng chứa các ô nhập dữ liệu: Check-in | Check-out | Guests | Min Price | Max Price
        self.inputs_row = ctk.CTkFrame(self.search_card, fg_color="transparent")
        self.inputs_row.pack(fill="x", padx=20, pady=(25, 15))
        
        # Cấu hình 5 cột cân bằng cho 5 ô nhập liệu
        for col in range(5):
            self.inputs_row.grid_columnconfigure(col, weight=1)

        # 1. Check-in
        self.lbl_checkin = ctk.CTkLabel(self.inputs_row, text="Check-in", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_checkin.grid(row=0, column=0, sticky="w", padx=8)
        self.entry_checkin = ctk.CTkEntry(self.inputs_row, placeholder_text="YYYY-MM-DD", height=40)
        self.entry_checkin.grid(row=1, column=0, sticky="ew", padx=8, pady=(5, 0))

        # 2. Check-out
        self.lbl_checkout = ctk.CTkLabel(self.inputs_row, text="Check-out", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_checkout.grid(row=0, column=1, sticky="w", padx=8)
        self.entry_checkout = ctk.CTkEntry(self.inputs_row, placeholder_text="YYYY-MM-DD", height=40)
        self.entry_checkout.grid(row=1, column=1, sticky="ew", padx=8, pady=(5, 0))

        # 3. Guests
        self.lbl_guests = ctk.CTkLabel(self.inputs_row, text="Guests", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_guests.grid(row=0, column=2, sticky="w", padx=8)
        self.combo_guests = ctk.CTkComboBox(self.inputs_row, values=["1 Guest", "2 Guests", "3-4 Guests", "Family"], height=40)
        self.combo_guests.grid(row=1, column=2, sticky="ew", padx=8, pady=(5, 0))

        # 4. Giá tối thiểu (Min Price)
        self.lbl_min_price = ctk.CTkLabel(self.inputs_row, text="Min Price ", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_min_price.grid(row=0, column=3, sticky="w", padx=8)
        self.entry_min_price = ctk.CTkEntry(self.inputs_row, placeholder_text="", height=40)
        self.entry_min_price.grid(row=1, column=3, sticky="ew", padx=8, pady=(5, 0))

        # 5. Giá tối đa (Max Price)
        self.lbl_max_price = ctk.CTkLabel(self.inputs_row, text="Max Price ", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_max_price.grid(row=0, column=4, sticky="w", padx=8)
        self.entry_max_price = ctk.CTkEntry(self.inputs_row, placeholder_text="", height=40)
        self.entry_max_price.grid(row=1, column=4, sticky="ew", padx=8, pady=(5, 0))

        # Nút SEARCH ROOMS
        self.btn_search = ctk.CTkButton(
            self.search_card,
            text="SEARCH ROOMS",
            height=45,
            width=240,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.on_search_click
        )
        self.btn_search.pack(pady=(10, 25))

        # TIÊU ĐỀ FEATURED ROOMS
        self.featured_title = ctk.CTkLabel(
            self.main_content,
            text="Featured Rooms",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.featured_title.pack(anchor="w", pady=(10, 15))

        # KHUNG CHỨA 3 CARD PHÒNG MẪU NẰM NGANG (FULL WIDTH)
        self.cards_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.cards_container.pack(fill="x")
        for col in range(3):
            self.cards_container.grid_columnconfigure(col, weight=1)

        featured_rooms_data = [
            {"title": "Deluxe", "price": "800,000 VNĐ", "desc": "Standard king size bed with city view."},
            {"title": "Family", "price": "1,200,000 VNĐ", "desc": "Spacious room for 4 people with 2 queen beds."},
            {"title": "Suite", "price": "2,500,000 VNĐ", "desc": "Luxury suite with private balcony & bathtub."}
        ]

        for i, room in enumerate(featured_rooms_data):
            card = ctk.CTkFrame(self.cards_container, corner_radius=10, border_width=1, border_color="#dddddd")
            card.grid(row=0, column=i, sticky="ew", padx=12, pady=5)

            # Khung hình đại diện phòng
            img_box = ctk.CTkFrame(card, height=110, fg_color="#1f538d", corner_radius=8)
            img_box.pack(fill="x", padx=15, pady=(15, 10))
            
            lbl_img = ctk.CTkLabel(img_box, text=f"📷 {room['title']}", text_color="white", font=ctk.CTkFont(size=16, weight="bold"))
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")

            lbl_card_title = ctk.CTkLabel(card, text=room["title"], font=ctk.CTkFont(size=18, weight="bold"))
            lbl_card_title.pack(pady=(5, 2))

            lbl_card_price = ctk.CTkLabel(card, text=room["price"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#28a745")
            lbl_card_price.pack(pady=(0, 12))

            btn_detail = ctk.CTkButton(
                card,
                text="Book Now",
                height=38,
                fg_color="#1f538d",
                font=ctk.CTkFont(weight="bold"),
                command=lambda r=room["title"]: self.on_book_room(r)
            )
            btn_detail.pack(padx=15, pady=(0, 15))

    # -----------------------------------------------------------------
    # LOGIC XỬ LÝ SỰ KIỆN
    # -----------------------------------------------------------------
    def on_login_click(self):
        messagebox.showinfo("Auth", "Navigate to Login Frame")

    def on_register_click(self):
        messagebox.showinfo("Auth", "Navigate to Register Frame")

    def on_search_click(self):
        min_price = self.entry_min_price.get().strip() or "0"
        max_price = self.entry_max_price.get().strip() or "∞"
        messagebox.showinfo(
            "Search", 
            f"Searching for rooms:\n"
            f"- Check-in: {self.entry_checkin.get()}\n"
            f"- Check-out: {self.entry_checkout.get()}\n"
            f"- Guests: {self.combo_guests.get()}\n"
            f"- Price range: ${min_price} - ${max_price}"
        )

    def on_book_room(self, room_name):
        messagebox.showinfo("Booking", f"You clicked Book Now for {room_name}")


if __name__ == "__main__":
    app = HotelBookingApp()
    app.mainloop()