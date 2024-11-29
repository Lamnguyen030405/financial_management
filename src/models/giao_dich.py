from datetime import datetime

class GiaoDich:
    def __init__(self, id: str, id_tai_khoan: str, so_tien: float, 
                 loai: str, danh_muc: str, ngay: datetime, ghi_chu: str):
        self._id = id
        self._id_tai_khoan = id_tai_khoan
        self._so_tien = so_tien
        self._loai = loai
        self._danh_muc = danh_muc
        self._ngay = ngay
        self._ghi_chu = ghi_chu

    def lay_so_tien(self) -> float:
        return self._so_tien

    def lay_loai(self) -> str:
        return self._loai

    def cap_nhat_chi_tiet(self, so_tien: float, loai: str):
        self._so_tien = so_tien
        self._loai = loai