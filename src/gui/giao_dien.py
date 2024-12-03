import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh
from src.models.tai_khoan import TaiKhoan
from src.models.giao_dich import GiaoDich
from src.models.khoan_vay import KhoanVay
from src.models.danh_muc import DanhMuc

class QuanLyTaiChinhGUI:
    def __init__(self):
        # Cấu hình giao diện
        ctk.set_appearance_mode("system")  # Chế độ giao diện hệ thống
        ctk.set_default_color_theme("blue")  # Chủ đề màu

        # Cửa sổ chính
        self.root = ctk.CTk()
        self.root.title("Quản Lý Tài Chính")
        self.root.geometry("800x600")

        # Quản lý tài chính backend
        self.quan_ly = QuanLyTaiChinh()
        self.quan_ly.nhap_csv()  # Nạp dữ liệu từ CSV

        # Tạo frame chính
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Tiêu đề
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="HỆ THỐNG QUẢN LÝ TÀI CHÍNH", 
            font=("Helvetica", 20, "bold")
        )
        self.title_label.pack(pady=20)

        # Tạo các nút chức năng
        self.create_menu_buttons()

    def create_menu_buttons(self):
        """Tạo các nút chức năng chính"""
        # Frame nút
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(padx=20, pady=10, fill="x")

        # Nhóm nút Tài Khoản
        tai_khoan_frame = ctk.CTkFrame(button_frame)
        tai_khoan_frame.pack(side="left", padx=10, expand=True, fill="x")
        
        ctk.CTkLabel(tai_khoan_frame, text="Tài Khoản", font=("Helvetica", 16, "bold")).pack(pady=10)
        ctk.CTkButton(tai_khoan_frame, text="Thêm Tài Khoản", command=self.them_tai_khoan).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(tai_khoan_frame, text="Xóa Tài Khoản", command=self.xoa_tai_khoan).pack(pady=5, padx=10, fill="x")

        # Nhóm nút Giao Dịch
        giao_dich_frame = ctk.CTkFrame(button_frame)
        giao_dich_frame.pack(side="left", padx=10, expand=True, fill="x")
        
        ctk.CTkLabel(giao_dich_frame, text="Giao Dịch", font=("Helvetica", 16, "bold")).pack(pady=10)
        ctk.CTkButton(giao_dich_frame, text="Thêm Giao Dịch", command=self.them_giao_dich).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(giao_dich_frame, text="Xóa Giao Dịch", command=self.xoa_giao_dich).pack(pady=5, padx=10, fill="x")

        # Nhóm nút Khoản Vay
        khoan_vay_frame = ctk.CTkFrame(button_frame)
        khoan_vay_frame.pack(side="left", padx=10, expand=True, fill="x")
        
        ctk.CTkLabel(khoan_vay_frame, text="Khoản Vay", font=("Helvetica", 16, "bold")).pack(pady=10)
        ctk.CTkButton(khoan_vay_frame, text="Thêm Khoản Vay", command=self.them_khoan_vay).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(khoan_vay_frame, text="Xóa Khoản Vay", command=self.xoa_khoan_vay).pack(pady=5, padx=10, fill="x")

        # Các nút chức năng khác
        action_frame = ctk.CTkFrame(self.main_frame)
        action_frame.pack(padx=20, pady=10, fill="x")

        action_buttons = [
            ("Tạo Báo Cáo", self.tao_bao_cao),
            ("Dự Báo Xu Hướng", self.du_bao_xu_huong),
            ("Thống Kê Tổng Quát", self.thong_ke_tong_quat),
            ("Xuất CSV", self.xuat_csv),
            ("Thoát", self.root.quit)
        ]

        for text, command in action_buttons:
            ctk.CTkButton(action_frame, text=text, command=command).pack(side="left", padx=10, expand=True, fill="x")

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

    def them_giao_dich(self):
        """Thêm giao dịch mới"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Thêm Giao Dịch")
        dialog.geometry("400x600")

        entries = [
            ("ID Giao Dịch", "id"),
            ("ID Tài Khoản", "id_tai_khoan"),
            ("Số Tiền", "so_tien"),
            ("Loại Giao Dịch", "loai"),
            ("Danh Mục", "danh_muc"),
            ("Ngày", "ngay"),
            ("Ghi Chú", "ghi_chu")
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
                giao_dich = GiaoDich(
                    entry_widgets['id'].get(),
                    entry_widgets['id_tai_khoan'].get(),
                    float(entry_widgets['so_tien'].get()),
                    entry_widgets['loai'].get(),
                    entry_widgets['danh_muc'].get(),
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

    def tao_bao_cao(self):
        """Tạo báo cáo tài chính"""
        try:
            ngay_bat_dau = datetime.strptime(
                simpledialog.askstring("Báo Cáo", "Nhập ngày bắt đầu (YYYY-MM-DD):"), 
                "%Y-%m-%d"
            )
            ngay_ket_thuc = datetime.strptime(
                simpledialog.askstring("Báo Cáo", "Nhập ngày kết thúc (YYYY-MM-DD):"), 
                "%Y-%m-%d"
            )
            
            bao_cao = self.quan_ly.tao_bao_cao_tai_chinh(ngay_bat_dau, ngay_ket_thuc)
            messagebox.showinfo("Báo Cáo Tài Chính", str(bao_cao))
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ!")

    def du_bao_xu_huong(self):
        """Dự báo xu hướng tài chính"""
        du_bao = self.quan_ly.du_bao_xu_huong_tai_chinh()
        messagebox.showinfo("Dự Báo Xu Hướng", str(du_bao))

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

    def xuat_csv(self):
        """Xuất dữ liệu ra CSV"""
        self.quan_ly.xuat_csv()
        messagebox.showinfo("Xuất CSV", "Xuất dữ liệu CSV thành công!")

    def run(self):
        """Chạy ứng dụng giao diện"""
        self.root.mainloop()