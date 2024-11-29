import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import csv

from src.models.tai_khoan import TaiKhoan
from src.models.khoan_vay import KhoanVay
from src.models.giao_dich import GiaoDich
from src.models.danh_muc import DanhMuc
from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh

class GiaoDien:
    def __init__(self, master):
        """
        Khởi tạo giao diện quản lý tài chính
        """
        self.master = master
        master.title("Hệ Thống Quản Lý Tài Chính")
        master.geometry("800x600")

        # Khởi tạo hệ thống quản lý tài chính
        self.quan_ly_tai_chinh = QuanLyTaiChinh()

        # Tạo thanh menu
        self.thanh_menu = tk.Menu(master)
        master.config(menu=self.thanh_menu)

        # Menu Tài Khoản
        self.menu_tai_khoan = tk.Menu(self.thanh_menu, tearoff=0)
        self.thanh_menu.add_cascade(label="Tài Khoản", menu=self.menu_tai_khoan)
        self.menu_tai_khoan.add_command(label="Thêm Tài Khoản", command=self.them_tai_khoan)
        self.menu_tai_khoan.add_command(label="Danh Sách Tài Khoản", command=self.hien_thi_tai_khoan)

        # Menu Giao Dịch
        self.menu_giao_dich = tk.Menu(self.thanh_menu, tearoff=0)
        self.thanh_menu.add_cascade(label="Giao Dịch", menu=self.menu_giao_dich)
        self.menu_giao_dich.add_command(label="Thêm Giao Dịch", command=self.them_giao_dich)
        self.menu_giao_dich.add_command(label="Xem Giao Dịch", command=self.xem_giao_dich)

        # Menu Báo Cáo
        self.menu_bao_cao = tk.Menu(self.thanh_menu, tearoff=0)
        self.thanh_menu.add_cascade(label="Báo Cáo", menu=self.menu_bao_cao)
        self.menu_bao_cao.add_command(label="Báo Cáo Tài Chính", command=self.tao_bao_cao_tai_chinh)
        self.menu_bao_cao.add_command(label="Xuất CSV", command=self.xuat_csv)
        self.menu_bao_cao.add_command(label="Dự Báo Xu Hướng", command=self.du_bao_xu_huong)

        # Menu Quản Lý
        self.menu_quan_ly = tk.Menu(self.thanh_menu, tearoff=0)
        self.thanh_menu.add_cascade(label="Quản Lý", menu=self.menu_quan_ly)
        self.menu_quan_ly.add_command(label="Thêm Khoản Vay", command=self.them_khoan_vay)
        self.menu_quan_ly.add_command(label="Đặt Mục Tiêu Tiết Kiệm", command=self.dat_muc_tieu_tiet_kiem)
        self.menu_quan_ly.add_command(label="Phương Pháp 6 Lỗ", command=self.thiet_lap_phuong_phap_sau_lo)

        # Khu vực trạng thái
        self.label_trang_thai = tk.Label(master, text="Sẵn sàng", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label_trang_thai.pack(side=tk.BOTTOM, fill=tk.X)

    def them_tai_khoan(self):
        """
        Hiển thị dialog thêm tài khoản mới
        """
        id_tai_khoan = simpledialog.askstring("Thêm Tài Khoản", "Nhập ID tài khoản:")
        ten_tai_khoan = simpledialog.askstring("Thêm Tài Khoản", "Nhập tên tài khoản:")
        so_du_ban_dau = simpledialog.askfloat("Thêm Tài Khoản", "Nhập số dư ban đầu:")

        if id_tai_khoan and ten_tai_khoan and so_du_ban_dau is not None:
            tai_khoan_moi = TaiKhoan(id_tai_khoan, ten_tai_khoan, so_du_ban_dau)
            if self.quan_ly_tai_chinh.them_tai_khoan(tai_khoan_moi):
                messagebox.showinfo("Thành Công", "Tài khoản đã được thêm.")
                self.label_trang_thai.config(text=f"Đã thêm tài khoản: {ten_tai_khoan}")
            else:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")

    def hien_thi_tai_khoan(self):
        """
        Hiển thị danh sách tài khoản
        """
        cua_so_tai_khoan = tk.Toplevel(self.master)
        cua_so_tai_khoan.title("Danh Sách Tài Khoản")
        cua_so_tai_khoan.geometry("400x300")

        tree = ttk.Treeview(cua_so_tai_khoan, columns=("ID", "Tên", "Số Dư"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Tên", text="Tên")
        tree.heading("Số Dư", text="Số Dư")

        # Lấy danh sách tài khoản
        # Giả sử phương thức lấy danh sách tài khoản là _tai_khoan
        for tai_khoan in self.quan_ly_tai_chinh._tai_khoan:
            tree.insert("", "end", values=(tai_khoan._id, tai_khoan._ten, tai_khoan.lay_so_du()))

        tree.pack(expand=True, fill='both')

    def them_giao_dich(self):
        """
        Thêm giao dịch mới
        """
        # Kiểm tra xem có tài khoản nào không
        if not self.quan_ly_tai_chinh._tai_khoan:
            messagebox.showerror("Lỗi", "Chưa có tài khoản nào. Vui lòng thêm tài khoản trước.")
            return

        # Dialog chọn tài khoản
        id_tai_khoan = simpledialog.askstring("Chọn Tài Khoản", "Nhập ID tài khoản:")
        
        # Dialog nhập giao dịch
        so_tien = simpledialog.askfloat("Giao Dịch", "Nhập số tiền:")
        loai_giao_dich = simpledialog.askstring("Giao Dịch", "Loại giao dịch (thu nhập/chi tiêu):")
        danh_muc = simpledialog.askstring("Giao Dịch", "Nhập danh mục:")

        if id_tai_khoan and so_tien is not None and loai_giao_dich and danh_muc:
            giao_dich = GiaoDich(id_tai_khoan, so_tien, loai_giao_dich, datetime.now(), danh_muc)
            
            if self.quan_ly_tai_chinh.them_giao_dich(giao_dich):
                messagebox.showinfo("Thành Công", "Giao dịch đã được thêm.")
                self.label_trang_thai.config(text=f"Đã thêm giao dịch: {so_tien} - {loai_giao_dich}")
            else:
                messagebox.showerror("Lỗi", "Không thể thêm giao dịch.")

    def xem_giao_dich(self):
        """
        Xem danh sách giao dịch
        """
        cua_so_giao_dich = tk.Toplevel(self.master)
        cua_so_giao_dich.title("Danh Sách Giao Dịch")
        cua_so_giao_dich.geometry("600x400")

        tree = ttk.Treeview(cua_so_giao_dich, 
                            columns=("Tài Khoản", "Số Tiền", "Loại", "Ngày", "Danh Mục"), 
                            show="headings")
        tree.heading("Tài Khoản", text="Tài Khoản")
        tree.heading("Số Tiền", text="Số Tiền")
        tree.heading("Loại", text="Loại")
        tree.heading("Ngày", text="Ngày")
        tree.heading("Danh Mục", text="Danh Mục")

        for tai_khoan in self.quan_ly_tai_chinh._tai_khoan:
            for giao_dich in tai_khoan.lay_giao_dich():
                tree.insert("", "end", values=(
                    tai_khoan._ten, 
                    giao_dich.lay_so_tien(), 
                    giao_dich.lay_loai(), 
                    giao_dich._ngay, 
                    giao_dich._danh_muc
                ))

        tree.pack(expand=True, fill='both')

    def tao_bao_cao_tai_chinh(self):
        """
        Tạo và hiển thị báo cáo tài chính
        """
        # Chọn khoảng thời gian
        ngay_bat_dau = simpledialog.askstring("Báo Cáo", "Nhập ngày bắt đầu (YYYY-MM-DD):")
        ngay_ket_thuc = simpledialog.askstring("Báo Cáo", "Nhập ngày kết thúc (YYYY-MM-DD):")

        try:
            ngay_bat_dau = datetime.strptime(ngay_bat_dau, "%Y-%m-%d")
            ngay_ket_thuc = datetime.strptime(ngay_ket_thuc, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ.")
            return

        bao_cao = self.quan_ly_tai_chinh.tao_bao_cao_tai_chinh(ngay_bat_dau, ngay_ket_thuc)

        # Hiển thị báo cáo
        cua_so_bao_cao = tk.Toplevel(self.master)
        cua_so_bao_cao.title("Báo Cáo Tài Chính")
        cua_so_bao_cao.geometry("600x400")

        # Tạo text widget để hiển thị báo cáo
        text_bao_cao = tk.Text(cua_so_bao_cao, wrap=tk.WORD)
        text_bao_cao.pack(expand=True, fill='both')

        # Định dạng báo cáo
        text_bao_cao.insert(tk.END, "BÁO CÁO TÀI CHÍNH\n\n")
        text_bao_cao.insert(tk.END, f"Tổng Số Dư: {bao_cao['tong_so_du']}\n")
        text_bao_cao.insert(tk.END, f"Tổng Nợ: {bao_cao['tong_no']}\n\n")

        text_bao_cao.insert(tk.END, "GIAO DỊCH THEO DANH MỤC:\n")
        for danh_muc, chi_tiet in bao_cao['giao_dich_theo_danh_muc'].items():
            text_bao_cao.insert(tk.END, f"{danh_muc}: Tổng Thu {chi_tiet['tong_thu']}, Tổng Chi {chi_tiet['tong_chi']}\n")

    def xuat_csv(self):
        """
        Xuất báo cáo ra file CSV
        """
        try:
            self.quan_ly_tai_chinh.xuat_csv()
            messagebox.showinfo("Xuất CSV", "Báo cáo đã được xuất thành công.")
            self.label_trang_thai.config(text="Đã xuất báo cáo CSV")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất CSV: {str(e)}")

    def du_bao_xu_huong(self):
        """
        Hiển thị dự báo xu hướng tài chính
        """
        du_bao = self.quan_ly_tai_chinh.du_bao_xu_huong_tai_chinh()

        cua_so_du_bao = tk.Toplevel(self.master)
        cua_so_du_bao.title("Dự Báo Xu Hướng Tài Chính")
        cua_so_du_bao.geometry("600x400")

        text_du_bao = tk.Text(cua_so_du_bao, wrap=tk.WORD)
        text_du_bao.pack(expand=True, fill='both')

        text_du_bao.insert(tk.END, "DỰ BÁO XU HƯỚNG TÀI CHÍNH\n\n")

        # Xu hướng chi tiêu
        text_du_bao.insert(tk.END, "XU HƯỚNG CHI TIÊU:\n")
        for danh_muc, chi_tiet in du_bao['xu_huong_chi_tieu'].items():
            text_du_bao.insert(tk.END, f"{danh_muc}: Trung bình {chi_tiet['trung_binh']}, Tổng Chi {chi_tiet['tong_chi']}\n")

        # Dự báo tiết kiệm
        text_du_bao.insert(tk.END, "\nDỰ BÁO TIẾT KIỆM:\n")
        for tai_khoan, chi_tiet in du_bao['du_bao_tiet_kiem'].items():
            text_du_bao.insert(tk.END, f"Tài Khoản {tai_khoan}: Mục Tiêu {chi_tiet['muc_tieu']}, Số Dư Hiện Tại {chi_tiet['so_du_hien_tai']}\n")

        # Cảnh báo nợ
        text_du_bao.insert(tk.END, "\nCẢNH BÁO NỢ:\n")
        for khoan_vay in du_bao['canh_bao_no']:
            text_du_bao.insert(tk.END, f"ID: {khoan_vay['id']}, Số Tiền Còn Lại: {khoan_vay['so_tien_con_lai']}, "
                                        f"Người Cho Vay: {khoan_vay['nguoi_cho_vay']}, "
                                        f"Ngày Đến Hạn: {khoan_vay['ngay_den_han']}\n")

    def them_khoan_vay(self):
        """
        Thêm khoản vay mới
        """
        id_khoan_vay = simpledialog.askstring("Thêm Khoản Vay", "Nhập ID khoản vay:")
        so_tien_vay = simpledialog.askfloat("Thêm Khoản Vay", "Nhập số tiền vay:")
        nguoi_cho_vay = simpledialog.askstring("Thêm Khoản Vay", "Nhập tên người cho vay:")
        
        # Chọn ngày đến hạn
        ngay_den_han_str = simpledialog.askstring("Thêm Khoản Vay", "Nhập ngày đến hạn (YYYY-MM-DD):")
        
        try:
            ngay_den_han = datetime.strptime(ngay_den_han_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ.")
            return

        if id_khoan_vay and so_tien_vay is not None and nguoi_cho_vay:
            khoan_vay_moi = KhoanVay(id_khoan_vay, so_tien_vay, nguoi_cho_vay, ngay_den_han)
            
            if self.quan_ly_tai_chinh.them_khoan_vay(khoan_vay_moi):
                messagebox.showinfo("Thành Công", "Khoản vay đã được thêm.")
                self.label_trang_thai.config(text=f"Đã thêm khoản vay: {id_khoan_vay}")
            else:
                messagebox.showerror("Lỗi", "Khoản vay đã tồn tại.")

    def dat_muc_tieu_tiet_kiem(self):
        """
        Đặt mục tiêu tiết kiệm cho tài khoản
        """
        # Kiểm tra xem có tài khoản nào không
        if not self.quan_ly_tai_chinh._tai_khoan:
            messagebox.showerror("Lỗi", "Chưa có tài khoản nào. Vui lòng thêm tài khoản trước.")
            return

        # Chọn tài khoản
        id_tai_khoan = simpledialog.askstring("Đặt Mục Tiêu Tiết Kiệm", "Nhập ID tài khoản:")
        so_tien_muc_tieu = simpledialog.askfloat("Đặt Mục Tiêu Tiết Kiệm", "Nhập số tiền mục tiêu:")

        if id_tai_khoan and so_tien_muc_tieu is not None:
            if self.quan_ly_tai_chinh.dat_muc_tieu_tiet_kiem(id_tai_khoan, so_tien_muc_tieu):
                messagebox.showinfo("Thành Công", "Mục tiêu tiết kiệm đã được đặt.")
                self.label_trang_thai.config(text=f"Đã đặt mục tiêu tiết kiệm cho tài khoản: {id_tai_khoan}")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy tài khoản.")

    def thiet_lap_phuong_phap_sau_lo(self):
        """
        Thiết lập phương pháp 6 lỗ
        """
        tong_thu_nhap = simpledialog.askfloat("Phương Pháp 6 Lỗ", "Nhập tổng thu nhập:")

        if tong_thu_nhap is not None:
            self.quan_ly_tai_chinh.thiet_lap_phuong_phap_sau_lo(tong_thu_nhap)
            messagebox.showinfo("Thành Công", "Đã thiết lập phương pháp 6 lỗ.")
            self.label_trang_thai.config(text="Đã thiết lập phương pháp quản lý tài chính 6 lỗ")

    def chay(self):
        """
        Chạy ứng dụng giao diện
        """
        self.master.mainloop()
