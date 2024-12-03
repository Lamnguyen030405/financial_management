import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from datetime import datetime
import csv

from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh
from src.models.tai_khoan import TaiKhoan
from src.models.khoan_vay import KhoanVay
from src.models.giao_dich import GiaoDich
from src.models.danh_muc import DanhMuc

class QuanLyTaiChinhGUI:
    def __init__(self):
        # Cấu hình giao diện
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Cửa sổ chính
        self.root = ctk.CTk()
        self.root.title("Quản Lý Tài Chính")
        self.root.geometry("1000x700")

        # Quản lý tài chính backend
        self.quan_ly = QuanLyTaiChinh()
        self.quan_ly.nhap_csv()

        # Tạo khung chính
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Khung menu bên trái
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # Khung nội dung
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề
        self.title_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="HỆ THỐNG\nQUẢN LÝ\nTÀI CHÍNH", 
            font=("Helvetica", 20, "bold")
        )
        self.title_label.pack(pady=20)

        # Menu chính
        self.create_main_menu()

    def create_main_menu(self):
        """Tạo menu chính với các mục chính"""
        menu_items = [
            {
                "text": "Tài Khoản", 
                "sub_items": [
                    {"text": "Thêm Tài Khoản", "command": self.them_tai_khoan},
                    {"text": "Xóa Tài Khoản", "command": self.xoa_tai_khoan},
                    {"text": "Xem Tài Khoản", "command": self.xem_tai_khoan}
                ]
            },
            {
                "text": "Giao Dịch", 
                "sub_items": [
                    {"text": "Thêm Giao Dịch", "command": self.them_giao_dich},
                    {"text": "Xóa Giao Dịch", "command": self.xoa_giao_dich},
                    {"text": "Cập Nhật Giao Dịch", "command": self.cap_nhat_giao_dich},
                    {"text": "Xem Giao Dịch", "command": self.xem_giao_dich}
                    
                ]
            },
            {
                "text": "Khoản Vay", 
                "sub_items": [
                    {"text": "Thêm Khoản Vay", "command": self.them_khoan_vay},
                    {"text": "Xóa Khoản Vay", "command": self.xoa_khoan_vay},
                    {"text": "Thêm Thanh Toán", "command": self.them_thanh_toan},
                    {"text": "Xem Lịch Sử Thanh Toán", "command": self.xem_lich_su_thanh_toan},
                    {"text": "Xem Khoản Vay", "command": self.xem_khoan_vay}
                ]
            },
            {
                "text": "Danh Mục", 
                "sub_items": [
                    {"text": "Thêm Danh Mục", "command": self.them_danh_muc},
                    {"text": "Xóa Danh Mục", "command": self.xoa_danh_muc},
                    {"text": "Cập Nhật Danh Mục", "command": self.cap_nhat_danh_muc},
                    {"text": "Xem Danh Mục", "command": self.xem_danh_muc}
                ]
            },
            {
                "text": "Báo Cáo", 
                "sub_items": [
                    {"text": "Tạo Báo Cáo", "command": self.tao_bao_cao},
                    {"text": "Dự Báo Xu Hướng", "command": self.du_bao_xu_huong},
                    {"text": "Thống Kê Tổng Quát", "command": self.thong_ke_tong_quat},
                    {"text": "Đặt mục tiêu tiết kiệm", "command": self.dat_muc_tieu_tiet_kiem}
                ]
            },
            {
                "text": "Sáu Lọ", 
                "sub_items": [
                    {"text": "Thiết Lập", "command": self.thiet_lap_sau_lo},
                    {"text": "Xem Phân Bổ", "command": self.xem_phan_bo_sau_lo},
                    {"text": "Chuyển tiền giữa các lọ", "command": self.chuyen_tien_giua_cac_lo}
                ]
            },
            {
                "text": "Dữ Liệu", 
                "sub_items": [
                    {"text": "Xuất CSV", "command": self.xuat_csv},
                    {"text": "Nhập CSV", "command": self.nhap_csv}
                ]
            }
        ]

        for menu_item in menu_items:
            main_button = ctk.CTkButton(
                self.sidebar_frame, 
                text=menu_item["text"], 
                command=lambda m=menu_item: self.toggle_submenu(m)
            )
            main_button.pack(pady=5, padx=10, fill="x")
        
        def exit_application(): 
            """Xuất dữ liệu ra CSV và thoát ứng dụng""" 
            self.xuat_csv() 
            self.root.quit()
        
        # Nút thoát
        exit_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Thoát", 
            fg_color="red", 
            hover_color="darkred", 
            command=exit_application
        )
        exit_button.pack(side="bottom", pady=20, padx=10, fill="x")

    def toggle_submenu(self, menu_item):
        """Hiển thị submenu khi nhấn vào menu chính"""
        # Xóa các widget cũ trong content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Tạo tiêu đề
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text=menu_item["text"], 
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)

        # Tạo khung chứa các nút con
        submenu_frame = ctk.CTkFrame(self.content_frame)
        submenu_frame.pack(padx=20, pady=10, fill="x")

        # Tạo các nút chức năng con
        for sub_item in menu_item.get("sub_items", []):
            sub_button = ctk.CTkButton(
                submenu_frame, 
                text=sub_item["text"], 
                command=sub_item["command"]
            )
            sub_button.pack(pady=5, padx=10, fill="x")

    def them_danh_muc(self):
        """Thêm danh mục mới"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Danh Mục")
        dialog.geometry("400x500")

        # Các trường nhập liệu
        entries = [
            ("ID Danh Mục", "id_danh_muc"),
            ("Tên Danh Mục", "ten_danh_muc"),
            ("Loại Danh Mục", "loai_danh_muc"),
            ("Mô Tả Danh Mục", "mo_ta_danh_muc")
        ]

        entry_widgets = {}
        for i, (label_text, attr_name) in enumerate(entries):
            label = ctk.CTkLabel(dialog, text=label_text)
            label.pack(pady=(10 if i==0 else 5, 0))
            
            entry = ctk.CTkEntry(dialog, width=300)
            entry.pack(pady=5)
            entry_widgets[attr_name] = entry

        def submit():
            # Lấy giá trị từ các ô nhập liệu
            danh_muc = DanhMuc(
                entry_widgets['id_danh_muc'].get(),
                entry_widgets['ten_danh_muc'].get(),
                entry_widgets['loai_danh_muc'].get(),
                entry_widgets['mo_ta_danh_muc'].get()
            )
            
            # Thử thêm danh mục
            if self.quan_ly.them_danh_muc(danh_muc):
                messagebox.showinfo("Thành Công", "Thêm danh mục thành công!")
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "ID danh mục đã tồn tại!")

        # Nút xác nhận
        submit_button = ctk.CTkButton(dialog, text="Thêm", command=submit)
        submit_button.pack(pady=20)

    def xoa_danh_muc(self):
        """Xóa danh mục"""
        id_danh_muc = simpledialog.askstring("Xóa Danh Mục", "Nhập ID danh mục cần xóa:")
        
        if id_danh_muc:
            # Gọi phương thức xóa danh mục từ quản lý
            self.quan_ly.xoa_danh_muc(id_danh_muc)
            messagebox.showinfo("Thành Công", "Đã xóa danh mục.")
            
    def cap_nhat_danh_muc(self):
        """Cập nhật danh mục trong hệ thống"""
        # Tạo cửa sổ dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Cập Nhật Danh Mục")
        dialog.geometry("400x300")

        # Label hướng dẫn
        huong_dan_label = ctk.CTkLabel(
            dialog, 
            text="Nhập thông tin để cập nhật danh mục", 
            font=("Helvetica", 14, "bold"),
            wraplength=350
        )
        huong_dan_label.pack(pady=(20, 10))

        # Nhập ID danh mục
        id_danh_muc_frame = ctk.CTkFrame(dialog)
        id_danh_muc_frame.pack(pady=10, padx=20, fill="x")

        id_danh_muc_label = ctk.CTkLabel(id_danh_muc_frame, text="ID Danh Mục:", font=("Helvetica", 12))
        id_danh_muc_label.pack(side="left", padx=10)

        id_danh_muc_entry = ctk.CTkEntry(id_danh_muc_frame, width=150)
        id_danh_muc_entry.pack(side="right", padx=10)

        # Nhập tên danh mục
        ten_frame = ctk.CTkFrame(dialog)
        ten_frame.pack(pady=10, padx=20, fill="x")

        ten_label = ctk.CTkLabel(ten_frame, text="Tên:", font=("Helvetica", 12))
        ten_label.pack(side="left", padx=10)

        ten_entry = ctk.CTkEntry(ten_frame, width=150)
        ten_entry.pack(side="right", padx=10)

        # Nhập loại danh mục với dropdown menu
        loai_label = ctk.CTkLabel(dialog, text="Loại Danh Mục:")
        loai_label.pack(pady=(10, 0))
    
        loai_options = ["Chi tiêu", "Thu nhập"]
        loai_var = tk.StringVar(dialog)
        loai_var.set(loai_options[0])
    
        loai_dropdown = ttk.Combobox(dialog, textvariable=loai_var, values=loai_options)
        loai_dropdown.pack(pady=5)

        def submit_cap_nhat():
            # Lấy thông tin từ các entry
            id_danh_muc = id_danh_muc_entry.get()
            ten = ten_entry.get()
            loai = loai_var.get()  # Lấy giá trị loại danh mục từ dropdown

            # Gọi phương thức cập nhật danh mục
            if self.quan_ly.cap_nhat_danh_muc(id_danh_muc, ten, loai):
                messagebox.showinfo("Thành Công", "Cập nhật danh mục thành công!")
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật danh mục!")

        submit_button = ctk.CTkButton(dialog, text="Xác Nhận", command=submit_cap_nhat)
        submit_button.pack(pady=20)

    def them_tai_khoan(self):
        """Thêm tài khoản mới"""
        # Tạo cửa sổ dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Tài Khoản")
        dialog.geometry("400x500")

        # Các trường nhập liệu
        entries = [
            ("ID Tài Khoản", "id_tai_khoan"),
            ("Tên Tài Khoản", "ten_tai_khoan"),
            ("Số Dư", "so_du"),
            ("Loại Tài Khoản", "loai_tai_khoan")
        ]

        entry_widgets = {}
        for i, (label_text, attr_name) in enumerate(entries):
            label = ctk.CTkLabel(dialog, text=label_text)
            label.pack(pady=(10 if i==0 else 5, 0))
            
            entry = ctk.CTkEntry(dialog, width=300)
            entry.pack(pady=5)
            entry_widgets[attr_name] = entry

        def submit():
            try:
                tai_khoan = TaiKhoan(
                    entry_widgets['id_tai_khoan'].get(),
                    entry_widgets['ten_tai_khoan'].get(),
                    float(entry_widgets['so_du'].get()),
                    entry_widgets['loai_tai_khoan'].get()
                )
                
                if self.quan_ly.them_tai_khoan(tai_khoan):
                    messagebox.showinfo("Thành Công", "Thêm tài khoản thành công!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "ID tài khoản đã tồn tại!")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số tiền!")

        submit_button = ctk.CTkButton(dialog, text="Thêm", command=submit)
        submit_button.pack(pady=20)

    def xoa_tai_khoan(self):
        """Xóa tài khoản"""
        id_tai_khoan = simpledialog.askstring("Xóa Tài Khoản", "Nhập ID tài khoản cần xóa:")
        if id_tai_khoan:
            self.quan_ly.xoa_tai_khoan(id_tai_khoan)
            messagebox.showinfo("Thành Công", "Đã xóa tài khoản.")

    def xem_tai_khoan(self):
        """Hiển thị thông tin tài khoản từ file CSV"""
        file_path = 'taikhoan.csv'

        # Xóa các widget cũ trong content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Tạo tiêu đề
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text="Thông Tin Tài Khoản", 
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)

        # Tạo khung chứa bảng thông tin tài khoản
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Tạo bảng
        columns = ("ID", "Tên", "Số Dư", "Loại")
        account_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        account_table.pack(fill="both", expand=True)

        # Đặt tên cho các cột
        for col in columns:
            account_table.heading(col, text=col)

        # Đặt độ rộng cho các cột
        account_table.column("ID", width=100)
        account_table.column("Tên", width=200)
        account_table.column("Số Dư", width=100)
        account_table.column("Loại", width=150)

        # Đọc dữ liệu từ file CSV và thêm vào bảng
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                account_table.insert("", "end", values=(row["ID"], row["Tên"], row["Số Dư"], row["Loại"]))

    def xem_giao_dich(self):
        """Hiển thị thông tin giao dịch từ file CSV"""
        file_path = 'giaodich.csv'

        # Xóa các widget cũ trong content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Tạo tiêu đề
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text="Thông Tin Giao Dịch", 
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)

        # Tạo khung chứa bảng thông tin giao dịch
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Tạo bảng
        columns = ("ID", "ID Tài Khoản", "Số Tiền", "Loại", "Danh Mục", "Ngày", "Ghi Chú")
        transaction_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        transaction_table.pack(fill="both", expand=True)

        # Đặt tên cho các cột
        for col in columns:
            transaction_table.heading(col, text=col)

        # Đặt độ rộng cho các cột
        transaction_table.column("ID", width=100)
        transaction_table.column("ID Tài Khoản", width=150)
        transaction_table.column("Số Tiền", width=100)
        transaction_table.column("Loại", width=100)
        transaction_table.column("Danh Mục", width=150)
        transaction_table.column("Ngày", width=100)
        transaction_table.column("Ghi Chú", width=200)

        # Đọc dữ liệu từ file CSV và thêm vào bảng
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                transaction_table.insert("", "end", values=(row["ID"], row["ID Tài Khoản"], row["Số Tiền"], row["Loại"], row["Danh Mục"], row["Ngày"], row["Ghi Chú"]))

    def xem_khoan_vay(self):
        """Hiển thị thông tin khoản vay từ file CSV"""
        file_path = 'khoanvay.csv'

        # Xóa các widget cũ trong content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Tạo tiêu đề
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text="Thông Tin Khoản Vay", 
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)

        # Tạo khung chứa bảng thông tin khoản vay
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Tạo bảng
        columns = ("ID", "Số Tiền", "Người Cho Vay", "Người Vay", "Lãi Suất", "Ngày Bắt Đầu", "Ngày Đến Hạn", "Trạng Thái", "Số Tiền Còn Lại")
        loan_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        loan_table.pack(fill="both", expand=True)

        # Đặt tên cho các cột
        for col in columns:
            loan_table.heading(col, text=col)

        # Đặt độ rộng cho các cột
        loan_table.column("ID", width=100)
        loan_table.column("Số Tiền", width=100)
        loan_table.column("Người Cho Vay", width=150)
        loan_table.column("Người Vay", width=150)
        loan_table.column("Lãi Suất", width=100)
        loan_table.column("Ngày Bắt Đầu", width=100)
        loan_table.column("Ngày Đến Hạn", width=100)
        loan_table.column("Trạng Thái", width=100)
        loan_table.column("Số Tiền Còn Lại", width=100)

        # Đọc dữ liệu từ file CSV và thêm vào bảng
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    loan_table.insert("", "end", values=(row["ID"], row["Số Tiền"], row["Người Cho Vay"], row["Người Vay"], row["Lãi Suất"], row["Ngày Bắt Đầu"], row["Ngày Đến Hạn"], row["Trạng Thái"], row["Số Tiền Còn Lại"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file {file_path}: {e}")

    def xem_danh_muc(self):
        """Hiển thị thông tin danh mục từ file CSV"""
        file_path = 'danhmuc.csv'

        # Xóa các widget cũ trong content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Tạo tiêu đề
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text="Thông Tin Danh Mục", 
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)

        # Tạo khung chứa bảng thông tin danh mục
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Tạo bảng
        columns = ("ID", "Tên", "Loại", "Mô Tả")
        category_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        category_table.pack(fill="both", expand=True)

        # Đặt tên cho các cột
        for col in columns:
            category_table.heading(col, text=col)

        # Đặt độ rộng cho các cột
        category_table.column("ID", width=100)
        category_table.column("Tên", width=200)
        category_table.column("Loại", width=100)
        category_table.column("Mô Tả", width=200)

        # Đọc dữ liệu từ file CSV và thêm vào bảng
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                category_table.insert("", "end", values=(row["ID"], row["Tên"], row["Loại"], row["Mô Tả"]))

    def xem_lich_su_thanh_toan(self):
        """Hiển thị lịch sử thanh toán từ file CSV"""
        file_path = 'lichsuthanhtoan.csv'

        # Xóa các widget cũ trong content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Tạo tiêu đề
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text="Lịch Sử Thanh Toán", 
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)

        # Tạo khung chứa bảng lịch sử thanh toán
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Tạo bảng
        columns = ("ID Khoản Vay", "Số Tiền", "Ngày Thanh Toán")
        payment_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        payment_table.pack(fill="both", expand=True)

        # Đặt tên cho các cột
        for col in columns:
            payment_table.heading(col, text=col)

        # Đặt độ rộng cho các cột
        payment_table.column("ID Khoản Vay", width=150)
        payment_table.column("Số Tiền", width=100)
        payment_table.column("Ngày Thanh Toán", width=150)

        # Đọc dữ liệu từ file CSV và thêm vào bảng
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    payment_table.insert("", "end", values=(row["ID Khoản Vay"], row["Số Tiền"], row["Ngày Thanh Toán"]))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file {file_path}: {e}")

    def them_giao_dich(self):
        """Thêm giao dịch mới"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Giao Dịch")
        dialog.geometry("400x600")

        entries = [
            ("ID Giao Dịch", "id"),
            ("ID Tài Khoản", "id_tai_khoan"),
            ("Số Tiền", "so_tien"),
            ("Ngày", "ngay"),
            ("Ghi Chú", "ghi_chu")
        ]

        entry_widgets = {}
        for i, (label_text, attr_name) in enumerate(entries):
            label = ctk.CTkLabel(dialog, text=label_text)
            label.pack(pady=(10 if i == 0 else 5, 0))
    
            entry = ctk.CTkEntry(dialog, width=300)
            entry.pack(pady=5)
            entry_widgets[attr_name] = entry

        # Thêm dropdown để chọn loại giao dịch
        loai_giao_dich_label = ctk.CTkLabel(dialog, text="Loại Giao Dịch")
        loai_giao_dich_label.pack(pady=(10, 0))

        loai_giao_dich_options = ["Chi tiêu", "Thu nhập"]
        loai_giao_dich_var = tk.StringVar(dialog)
        loai_giao_dich_var.set(loai_giao_dich_options[0])

        loai_giao_dich_dropdown = ttk.Combobox(dialog, textvariable=loai_giao_dich_var, values=loai_giao_dich_options)
        loai_giao_dich_dropdown.pack(pady=5)

        # Thêm dropdown để chọn danh mục
        danh_muc_label = ctk.CTkLabel(dialog, text="Danh Mục")
        danh_muc_label.pack(pady=(10, 0))

        # Lấy danh sách tên danh mục từ self.quan_ly._danh_muc
        danh_muc_options = [dm._ten for dm in self.quan_ly._danh_muc]
        danh_muc_var = tk.StringVar(dialog)
        danh_muc_var.set(danh_muc_options[0] if danh_muc_options else "")

        danh_muc_dropdown = ttk.Combobox(dialog, textvariable=danh_muc_var, values=danh_muc_options)
        danh_muc_dropdown.pack(pady=5)

        def submit():
            try:
                giao_dich = GiaoDich(
                    entry_widgets['id'].get(),
                    entry_widgets['id_tai_khoan'].get(),
                    float(entry_widgets['so_tien'].get()),
                    loai_giao_dich_var.get(),  # Lấy giá trị loại giao dịch từ dropdown
                    danh_muc_var.get(),  # Lấy giá trị danh mục từ dropdown
                    datetime.strptime(entry_widgets['ngay'].get(), "%Y-%m-%d"),
                    entry_widgets['ghi_chu'].get()
                )
        
                if self.quan_ly.them_giao_dich(giao_dich):
                    messagebox.showinfo("Thành Công", "Thêm giao dịch thành công!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy tài khoản!")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        submit_button = ctk.CTkButton(dialog, text="Thêm", command=submit)
        submit_button.pack(pady=20)

    def xoa_giao_dich(self):
        """Xóa giao dịch"""
        id_tai_khoan = simpledialog.askstring("Xóa Giao Dịch", "Nhập ID tài khoản:")
        id_giao_dich = simpledialog.askstring("Xóa Giao Dịch", "Nhập ID giao dịch:")
        
        if id_tai_khoan and id_giao_dich:
            self.quan_ly.xoa_giao_dich(id_tai_khoan, id_giao_dich)
            messagebox.showinfo("Thành Công", "Đã xóa giao dịch.")
            
    def cap_nhat_giao_dich(self):
        """Cập nhật giao dịch trong một tài khoản"""
        # Tạo cửa sổ dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Cập Nhật Giao Dịch")
        dialog.geometry("400x400")

        # Label hướng dẫn
        huong_dan_label = ctk.CTkLabel(
            dialog, 
            text="Nhập thông tin để cập nhật giao dịch", 
            font=("Helvetica", 14, "bold"),
            wraplength=350
        )
        huong_dan_label.pack(pady=(20, 10))

        # Nhập ID tài khoản
        id_tai_khoan_frame = ctk.CTkFrame(dialog)
        id_tai_khoan_frame.pack(pady=10, padx=20, fill="x")

        id_tai_khoan_label = ctk.CTkLabel(id_tai_khoan_frame, text="ID Tài Khoản:", font=("Helvetica", 12))
        id_tai_khoan_label.pack(side="left", padx=10)

        id_tai_khoan_entry = ctk.CTkEntry(id_tai_khoan_frame, width=150)
        id_tai_khoan_entry.pack(side="right", padx=10)

        # Nhập ID giao dịch
        id_giao_dich_frame = ctk.CTkFrame(dialog)
        id_giao_dich_frame.pack(pady=10, padx=20, fill="x")

        id_giao_dich_label = ctk.CTkLabel(id_giao_dich_frame, text="ID Giao Dịch:", font=("Helvetica", 12))
        id_giao_dich_label.pack(side="left", padx=10)

        id_giao_dich_entry = ctk.CTkEntry(id_giao_dich_frame, width=150)
        id_giao_dich_entry.pack(side="right", padx=10)

        # Nhập số tiền
        so_tien_frame = ctk.CTkFrame(dialog)
        so_tien_frame.pack(pady=10, padx=20, fill="x")

        so_tien_label = ctk.CTkLabel(so_tien_frame, text="Số Tiền:", font=("Helvetica", 12))
        so_tien_label.pack(side="left", padx=10)

        so_tien_entry = ctk.CTkEntry(so_tien_frame, width=150)
        so_tien_entry.pack(side="right", padx=10)

        # Nhập loại giao dịch với dropdown menu
        loai_label = ctk.CTkLabel(dialog, text="Loại Giao Dịch:")
        loai_label.pack(pady=(10, 0))
    
        loai_options = ["Chi tiêu", "Thu nhập"]
        loai_var = tk.StringVar(dialog)
        loai_var.set(loai_options[0])
    
        loai_dropdown = ttk.Combobox(dialog, textvariable=loai_var, values=loai_options)
        loai_dropdown.pack(pady=5)

        def submit_cap_nhat():
            try:
                # Lấy thông tin từ các entry
                id_tai_khoan = id_tai_khoan_entry.get()
                id_giao_dich = id_giao_dich_entry.get()
                so_tien = float(so_tien_entry.get())
                loai = loai_var.get()  # Lấy giá trị loại giao dịch từ dropdown

                # Gọi phương thức cập nhật giao dịch
                if self.quan_ly.cap_nhat_giao_dich(id_tai_khoan, id_giao_dich, so_tien, loai):
                    messagebox.showinfo("Thành Công", "Cập nhật giao dịch thành công!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không thể cập nhật giao dịch!")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ!")

        submit_button = ctk.CTkButton(dialog, text="Xác Nhận", command=submit_cap_nhat)
        submit_button.pack(pady=20)

    def them_khoan_vay(self):
        """Thêm khoản vay mới"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Khoản Vay")
        dialog.geometry("400x700")

        entries = [
            ("ID Khoản Vay", "id_khoan_vay"),
            ("Người Cho Vay", "nguoi_cho_vay"),
            ("Số Tiền", "so_tien"),
            ("Người Vay", "nguoi_vay"),
            ("Lãi Suất (%)", "lai_suat"),
            ("Ngày Bắt Đầu", "ngay_bat_dau"),
            ("Ngày Đến Hạn", "ngay_den_han")
        ]

        entry_widgets = {}
        for i, (label_text, attr_name) in enumerate(entries):
            label = ctk.CTkLabel(dialog, text=label_text)
            label.pack(pady=(10 if i==0 else 5, 0))
            
            entry = ctk.CTkEntry(dialog, width=300)
            entry.pack(pady=5)
            entry_widgets[attr_name] = entry

        def submit():
            try:
                khoan_vay = KhoanVay(
                    entry_widgets['id_khoan_vay'].get(),
                    float(entry_widgets['so_tien'].get()),
                    entry_widgets['nguoi_cho_vay'].get(),
                    entry_widgets['nguoi_vay'].get(),
                    float(entry_widgets['lai_suat'].get()),
                    datetime.strptime(entry_widgets['ngay_bat_dau'].get(), "%Y-%m-%d"),
                    datetime.strptime(entry_widgets['ngay_den_han'].get(), "%Y-%m-%d")
                )
                
                if self.quan_ly.them_khoan_vay(khoan_vay):
                    messagebox.showinfo("Thành Công", "Thêm khoản vay thành công!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "ID khoản vay đã tồn tại!")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        submit_button = ctk.CTkButton(dialog, text="Thêm", command=submit)
        submit_button.pack(pady=20)

    def xoa_khoan_vay(self):
        """Xóa khoản vay"""
        id_khoan_vay = simpledialog.askstring("Xóa Khoản Vay", "Nhập ID khoản vay cần xóa:")
        if id_khoan_vay:
            self.quan_ly.xoa_khoan_vay(id_khoan_vay)
            messagebox.showinfo("Thành Công", "Đã xóa khoản vay.")
            
    def them_thanh_toan(self):
        """Thêm thanh toán mới cho khoản vay"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Thanh Toán")
        dialog.geometry("400x300")

        # Label hướng dẫn
        huong_dan_label = ctk.CTkLabel(
            dialog, 
            text="Nhập thông tin để thêm thanh toán cho khoản vay", 
            font=("Helvetica", 14, "bold"),
            wraplength=350
        )
        huong_dan_label.pack(pady=(20, 10))

        # Nhập ID khoản vay
        id_khoan_vay_frame = ctk.CTkFrame(dialog)
        id_khoan_vay_frame.pack(pady=10, padx=20, fill="x")

        id_khoan_vay_label = ctk.CTkLabel(id_khoan_vay_frame, text="ID Khoản Vay:", font=("Helvetica", 12))
        id_khoan_vay_label.pack(side="left", padx=10)

        id_khoan_vay_entry = ctk.CTkEntry(id_khoan_vay_frame, width=150)
        id_khoan_vay_entry.pack(side="right", padx=10)

        # Nhập số tiền thanh toán
        so_tien_frame = ctk.CTkFrame(dialog)
        so_tien_frame.pack(pady=10, padx=20, fill="x")

        so_tien_label = ctk.CTkLabel(so_tien_frame, text="Số Tiền:", font=("Helvetica", 12))
        so_tien_label.pack(side="left", padx=10)

        so_tien_entry = ctk.CTkEntry(so_tien_frame, width=150)
        so_tien_entry.pack(side="right", padx=10)

        # Nhập ngày thanh toán
        ngay_frame = ctk.CTkFrame(dialog)
        ngay_frame.pack(pady=10, padx=20, fill="x")

        ngay_label = ctk.CTkLabel(ngay_frame, text="Ngày (YYYY-MM-DD):", font=("Helvetica", 12))
        ngay_label.pack(side="left", padx=10)

        ngay_entry = ctk.CTkEntry(ngay_frame, width=150)
        ngay_entry.pack(side="right", padx=10)

        def submit_thanh_toan():
            try:
                # Lấy thông tin từ các entry
                id_khoan_vay = id_khoan_vay_entry.get()
                so_tien = float(so_tien_entry.get())
                ngay = datetime.strptime(ngay_entry.get(), "%Y-%m-%d")

                # Gọi phương thức thêm thanh toán
                if self.quan_ly.them_thanh_toan(id_khoan_vay, so_tien, ngay):
                    messagebox.showinfo("Thành Công", "Thêm thanh toán thành công!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không thể thêm thanh toán!")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        submit_button = ctk.CTkButton(dialog, text="Xác Nhận", command=submit_thanh_toan)
        submit_button.pack(pady=20)

    def tao_bao_cao(self):
        """Tạo báo cáo tài chính và hiển thị trên GUI"""
        try:
            # Yêu cầu người dùng nhập ngày bắt đầu và ngày kết thúc
            ngay_bat_dau = datetime.strptime(
                simpledialog.askstring("Báo Cáo", "Nhập ngày bắt đầu (YYYY-MM-DD):"), 
                "%Y-%m-%d"
            )
            ngay_ket_thuc = datetime.strptime(
                simpledialog.askstring("Báo Cáo", "Nhập ngày kết thúc (YYYY-MM-DD):"), 
                "%Y-%m-%d"
            )
        
            # Lấy dữ liệu báo cáo từ hàm tao_bao_cao_tai_chinh
            bao_cao = self.quan_ly.tao_bao_cao_tai_chinh(ngay_bat_dau, ngay_ket_thuc)
        
            # Xóa các widget cũ trong content frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Tạo tiêu đề
            title_label = ctk.CTkLabel(
                self.content_frame, 
                text="Báo Cáo Tài Chính", 
                font=("Helvetica", 20, "bold")
            )
            title_label.pack(pady=20)

            # Tổng số dư và tổng nợ
            summary_frame = ctk.CTkFrame(self.content_frame)
            summary_frame.pack(pady=10, padx=20, fill="x")

            tong_so_du_label = ctk.CTkLabel(
                summary_frame, 
                text=f"Tổng Số Dư: {bao_cao['tong_so_du']}", 
                font=("Helvetica", 14, "bold")
            )
            tong_so_du_label.pack(side="left", padx=10)

            tong_no_label = ctk.CTkLabel(
                summary_frame, 
                text=f"Tổng Nợ: {bao_cao['tong_no']}", 
                font=("Helvetica", 14, "bold")
            )
            tong_no_label.pack(side="right", padx=10)

            # Bảng chi tiết tài khoản
            tk_details_frame = ctk.CTkFrame(self.content_frame)
            tk_details_frame.pack(pady=10, padx=20, fill="both", expand=True)

            tk_columns = ("ID", "Tên", "Số Dư")
            tk_table = ttk.Treeview(tk_details_frame, columns=tk_columns, show='headings')
            tk_table.pack(fill="both", expand=True)

            for col in tk_columns:
                tk_table.heading(col, text=col)
                tk_table.column(col, width=100)

            for chi_tiet in bao_cao["chi_tiet_tai_khoan"]:
                tk_table.insert("", "end", values=(chi_tiet["id"], chi_tiet["ten"], chi_tiet["so_du"]))

            # Bảng giao dịch theo danh mục
            gd_details_frame = ctk.CTkFrame(self.content_frame)
            gd_details_frame.pack(pady=10, padx=20, fill="both", expand=True)

            gd_columns = ("Danh Mục", "Tổng Thu", "Tổng Chi")
            gd_table = ttk.Treeview(gd_details_frame, columns=gd_columns, show='headings')
            gd_table.pack(fill="both", expand=True)

            for col in gd_columns:
                gd_table.heading(col, text=col)
                gd_table.column(col, width=100)

            for danh_muc, values in bao_cao["giao_dich_theo_danh_muc"].items():
                gd_table.insert("", "end", values=(danh_muc, values["tong_thu"], values["tong_chi"]))
    
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tạo báo cáo: {e}")

            
    def du_bao_xu_huong(self):
        """Dự báo xu hướng tài chính và hiển thị kết quả trên GUI"""
        # Lấy dữ liệu dự báo
        du_bao = self.quan_ly.du_bao_xu_huong_tai_chinh()

        # Xóa các widget cũ trong content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Tạo tiêu đề
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text="Dự Báo Xu Hướng Tài Chính", 
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=20)

        # Khung chứa bảng xu hướng chi tiêu
        chi_tieu_frame = ctk.CTkFrame(self.content_frame)
        chi_tieu_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Bảng xu hướng chi tiêu
        chi_tieu_table = ttk.Treeview(chi_tieu_frame, columns=("Danh Mục", "Trung Bình", "Tổng Chi"), show='headings')
        chi_tieu_table.pack(fill="both", expand=True)
        chi_tieu_table.heading("Danh Mục", text="Danh Mục")
        chi_tieu_table.heading("Trung Bình", text="Trung Bình")
        chi_tieu_table.heading("Tổng Chi", text="Tổng Chi")

        for danh_muc, data in du_bao["xu_huong_chi_tieu"].items():
            chi_tieu_table.insert("", "end", values=(danh_muc, data["trung_binh"], data["tong_chi"]))

        # Khung chứa bảng dự báo tiết kiệm
        tiet_kiem_frame = ctk.CTkFrame(self.content_frame)
        tiet_kiem_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Bảng dự báo tiết kiệm
        tiet_kiem_table = ttk.Treeview(tiet_kiem_frame, columns=("ID Tài Khoản", "Mục Tiêu", "Số Dư Hiện Tại"), show='headings')
        tiet_kiem_table.pack(fill="both", expand=True)
        tiet_kiem_table.heading("ID Tài Khoản", text="ID Tài Khoản")
        tiet_kiem_table.heading("Mục Tiêu", text="Mục Tiêu")
        tiet_kiem_table.heading("Số Dư Hiện Tại", text="Số Dư Hiện Tại")

        for id_tai_khoan, data in du_bao["du_bao_tiet_kiem"].items():
            tiet_kiem_table.insert("", "end", values=(id_tai_khoan, data["muc_tieu"], data["so_du_hien_tai"]))

        # Khung chứa bảng cảnh báo nợ
        no_frame = ctk.CTkFrame(self.content_frame)
        no_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Bảng cảnh báo nợ
        no_table = ttk.Treeview(no_frame, columns=("ID", "Số Tiền Còn Lại", "Người Cho Vay", "Ngày Đến Hạn"), show='headings')
        no_table.pack(fill="both", expand=True)
        no_table.heading("ID", text="ID")
        no_table.heading("Số Tiền Còn Lại", text="Số Tiền Còn Lại")
        no_table.heading("Người Cho Vay", text="Người Cho Vay")
        no_table.heading("Ngày Đến Hạn", text="Ngày Đến Hạn")

        for canh_bao in du_bao["canh_bao_no"]:
            no_table.insert("", "end", values=(canh_bao["id"], canh_bao["so_tien_con_lai"], canh_bao["nguoi_cho_vay"], canh_bao["ngay_den_han"]))

        messagebox.showinfo("Dự Báo Xu Hướng", "Dự báo xu hướng tài chính đã được cập nhật và hiển thị.")

    def thong_ke_tong_quat(self):
        """Lấy thống kê tổng quát"""
        thong_ke = self.quan_ly.lay_thong_ke_tong_quat()
        
        # Tạo cửa sổ thống kê
        thong_ke_window = ctk.CTkToplevel(self.root)
        thong_ke_window.title("Thống Kê Tổng Quát")
        thong_ke_window.geometry("500x400")

        # Tạo khung cuộn để hiển thị thống kê
        scrollable_frame = ctk.CTkScrollableFrame(thong_ke_window, width=450, height=350)
        scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Tiêu đề
        title_label = ctk.CTkLabel(
            scrollable_frame, 
            text="THỐNG KÊ TÀI CHÍNH", 
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Hiển thị từng mục thống kê
        for key, value in thong_ke.items():
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(fill="x", pady=5)

            key_label = ctk.CTkLabel(row_frame, text=str(key), font=("Helvetica", 14))
            key_label.pack(side="left", padx=10)

            value_label = ctk.CTkLabel(row_frame, text=str(value), font=("Helvetica", 14, "bold"))
            value_label.pack(side="right", padx=10)
    
    def dat_muc_tieu_tiet_kiem(self):
        """Đặt mục tiêu tiết kiệm cho một tài khoản"""
        # Tạo cửa sổ dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Đặt Mục Tiêu Tiết Kiệm")
        dialog.geometry("400x300")

        # Label hướng dẫn
        huong_dan_label = ctk.CTkLabel(
            dialog, 
            text="Nhập thông tin để đặt mục tiêu tiết kiệm", 
            font=("Helvetica", 14, "bold"),
            wraplength=350
        )
        huong_dan_label.pack(pady=(20, 10))

        # Nhập ID tài khoản
        id_tai_khoan_frame = ctk.CTkFrame(dialog)
        id_tai_khoan_frame.pack(pady=10, padx=20, fill="x")

        id_tai_khoan_label = ctk.CTkLabel(id_tai_khoan_frame, text="ID Tài Khoản:", font=("Helvetica", 12))
        id_tai_khoan_label.pack(side="left", padx=10)

        id_tai_khoan_entry = ctk.CTkEntry(id_tai_khoan_frame, width=150)
        id_tai_khoan_entry.pack(side="right", padx=10)

        # Nhập số tiền mục tiêu
        so_tien_frame = ctk.CTkFrame(dialog)
        so_tien_frame.pack(pady=10, padx=20, fill="x")

        so_tien_label = ctk.CTkLabel(so_tien_frame, text="Số Tiền Mục Tiêu:", font=("Helvetica", 12))
        so_tien_label.pack(side="left", padx=10)

        so_tien_entry = ctk.CTkEntry(so_tien_frame, width=150)
        so_tien_entry.pack(side="right", padx=10)

        def submit_dat_muc_tieu():
            try:
                # Lấy thông tin từ các entry
                id_tai_khoan = id_tai_khoan_entry.get()
                so_tien = float(so_tien_entry.get())

                # Gọi phương thức đặt mục tiêu tiết kiệm
                if self.quan_ly.dat_muc_tieu_tiet_kiem(id_tai_khoan, so_tien):
                    messagebox.showinfo("Thành Công", "Đặt mục tiêu tiết kiệm thành công!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không thể đặt mục tiêu tiết kiệm!")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ!")

        submit_button = ctk.CTkButton(dialog, text="Xác Nhận", command=submit_dat_muc_tieu)
        submit_button.pack(pady=20)

    def xuat_csv(self):
        """Xuất dữ liệu ra CSV"""
        self.quan_ly.xuat_csv()
        messagebox.showinfo("Xuất CSV", "Xuất dữ liệu CSV thành công!")
        
    def nhap_csv(self):
        """Nhập dữ liệu từ CSV"""
        self.quan_ly.nhap_csv()
        messagebox.showinfo("Nhập CSV", "Nhập dữ liệu CSV thành công!")

    def thiet_lap_sau_lo(self):
        """Thiết lập phương pháp sáu lọ"""
        # Tạo cửa sổ dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thiết Lập Phương Pháp Sáu Lọ")
        dialog.geometry("400x300")

        # Label hướng dẫn
        huong_dan_label = ctk.CTkLabel(
            dialog, 
            text="Phương Pháp Sáu Lọ sẽ phân bổ thu nhập của bạn",
            font=("Helvetica", 14, "bold"),
            wraplength=350
        )
        huong_dan_label.pack(pady=(20, 10))

        # Lấy tổng thu nhập sử dụng hàm tong_thu_nhap
        tong_thu_nhap = self.quan_ly.tinh_tong_thu_nhap()

        def submit_thu_nhap():
            # Gọi phương thức thiết lập sáu lọ
            if not self.quan_ly.thiet_lap_phuong_phap_sau_lo(tong_thu_nhap):
                messagebox.showinfo("Thành Công", "Thiết lập phương pháp sáu lọ thành công!")
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể thiết lập phương pháp sáu lọ!")

        # Hiển thị tổng thu nhập trong label
        thu_nhap_label = ctk.CTkLabel(
            dialog, 
            text=f"Tổng Thu Nhập: {tong_thu_nhap}", 
            font=("Helvetica", 12, "bold")
        )
        thu_nhap_label.pack(pady=(10, 20))

        submit_button = ctk.CTkButton(dialog, text="Xác Nhận", command=submit_thu_nhap)
        submit_button.pack(pady=20)

    def xem_phan_bo_sau_lo(self):
        """Xem phân bổ phương pháp sáu lọ"""
        # Kiểm tra xem đã thiết lập phương pháp sáu lọ chưa
        if not self.quan_ly._phuong_phap_sau_lo:
            messagebox.showwarning("Cảnh Báo", "Chưa thiết lập phương pháp sáu lọ. Vui lòng thiết lập trước!")
            return

        # Tạo cửa sổ hiển thị
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Phân Bổ Sáu Lọ")
        dialog.geometry("500x400")

        # Tiêu đề
        title_label = ctk.CTkLabel(
            dialog, 
            text="PHÂN BỔ THU NHẬP THEO PHƯƠNG PHÁP SÁU LỌ", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Tạo khung cuộn
        scrollable_frame = ctk.CTkScrollableFrame(dialog, width=450, height=300)
        scrollable_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Lấy thông tin phân bổ
        phan_bo = self.quan_ly._phuong_phap_sau_lo._lo

        # Từ điển màu sắc cho các lọ
        mau_sac = {
            "Thiết Yếu": "#FF6B6B",   # Đỏ nhạt
            "Tiết Kiệm": "#4ECDC4",    # Xanh ngọc
            "Giáo Dục": "#45B7D1",     # Xanh dương nhạt
            "Hưởng Thụ": "#FDCB6E",    # Vàng
            "Đầu Tư": "#6C5CE7",       # Tím
            "Từ Thiện": "#A8E6CF"      # Xanh lá nhạt
        }

        # Hiển thị từng mục phân bổ
        tong_thu_nhap = sum(phan_bo.values())
        for ten_lo, so_tien in phan_bo.items():
            # Frame cho mỗi lọ
            lo_frame = ctk.CTkFrame(scrollable_frame)
            lo_frame.pack(fill="x", pady=5)

            # Tên lọ
            ten_lo_label = ctk.CTkLabel(
                lo_frame, 
                text=ten_lo, 
                font=("Helvetica", 14),
                text_color=mau_sac.get(ten_lo, "#000000")
            )
            ten_lo_label.pack(side="left", padx=10)

            # Số tiền và phần trăm
            phan_tram = (so_tien / tong_thu_nhap) * 100
            so_tien_label = ctk.CTkLabel(
                lo_frame, 
                text=f"{so_tien:,.0f} VNĐ ({phan_tram:.1f}%)", 
                font=("Helvetica", 14, "bold")
            )
            so_tien_label.pack(side="right", padx=10)
    
    def chuyen_tien_giua_cac_lo(self):
        """Chuyển tiền giữa các lọ"""
        # Tạo cửa sổ dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Chuyển Tiền Giữa Các Lọ")
        dialog.geometry("400x300")

        # Label hướng dẫn
        huong_dan_label = ctk.CTkLabel(
            dialog, 
            text="Nhập thông tin để chuyển tiền giữa các lọ", 
            font=("Helvetica", 14, "bold"),
            wraplength=350
        )
        huong_dan_label.pack(pady=(20, 10))

        # Nhập lọ nguồn
        tu_lo_frame = ctk.CTkFrame(dialog)
        tu_lo_frame.pack(pady=10, padx=20, fill="x")

        tu_lo_label = ctk.CTkLabel(tu_lo_frame, text="Lọ Nguồn:", font=("Helvetica", 12))
        tu_lo_label.pack(side="left", padx=10)

        tu_lo_options = list(self.quan_ly._phuong_phap_sau_lo._lo.keys())
        tu_lo_var = tk.StringVar(dialog)
        tu_lo_var.set(tu_lo_options[0])

        tu_lo_dropdown = ttk.Combobox(tu_lo_frame, textvariable=tu_lo_var, values=tu_lo_options)
        tu_lo_dropdown.pack(side="right", padx=10)

        # Nhập lọ đích
        den_lo_frame = ctk.CTkFrame(dialog)
        den_lo_frame.pack(pady=10, padx=20, fill="x")

        den_lo_label = ctk.CTkLabel(den_lo_frame, text="Lọ Đích:", font=("Helvetica", 12))
        den_lo_label.pack(side="left", padx=10)

        den_lo_var = tk.StringVar(dialog)
        den_lo_var.set(tu_lo_options[0])

        den_lo_dropdown = ttk.Combobox(den_lo_frame, textvariable=den_lo_var, values=tu_lo_options)
        den_lo_dropdown.pack(side="right", padx=10)

        # Nhập số tiền chuyển
        so_tien_frame = ctk.CTkFrame(dialog)
        so_tien_frame.pack(pady=10, padx=20, fill="x")

        so_tien_label = ctk.CTkLabel(so_tien_frame, text="Số Tiền:", font=("Helvetica", 12))
        so_tien_label.pack(side="left", padx=10)

        so_tien_entry = ctk.CTkEntry(so_tien_frame, width=150)
        so_tien_entry.pack(side="right", padx=10)

        def submit_chuyen_tien():
            try:
                # Lấy thông tin từ các entry
                tu_lo = tu_lo_var.get()
                den_lo = den_lo_var.get()
                so_tien = float(so_tien_entry.get())

                # Gọi phương thức chuyển tiền
                self.quan_ly._phuong_phap_sau_lo.chuyen_tien_giua_cac_lo(tu_lo, den_lo, so_tien)
                messagebox.showinfo("Thành Công", "Chuyển tiền giữa các lọ thành công!")
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        submit_button = ctk.CTkButton(dialog, text="Xác Nhận", command=submit_chuyen_tien)
        submit_button.pack(pady=20)

    def run(self):
        """Chạy ứng dụng giao diện"""
        self.root.mainloop()