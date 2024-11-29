from typing import List
from datetime import datetime
from src.models.giao_dich import GiaoDich

class TaiKhoan:
    def __init__(self, id: str, ten: str, so_du: float, loai: str):
        self._id = id
        self._ten = ten
        self._so_du = so_du
        self._loai = loai
        self._giao_dich : List[GiaoDich] = []
    
    def them_giao_dich(self, giao_dich: GiaoDich):
        # Chú ý: sử dụng method thay vì gọi trực tiếp thuộc tính
        if giao_dich.lay_loai() == "thu nhập":
            self._so_du += giao_dich.lay_so_tien()
        elif giao_dich.lay_loai() == "chi tiêu":
            self._so_du -= giao_dich.lay_so_tien()
        self._giao_dich.append(giao_dich)
    
    def cap_nhat_so_du(self):
        self._so_du = 0
        for giao_dich in self._giao_dich:
            if giao_dich.lay_loai() == "thu nhập":
                self._so_du += giao_dich.lay_so_tien()
            elif giao_dich.lay_loai() == "chi tiêu":
                self._so_du -= giao_dich.lay_so_tien()
                
    def lay_so_du(self) -> float:
        return self._so_du
    
    def lay_giao_dich(self) -> List[GiaoDich]:
        return self._giao_dich