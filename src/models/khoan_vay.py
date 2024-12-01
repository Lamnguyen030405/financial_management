from datetime import datetime
from typing import List, Dict

class KhoanVay:
    def __init__(self, id: str, so_tien: float, nguoi_cho_vay: str, nguoi_vay: str, 
                 lai_suat: float, ngay_bat_dau: datetime, ngay_den_han: datetime):
        """
        Khởi tạo một khoản vay mới
        
        :param id: Mã định danh của khoản vay
        :param so_tien: Số tiền vay ban đầu
        :param nguoi_cho_vay: Tên người cho vay
        :param nguoi_vay: Tên người vay
        :param lai_suat: Lãi suất hàng năm (%)
        :param ngay_bat_dau: Ngày bắt đầu vay
        :param ngay_den_han: Ngày đáo hạn
        """
        self._id = id
        self._so_tien = so_tien
        self._nguoi_cho_vay = nguoi_cho_vay
        self._nguoi_vay = nguoi_vay
        self._lai_suat = lai_suat
        self._ngay_bat_dau = ngay_bat_dau
        self._ngay_den_han = ngay_den_han
        self._trang_thai = "dang hoat dong"
        self._lich_su_thanh_toan: List[Dict] = []
        self._so_tien_con_lai = so_tien

    def tinh_lai(self) -> float:
        """
        Tính số tiền lãi dựa trên số tiền vay, lãi suất và thời gian vay
        
        :return: Số tiền lãi phải trả
        """
        # Tính số năm giữa ngày bắt đầu và ngày đáo hạn
        thoi_gian_vay = (self._ngay_den_han - self._ngay_bat_dau).days / 365.25
        
        # Tính tổng số tiền lãi 
        lai = self._so_tien * (self._lai_suat / 100) * thoi_gian_vay
        
        return round(lai, 2)

    def them_thanh_toan(self, so_tien: float, ngay: datetime):
        """
        Thêm một khoản thanh toán vào lịch sử và cập nhật số tiền còn lại
        
        :param so_tien: Số tiền thanh toán
        :param ngay: Ngày thanh toán
        :raises ValueError: Nếu số tiền thanh toán lớn hơn số tiền còn lại
        """
        if so_tien > self._so_tien_con_lai:
            raise ValueError("Số tiền thanh toán vượt quá số tiền còn lại")
        
        # Thêm thông tin thanh toán vào lịch sử
        thanh_toan = {
            "so_tien": so_tien,
            "ngay": ngay
        }
        self._lich_su_thanh_toan.append(thanh_toan)
        
        # Cập nhật số tiền còn lại
        self._so_tien_con_lai -= so_tien
        
        # Cập nhật trạng thái nếu đã thanh toán hết
        self.cap_nhat_trang_thai()

    def cap_nhat_trang_thai(self):
        """
        Cập nhật trạng thái khoản vay
        """
        if self._so_tien_con_lai <= 0:
            self._trang_thai = "da thanh toan"
        elif datetime.now() > self._ngay_den_han:
            self._trang_thai = "qua han"
        else:
            self._trang_thai = "dang hoat dong"

    def lay_so_tien_con_lai(self) -> float:
        """
        Lấy số tiền còn lại của khoản vay
        
        :return: Số tiền còn lại
        """
        return self._so_tien_con_lai

    def lay_lich_su_thanh_toan(self) -> List[Dict]:
        """
        Lấy lịch sử các khoản thanh toán
        
        :return: Danh sách các khoản thanh toán
        """
        return self._lich_su_thanh_toan