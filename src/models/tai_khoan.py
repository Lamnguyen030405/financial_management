from typing import List
from datetime import datetime
from financial_management.src.models.giao_dich import GiaoDich

class TaiKhoan:
    def __init__(self, id: str, ten: str, so_du: float, loai: str):
        self._id = id
        self._ten = ten
        self._so_du = so_du
        self._loai = loai
        self._giao_dich : List[GiaoDich] = []

    def them_giao_dich(self, giao_dich):
        # TODO: Thuc hien them giao dich
        pass

    def cap_nhat_so_du(self):
        # TODO: Thuc hien cap nhat so du
        pass

    def lay_so_du(self) -> float:
        return self._so_du

    def lay_giao_dich(self) -> List:
        return self._giao_dich
