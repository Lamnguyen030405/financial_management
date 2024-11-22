from datetime import datetime
from typing import List
from financial_management.src.models.tai_khoan import TaiKhoan
from financial_management.src.models.khoan_vay import KhoanVay
from financial_management.src.models.giao_dich import GiaoDich
from financial_management.src.models.danh_muc import DanhMuc
from financial_management.src.models.phuong_phap_sau_lo import PhuongPhapSauLo

class QuanLyTaiChinh:
    def __init__(self):
        """
        Khoi tao quan ly tai chinh voi danh sach tai khoan, khoan vay va danh muc trong
        """
        self._tai_khoan: List[TaiKhoan] = []
        self._khoan_vay: List[KhoanVay] = []
        self._danh_muc: List[DanhMuc] = []
        self._phuong_phap_sau_lo = None

    def them_tai_khoan(self, tai_khoan: TaiKhoan):
        """
        Them mot tai khoan moi vao he thong
        """
        if not any(tk._id == tai_khoan._id for tk in self._tai_khoan):
            self._tai_khoan.append(tai_khoan)
            return True
        return False

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
        if not any(kv._id == khoan_vay._id for kv in self._khoan_vay):
            self._khoan_vay.append(khoan_vay)
            return True
        return False

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
        
        # TODO: Them logic tao bao cao chi tiet
        return bao_cao

    def xuat_csv(self, duong_dan: str = "bao_cao_tai_chinh.csv"):
        """
        Xuat du lieu tai chinh ra file CSV
        """
        # TODO: Implement xuat du lieu ra CSV
        pass

    def dat_muc_tieu_tiet_kiem(self, id_tai_khoan: str, so_tien: float):
        """
        Dat muc tieu tiet kiem cho mot tai khoan cu the
        """
        for tai_khoan in self._tai_khoan:
            if tai_khoan._id == id_tai_khoan:
                # TODO: Implement logic dat muc tieu tiet kiem
                pass
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
        
        # TODO: Implement logic du bao
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