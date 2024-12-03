from datetime import datetime
from src.managers.quan_ly_tai_chinh import QuanLyTaiChinh
from src.models.tai_khoan import TaiKhoan
from src.models.giao_dich import GiaoDich
from src.models.khoan_vay import KhoanVay
from src.models.danh_muc import DanhMuc
from src.models.phuong_phap_sau_lo import PhuongPhapSauLo

# Tạo đối tượng quản lý tài chính
quan_ly = QuanLyTaiChinh()

def hien_thi_menu():
    print("\n=== MENU QUẢN LÝ TÀI CHÍNH ===")
    print("1. Quản lý Tài Khoản")
    print("   11. Thêm tài khoản")
    print("   12. Xóa tài khoản")
    print("2. Quản lý Giao Dịch")
    print("   21. Thêm giao dịch")
    print("   22. Xóa giao dịch")
    print("3. Quản lý Khoản Vay")
    print("   31. Thêm khoản vay")
    print("   32. Xóa khoản vay")
    print("4. Quản lý Danh Mục")
    print("   41. Thêm danh mục")
    print("   42. Xóa danh mục")
    print("5. Báo Cáo và Phân Tích")
    print("   51. Tạo báo cáo tài chính")
    print("   52. Dự báo xu hướng tài chính")
    print("   53. Lấy thống kê tổng quát")
    print("   54. Đặt mục tiêu tiết kiệm")
    print("6. Quản lý Phương Pháp Sáu Lọ")
    print("   61. Thiết lập phương pháp sáu lọ")
    print("   62. Xem phân bổ sáu lọ")
    print("7. Quản lý Dữ Liệu")
    print("   71. Xuất dữ liệu CSV")
    print("8. Thoát")

def chon_menu():
    try:
        return int(input("Chọn chức năng: "))
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
    loai = input("Nhập loại giao dịch (Thu nhập/Chi tiêu): ")
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
    nguoi_vay = input("Nhập tên người vay: ")
    lai_suat = float(input("Nhập lãi suất (%): "))
    ngay_bat_dau = datetime.strptime(input("Nhập ngày bắt đầu (YYYY-MM-DD): "), "%Y-%m-%d")
    ngay_den_han = datetime.strptime(input("Nhập ngày đến hạn (YYYY-MM-DD): "), "%Y-%m-%d")
    khoan_vay = KhoanVay(
        id_khoan_vay, 
        so_tien, 
        nguoi_cho_vay, 
        nguoi_vay, 
        lai_suat, 
        ngay_bat_dau, 
        ngay_den_han,
    )
    if quan_ly.them_khoan_vay(khoan_vay):
        print("Thêm khoản vay thành công!")
    else:
        print("ID khoản vay đã tồn tại!")

def xoa_khoan_vay():
    id_khoan_vay = input("Nhập ID khoản vay cần xóa: ")
    quan_ly.xoa_khoan_vay(id_khoan_vay)
    print("Đã xóa khoản vay.")

def them_danh_muc():
    id_danh_muc = input("Nhập ID danh mục: ")
    ten_danh_muc = input("Nhập tên danh mục: ")
    loai_danh_muc = input("Nhập loại danh mục: ")
    mo_ta_danh_muc = input("Nhập mô tả danh mục: ")
    
    danh_muc = DanhMuc(id_danh_muc, ten_danh_muc, loai_danh_muc, mo_ta_danh_muc)
    if quan_ly.them_danh_muc(danh_muc):
        print("Thêm danh mục thành công!")
    else:
        print("ID danh mục đã tồn tại!")

def xoa_danh_muc():
    id_danh_muc = input("Nhập ID danh mục cần xóa: ")
    quan_ly.xoa_danh_muc(id_danh_muc)
    print("Đã xóa danh mục.")

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

def thiet_lap_sau_lo():
    tong_thu_nhap = quan_ly.tinh_tong_thu_nhap()
    quan_ly.thiet_lap_phuong_phap_sau_lo(tong_thu_nhap)
    print("Thiết lập phương pháp sáu lọ thành công!")

def xem_phan_bo_sau_lo():
    if quan_ly._phuong_phap_sau_lo:
        print("Phân bổ sáu lọ:")
        for ten_lo, so_tien in quan_ly._phuong_phap_sau_lo._lo.items():
            print(f"{ten_lo}: {so_tien}")
    else:
        print("Chưa thiết lập phương pháp sáu lọ. Vui lòng thiết lập trước.")

def thong_ke_tong_quat():
    thong_ke = quan_ly.lay_thong_ke_tong_quat()
    print("Thống kê tổng quát:")
    for key, value in thong_ke.items():
        print(f"{key}: {value}")

def main():
    quan_ly.nhap_csv()
    while True:
        hien_thi_menu()
        lua_chon = chon_menu()
        
        # Tài khoản
        if lua_chon == 11:
            them_tai_khoan()
        elif lua_chon == 12:
            xoa_tai_khoan()
        
        # Giao dịch
        elif lua_chon == 21:
            them_giao_dich()
        elif lua_chon == 22:
            xoa_giao_dich()
        
        # Khoản vay
        elif lua_chon == 31:
            them_khoan_vay()
        elif lua_chon == 32:
            xoa_khoan_vay()
        
        # Danh mục
        elif lua_chon == 41:
            them_danh_muc()
        elif lua_chon == 42:
            xoa_danh_muc()
        
        # Báo cáo và phân tích
        elif lua_chon == 51:
            tao_bao_cao()
        elif lua_chon == 52:
            du_bao_xu_huong()
        elif lua_chon == 53:
            thong_ke_tong_quat()
        elif lua_chon == 54:
            dat_muc_tieu_tiet_kiem()
        
        # Phương pháp sáu lọ
        elif lua_chon == 61:
            thiet_lap_sau_lo()
        elif lua_chon == 62:
            xem_phan_bo_sau_lo()
        
        # Quản lý dữ liệu
        elif lua_chon == 71:
            quan_ly.xuat_csv()
            print("Xuất dữ liệu CSV thành công!")
        
        # Thoát
        elif lua_chon == 8:    
            print("Thoát chương trình!")
            break
        
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

if __name__ == "__main__":
    main()