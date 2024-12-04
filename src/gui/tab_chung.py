from typing import Callable
from CTkTable import CTkTable
import customtkinter as ctk

from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh

class TabCoBan:
    def __init__(self, tabview: ctk.CTkTabview, name: str, actions: dict[str, tuple[str, Callable | None]] = {}, **kwargs):
        self.name = name
        self.tabview = tabview
        self.tab = tabview.tab(name)
        self.buttons : dict[str, ctk.CTkButton] = {}

        # Tạo tiêu đề cho tab
        title_label = ctk.CTkLabel(self.tab, text=name, font=("Helvetica", 20, "bold"))
        title_label.pack(anchor=ctk.W, padx=20,pady=20)
        # Tạo các nút
        button_frame = ctk.CTkFrame(self.tab, fg_color="transparent")
        for id, (text, command) in actions.items():
            button = ctk.CTkButton(button_frame, text=text, width=150, height=40, command=command)
            button.pack(side="left", padx=15)
            self.buttons.setdefault(id, button)
        button_frame.pack(anchor='w')
        # Tạo bảng
        self.table : None | CTkTable

    def create_table(self, table_data, onclick: Callable | None = None):
        if onclick is None:
            onclick = self.base_on_table_click
        table_frame = ctk.CTkScrollableFrame(self.tab, fg_color="transparent")
        table_frame.pack(fill="both", padx=30, pady=20, expand=True)
        self.table = CTkTable(master=table_frame, values=table_data, header_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"][0 if ctk.get_appearance_mode() == "Light" else 1], command=onclick)
        self.table.pack(expand=True, fill="both")

    def base_on_table_click(self, args):
        selected = self.table.get_selected_row()["row_index"]
        if selected: self.table.deselect_row(selected)
        selected = args["row"]
        self.table.select_row(selected)
        return selected
        