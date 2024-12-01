from datetime import datetime
from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh
from src.models.tai_khoan import TaiKhoan
from src.models.giao_dich import GiaoDich
from src.models.khoan_vay import KhoanVay
from src.models.danh_muc import DanhMuc

# Tạo đối tượng quản lý tài chính
quan_ly = QuanLyTaiChinh()

def hien_thi_menu():
    print("\n=== MENU ===")
    print("1. Thêm tài khoản")
    print("2. Xóa tài khoản")
    print("3. Thêm giao dịch")
    print("4. Thêm khoản vay")
    print("5. Tạo báo cáo tài chính")
    print("6. Đặt mục tiêu tiết kiệm")
    print("7. Dự báo xu hướng tài chính")
    print("8. Thoát")

def chon_menu():
    try:
        return int(input("Chọn chức năng (1-8): "))
    except ValueError:
        return 0

def them_tai_khoan():
    id_tai_khoan = input("Nhập ID tài khoản: ")
    ten_tai_khoan = input("Nhập tên tài khoản: ")
    so_du = float(input("Nhập số dư ban đầu: "))
    loai_tai_khoan = input("Nhập loại tài khoản: ")
    tai_khoan = TaiKhoan(id_tai_khoan, ten_tai_khoan, so_du, loai_tai_khoan)
    if quan_ly.them_tai_khoan(tai_khoan):
        print("Thêm tài khoản thành công!")
    else:
        print("ID tài khoản đã tồn tại!")

def xoa_tai_khoan():
    id_tai_khoan = input("Nhập ID tài khoản cần xóa: ")
    quan_ly.xoa_tai_khoan(id_tai_khoan)
    print("Đã xóa tài khoản.")
    
def xoa_giao_dich():
    id_tai_khoan = input("Nhập ID tài khoản của giao dịch cần xóa: ")
    id_giao_dich = input("Nhập ID của giao dịch cần xóa: ")
    quan_ly.xoa_giao_dich(id_tai_khoan, id_giao_dich)
    print("Đã xóa giao dịch.")

def them_giao_dich():
    id = input("Nhập ID giao dịch: ")
    id_tai_khoan = input("Nhập ID tài khoản: ")
    so_tien = float(input("Nhập số tiền: "))
    loai = input("Nhập loại giao dịch (thu nhập/chi tiêu): ")
    ngay = datetime.strptime(input("Nhập ngày (YYYY-MM-DD): "), "%Y-%m-%d")
    danh_muc = input("Nhập danh mục: ")
    ghi_chu = input("Nhập ghi chú: ")
    giao_dich = GiaoDich(id, id_tai_khoan, so_tien, loai, danh_muc, ngay, ghi_chu)
    if quan_ly.them_giao_dich(giao_dich):
        print("Thêm giao dịch thành công!")
    else:
        print("Không tìm thấy tài khoản.")

def them_khoan_vay():
    id_khoan_vay = input("Nhập ID khoản vay: ")
    nguoi_cho_vay = input("Nhập tên người cho vay: ")
    so_tien = float(input("Nhập số tiền vay: "))
    ngay_den_han = datetime.strptime(input("Nhập ngày đến hạn (YYYY-MM-DD): "), "%Y-%m-%d")
    khoan_vay = KhoanVay(id_khoan_vay, nguoi_cho_vay, so_tien, ngay_den_han)
    if quan_ly.them_khoan_vay(khoan_vay):
        print("Thêm khoản vay thành công!")
    else:
        print("ID khoản vay đã tồn tại!")

def tao_bao_cao():
    ngay_bat_dau = datetime.strptime(input("Nhập ngày bắt đầu (YYYY-MM-DD): "), "%Y-%m-%d")
    ngay_ket_thuc = datetime.strptime(input("Nhập ngày kết thúc (YYYY-MM-DD): "), "%Y-%m-%d")
    bao_cao = quan_ly.tao_bao_cao_tai_chinh(ngay_bat_dau, ngay_ket_thuc)
    print("Báo cáo tài chính:", bao_cao)

def dat_muc_tieu_tiet_kiem():
    id_tai_khoan = input("Nhập ID tài khoản: ")
    so_tien = float(input("Nhập số tiền mục tiêu: "))
    if quan_ly.dat_muc_tieu_tiet_kiem(id_tai_khoan, so_tien):
        print("Đặt mục tiêu tiết kiệm thành công!")
    else:
        print("Không tìm thấy tài khoản.")

def du_bao_xu_huong():
    du_bao = quan_ly.du_bao_xu_huong_tai_chinh()
    print("Dự báo xu hướng tài chính:", du_bao)
    


def main():
    quan_ly.nhap_csv()
    while True:
        hien_thi_menu()
        lua_chon = chon_menu()
        if lua_chon == 1:
            them_tai_khoan()
        elif lua_chon == 2:
            xoa_tai_khoan()
        elif lua_chon == 3:
            them_giao_dich()
        elif lua_chon == 4:
            xoa_giao_dich()
        elif lua_chon == 5:
            quan_ly.xuat_csv()
        elif lua_chon == 6:
            quan_ly.nhap_csv()
        elif lua_chon == 7:    
            print("Thoát chương trình!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

if __name__ == "__main__":
    main()
