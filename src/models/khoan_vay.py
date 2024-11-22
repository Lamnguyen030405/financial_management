from datetime import datetime
from typing import List, Dict

class KhoanVay:
    def __init__(self, id: str, so_tien: float, nguoi_cho_vay: str, nguoi_vay: str, 
                 lai_suat: float, ngay_bat_dau: datetime, ngay_den_han: datetime):
        self._id = id
        self._so_tien = so_tien
        self._nguoi_cho_vay = nguoi_cho_vay
        self._nguoi_vay = nguoi_vay
        self._lai_suat = lai_suat
        self._ngay_bat_dau = ngay_bat_dau
        self._ngay_den_han = ngay_den_han
        self._trang_thai = "dang hoat dong"
        self._lich_su_thanh_toan: List[Dict] = []

    def tinh_lai(self) -> float:
        # TODO: Thuc hien tinh toan lai
        pass

    def them_thanh_toan(self, so_tien: float, ngay: datetime):
        # TODO: Thuc hien them thanh toan
        pass

    def cap_nhat_trang_thai(self):
        # TODO: Thuc hien cap nhat trang thai
        pass

    def lay_so_tien_con_lai(self) -> float:
        # TODO: Thuc hien tinh so tien con lai
        pass