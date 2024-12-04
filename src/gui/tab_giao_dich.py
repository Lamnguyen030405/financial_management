from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk
from CTkTable import CTkTable as CTkTable

from src.gui.hop_thoai import HopThoai
from src.models.giao_dich import GiaoDich
from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh

from .tab_chung import TabCoBan

class TabGiaoDich(TabCoBan):
    def __init__(self, tabview: ctk.CTkTabview, name: str, manager: QuanLyTaiChinh):
        actions = {
            "add_btn": ("Thêm Giao Dịch", self.them_giao_dich_click),
            "del_btn": ("Xóa Giao Dịch", self.xoa_giao_dich_click),
            "upd_btn": ("Cập Nhật Giao Dịch", self.cap_nhat_giao_dich_click)
        }
        super().__init__(tabview, name, actions)
        self.buttons["del_btn"].configure(state="disabled")
        self.buttons["upd_btn"].configure(state="disabled")
        self.manager = manager
        table_data = [["ID", "Tài khoản", "Số tiền", "Loại giao dịch", "Danh mục", "Thời gian", "Ghi chú"]]
        for giao_dich, tai_khoan in [(giao_dich, tai_khoan._ten) for tai_khoan in manager._tai_khoan for giao_dich in tai_khoan._giao_dich]:
            table_data.append([giao_dich._id, tai_khoan, giao_dich._so_tien, giao_dich._loai, giao_dich._danh_muc, giao_dich._ngay, giao_dich._ghi_chu])
        self.create_table(table_data, self.table_giao_dich_click)
        self.add_dialog = None
        self.upd_dialog = None

    def them_giao_dich_click(self):
        # Tạo cửa sổ dialog
        def submit(entries: list[str]):
            try:
                giao_dich = GiaoDich(*[t(v) for v, t in zip(entries, [str, str, float, str, str, datetime, str])])
                if self.manager.them_giao_dich(giao_dich):
                    tai_khoan = next((tai_khoan._ten for tai_khoan in self.manager._tai_khoan if tai_khoan._id == entries[1]))
                    self.table.add_row([giao_dich._id, tai_khoan, giao_dich._so_tien, giao_dich._loai, giao_dich._danh_muc, giao_dich._ngay, giao_dich._ghi_chu])
                    return True
                else:
                    messagebox.showerror("Lỗi", "ID tài khoản đã tồn tại!")
                    return False
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số tiền!")
                return False
        if self.add_dialog is None or not self.add_dialog.dialog.winfo_exists():
            self.add_dialog = HopThoai(self.tabview, "Thêm Giao Dịch", ["ID Giao Dịch", "ID Tài khoản" "Số tiền", "Loại giao dịch", "Danh mục", "Thời gian", "Ghi chú"], ("Thêm", submit))

    def xoa_giao_dich_click(self):
        selected = self.table.get_selected_row()["row_index"]
        id = self.table.get_row(selected)[0]
        acc_id = next((tai_khoan._id for tai_khoan in self.manager._tai_khoan for giao_dich in tai_khoan._giao_dich if giao_dich._id == id))
        self.manager.xoa_giao_dich(id, acc_id)
        self.table.deselect_row(selected)
        self.table.delete_row(selected)
        self.buttons["del_btn"].configure(state="disabled")
        self.buttons["upd_btn"].configure(state="disabled")

    def cap_nhat_giao_dich_click(self):
        def submit(entries: list[str]):
            try:
                giao_dich = GiaoDich(*[t(v) for v, t in zip(entries, [str, str, float, str, str, datetime.fromisoformat, str])])
                if self.manager.cap_nhat_giao_dich(giao_dich):
                    tai_khoan = next((tai_khoan._ten for tai_khoan in self.manager._tai_khoan if tai_khoan._id == entries[1]))
                    upd_row = self.table.get_selected_row()["row_index"]
                    for col, info in zip(range(self.table.columns), [giao_dich._id, tai_khoan, giao_dich._so_tien, giao_dich._loai, giao_dich._danh_muc, giao_dich._ngay, giao_dich._ghi_chu]):
                        self.table.insert(upd_row, col, info)
                    return True
                else:
                    messagebox.showerror("Lỗi", "ID tài khoản đã tồn tại!")
                    return False
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số tiền!")
                return False
        if self.upd_dialog is None or not self.upd_dialog.dialog.winfo_exists():
            self.upd_dialog = HopThoai(self.tabview, "Cập nhật Giao Dịch", ["ID Giao Dịch", "ID Tài khoản", "Số tiền", "Loại giao dịch", "Danh mục", "Thời gian", "Ghi chú"], ("Cập nhật", submit))
            selected = self.table.get_selected_row()["row_index"]
            gd = self.table.get_row(selected).copy()
            id = gd[0]
            gd[1] = next((tai_khoan._id for tai_khoan in self.manager._tai_khoan for giao_dich in tai_khoan._giao_dich if giao_dich._id == id))
            self.upd_dialog.fill_entries(gd)

    def table_giao_dich_click(self, args):
        selected = self.base_on_table_click(args)
        if selected > 0:
            self.buttons["del_btn"].configure(state="normal")
            self.buttons["upd_btn"].configure(state="normal")
        else:
            self.buttons["del_btn"].configure(state="disabled")
            self.buttons["upd_btn"].configure(state="disabled")