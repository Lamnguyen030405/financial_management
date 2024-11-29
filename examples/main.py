import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import csv

from src.gui.giao_dien import GiaoDien

def main():
    """
    Hàm chính để khởi chạy ứng dụng
    """
    root = tk.Tk()
    app = GiaoDien(root)
    app.chay()


if __name__ == "__main__":
    main()