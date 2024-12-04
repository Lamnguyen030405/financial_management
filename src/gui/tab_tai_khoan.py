from tkinter import messagebox
import customtkinter as ctk
from CTkTable import CTkTable as CTkTable

from src.gui.hop_thoai import HopThoai
from src.models.tai_khoan import TaiKhoan
from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh

from .tab_chung import TabCoBan

class TabTaiKhoan(TabCoBan):
    def __init__(self, tabview: ctk.CTkTabview, name: str, manager: QuanLyTaiChinh):
        actions = {
            "add_btn": ("Thêm tài khoản", self.them_tai_khoan_click),
            "del_btn": ("Xóa tài khoản", self.xoa_tai_khoan_click),
        }
        super().__init__(tabview, name, actions)
        self.buttons["del_btn"].configure(state="disabled")
        self.manager = manager
        table_data = [["ID", "Tên tài khoản", "Số Dư", "Loại tài khoản"]]
        for tai_khoan in manager._tai_khoan:
            table_data.append([tai_khoan._id, tai_khoan._ten, tai_khoan._so_du, tai_khoan._loai])
        self.create_table(table_data, self.table_tai_khoan_click)
        self.add_dialog = None

    def them_tai_khoan_click(self):
        # Tạo cửa sổ dialog
        def submit(entries: list[str]):
            try:
                tai_khoan = TaiKhoan(*[t(v) for v, t in zip(entries, [str, str, float, str])])
                if self.manager.them_tai_khoan(tai_khoan):
                    self.table.add_row([tai_khoan._id, tai_khoan._ten, tai_khoan._so_du, tai_khoan._loai])
                    return True
                else:
                    messagebox.showerror("Lỗi", "ID tài khoản đã tồn tại!")
                    return False
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số tiền!")
                return False
        if self.add_dialog is None or not self.add_dialog.dialog.winfo_exists():
            self.add_dialog = HopThoai(self.tabview, "Thêm Tài Khoản", ["ID Tài Khoản", "Tên Tài Khoản", "Số Dư", "Loại Tài Khoản"], ("Thêm", submit))

    def xoa_tai_khoan_click(self):
        selected = self.table.get_selected_row()["row_index"]
        id = self.table.get_row(selected)[0]
        self.manager.xoa_tai_khoan(str(id))
        self.table.deselect_row(selected)
        self.table.delete_row(selected)
        self.buttons["del_btn"].configure(state="disabled")

    def table_tai_khoan_click(self, args):
        selected = self.base_on_table_click(args)
        if selected > 0:
            self.buttons["del_btn"].configure(state="normal")
        else:
            self.buttons["del_btn"].configure(state="disabled")