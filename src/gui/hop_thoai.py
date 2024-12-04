import customtkinter as ctk
from typing import Callable


class HopThoai:
    def __init__(self, master, title: str | None, entries: list[str], confirm: tuple[str, Callable[[list[str]], bool]] | None = None, cancel: tuple[str, Callable[[list[str]], bool]] | None = None):
        self.dialog = ctk.CTkToplevel(master)
        w = 450
        h = 600
        self.dialog.geometry(f"{w}x{h}")
        self.dialog.title(title or "Hộp thoại")
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        self.dialog.wm_attributes("-topmost", True)
        self.dialog.wait_visibility()
        self.dialog.grab_set()
        self.dialog.resizable(0, 0)
        self.entries: list[ctk.CTkEntry] = []
        self.confirm: tuple[str, Callable[[list[str]], bool] | None] = confirm or ("Ok", None)
        self.cancel: tuple[str, Callable[[list[str]], bool] | None] = cancel or ("", None)
        entry_width = 300
        entry_pad = w // 2 - entry_width // 2
        for entry in entries:
            ctk.CTkLabel(master=self.dialog, text=entry, justify="left", compound="left").pack(anchor='w', padx=(entry_pad, 0), pady=(15, 0))
            entry_ctrl = ctk.CTkEntry(master=self.dialog, width=entry_width, border_width=1)
            entry_ctrl.pack(anchor='w', padx=(entry_pad, 0))
            self.entries.append(entry_ctrl)
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        ctk.CTkButton(button_frame, text=self.confirm[0], height=40, command=self.on_confirm).pack(expand=True, side='left', fill="x", padx=8)
        if len(self.cancel[0]) != 0:
            ctk.CTkButton(button_frame, text=self.cancel[0], height=40, command=self.on_cancel).pack(expand=True, side='right', fill="x", padx=8)
        button_frame.pack(padx=entry_pad - 16, fill="x", pady=(25, 0))

    def on_close(self):
        self.dialog.grab_release()
        self.dialog.destroy()

    def on_confirm(self):
        if self.confirm[1] is not None:
            if not self.confirm[1]([entry.get() for entry in self.entries]):
                return
        self.on_close()

    def on_cancel(self):
        if self.cancel[1] is not None:
            if not self.cancel[1]([entry.get() for entry in self.entries]):
                return
        self.on_close()
    
    def fill_entries(self, data: list[str]):
        for entry, content in zip(self.entries, data):
            entry.delete(0, ctk.END)
            entry.insert(0, content)