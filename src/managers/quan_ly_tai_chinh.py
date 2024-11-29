from datetime import datetime
from typing import List
from csv import writer
from src.models.tai_khoan import TaiKhoan
from src.models.khoan_vay import KhoanVay
from src.models.giao_dich import GiaoDich
from src.models.danh_muc import DanhMuc
from src.models.phuong_phap_sau_lo import PhuongPhapSauLo

class QuanLyTaiChinh:
    def __init__(self):
        """
        Khoi tao quan ly tai chinh voi danh sach tai khoan, khoan vay va danh muc trong
        """
        self._tai_khoan: List[TaiKhoan] = []
        self._khoan_vay: List[KhoanVay] = []
        self._danh_muc: List[DanhMuc] = []
        self._phuong_phap_sau_lo = None
        self._muc_tieu_tiet_kiem = {}

    def them_tai_khoan(self, tai_khoan: TaiKhoan):
        """
        Them mot tai khoan moi vao he thong
        """
        for tk in self._tai_khoan:
            if tk._id == tai_khoan._id:
                return False
        self._tai_khoan.append(tai_khoan)
        return True

    def xoa_tai_khoan(self, id_tai_khoan: str):
        """
        Xoa tai khoan theo ID
        """
        self._tai_khoan = [tk for tk in self._tai_khoan if tk._id != id_tai_khoan]

    def them_giao_dich(self, giao_dich: GiaoDich):
        """
        Them mot giao dich moi vao tai khoan
        """
        for tai_khoan in self._tai_khoan:
            if tai_khoan._id == giao_dich._id_tai_khoan:
                tai_khoan.them_giao_dich(giao_dich)
                tai_khoan.cap_nhat_so_du()
                return True
        return False

    def them_khoan_vay(self, khoan_vay: KhoanVay):
        """
        Them mot khoan vay moi vao he thong
        """
        for kv in self._khoan_vay:
            if kv._id == khoan_vay._id:
                return False
        self._khoan_vay.append(khoan_vay)
        return True

    def tao_bao_cao_tai_chinh(self, ngay_bat_dau: datetime, ngay_ket_thuc: datetime) -> dict:
        """
        Tao bao cao tai chinh trong khoang thoi gian
        """
        bao_cao = {
            "tong_so_du": sum(tk.lay_so_du() for tk in self._tai_khoan),
            "tong_no": sum(kv.lay_so_tien_con_lai() for kv in self._khoan_vay),
            "giao_dich_theo_danh_muc": {},
            "chi_tiet_tai_khoan": []
        }
        
        # Chi tiet giao dich theo danh muc trong khoang thoi gian
        for tai_khoan in self._tai_khoan:
            chi_tiet_tai_khoan = {
                "id": tai_khoan._id,
                "ten": tai_khoan._ten,
                "so_du": tai_khoan.lay_so_du(),
                "giao_dich": []
            }
            
            for giao_dich in tai_khoan.lay_giao_dich():
                if ngay_bat_dau <= giao_dich._ngay <= ngay_ket_thuc:
                    chi_tiet_tai_khoan["giao_dich"].append({
                        "so_tien": giao_dich.lay_so_tien(),
                        "loai": giao_dich.lay_loai(),
                        "ngay": giao_dich._ngay,
                        "danh_muc": giao_dich._danh_muc
                    })
                    
                    # Thong ke giao dich theo danh muc
                    if giao_dich._danh_muc not in bao_cao["giao_dich_theo_danh_muc"]:
                        bao_cao["giao_dich_theo_danh_muc"][giao_dich._danh_muc] = {
                            "tong_thu": 0,
                            "tong_chi": 0
                        }
                    
                    if giao_dich.lay_loai() == "thu nhập":
                        bao_cao["giao_dich_theo_danh_muc"][giao_dich._danh_muc]["tong_thu"] += giao_dich.lay_so_tien()
                    elif giao_dich.lay_loai() == "chi tiêu":
                        bao_cao["giao_dich_theo_danh_muc"][giao_dich._danh_muc]["tong_chi"] += giao_dich.lay_so_tien()
            
            bao_cao["chi_tiet_tai_khoan"].append(chi_tiet_tai_khoan)
        
        return bao_cao

    def xuat_csv(self, duong_dan: str = "bao_cao_tai_chinh.csv"):
        """
        Xuat du lieu tai chinh ra file CSV
        """
        with open(duong_dan, 'w', newline='', encoding='utf-8') as file:
            csv_writer = writer(file)
            
            # Header
            csv_writer.writerow([
                'Tai Khoan', 'So Du', 'Tong Thu', 'Tong Chi', 
                'Danh Muc', 'So Tien', 'Ngay', 'Loai'
            ])
            
            for tai_khoan in self._tai_khoan:
                tong_thu = sum(gd.lay_so_tien() for gd in tai_khoan.lay_giao_dich() if gd.lay_loai() == "thu nhập")
                tong_chi = sum(gd.lay_so_tien() for gd in tai_khoan.lay_giao_dich() if gd.lay_loai() == "chi tiêu")
                
                for giao_dich in tai_khoan.lay_giao_dich():
                    csv_writer.writerow([
                        tai_khoan._ten, 
                        tai_khoan.lay_so_du(), 
                        tong_thu, 
                        tong_chi,
                        giao_dich._danh_muc, 
                        giao_dich.lay_so_tien(), 
                        giao_dich._ngay, 
                        giao_dich.lay_loai()
                    ])

    def dat_muc_tieu_tiet_kiem(self, id_tai_khoan: str, so_tien: float):
        """
        Dat muc tieu tiet kiem cho mot tai khoan cu the
        """
        for tai_khoan in self._tai_khoan:
            if tai_khoan._id == id_tai_khoan:
                self._muc_tieu_tiet_kiem[id_tai_khoan] = so_tien
                return True
        return False

    def du_bao_xu_huong_tai_chinh(self) -> dict:
        """
        Du bao xu huong tai chinh dua tren du lieu lich su
        """
        du_bao = {
            "xu_huong_chi_tieu": {},
            "du_bao_tiet_kiem": {},
            "canh_bao_no": []
        }
        
        # Xu huong chi tieu theo danh muc
        for tai_khoan in self._tai_khoan:
            danh_muc_chi_tieu = {}
            for giao_dich in tai_khoan.lay_giao_dich():
                if giao_dich.lay_loai() == "chi tiêu":
                    if giao_dich._danh_muc not in danh_muc_chi_tieu:
                        danh_muc_chi_tieu[giao_dich._danh_muc] = []
                    danh_muc_chi_tieu[giao_dich._danh_muc].append(giao_dich.lay_so_tien())
            
            for danh_muc, chi_tieu in danh_muc_chi_tieu.items():
                du_bao["xu_huong_chi_tieu"][danh_muc] = {
                    "trung_binh": sum(chi_tieu) / len(chi_tieu) if chi_tieu else 0,
                    "tong_chi": sum(chi_tieu)
                }
        
        # Du bao tiet kiem
        for id_tai_khoan, muc_tieu in self._muc_tieu_tiet_kiem.items():
            du_bao["du_bao_tiet_kiem"][id_tai_khoan] = {
                "muc_tieu": muc_tieu,
                "so_du_hien_tai": next((tk.lay_so_du() for tk in self._tai_khoan if tk._id == id_tai_khoan), 0)
            }
        
        # Canh bao no
        for khoan_vay in self._khoan_vay:
            canh_bao = {
                "id": khoan_vay._id,
                "so_tien_con_lai": khoan_vay.lay_so_tien_con_lai(),
                "nguoi_cho_vay": khoan_vay._nguoi_cho_vay,
                "ngay_den_han": khoan_vay._ngay_den_han
            }
            du_bao["canh_bao_no"].append(canh_bao)
        
        return du_bao

    def thiet_lap_phuong_phap_sau_lo(self, tong_thu_nhap: float):
        """
        Thiet lap phuong phap quan ly tai chinh 6 lo
        """
        self._phuong_phap_sau_lo = PhuongPhapSauLo(tong_thu_nhap)
        self._phuong_phap_sau_lo.phan_bo_thu_nhap()

    def them_danh_muc(self, danh_muc: DanhMuc):
        """
        Them mot danh muc moi vao he thong
        """
        if not any(dm._id == danh_muc._id for dm in self._danh_muc):
            self._danh_muc.append(danh_muc)
            return True
        return False

    def lay_thong_ke_tong_quat(self) -> dict:
        """
        Lay thong ke tong quat ve tinh hinh tai chinh
        """
        return {
            "so_tai_khoan": len(self._tai_khoan),
            "so_khoan_vay": len(self._khoan_vay),
            "tong_tai_san": sum(tk.lay_so_du() for tk in self._tai_khoan),
            "tong_no": sum(kv.lay_so_tien_con_lai() for kv in self._khoan_vay)
        }