class PhuongPhapSauLo:
    def __init__(self, tong_thu_nhap: float):
        self._lo = {
            "thiet_yeu": 0.0,       # 55% cho nhu cau thiet yeu
            "dai_han": 0.0,         # 10% cho tiet kiem dai han
            "giao_duc": 0.0,        # 10% cho giao duc
            "giai_tri": 0.0,        # 10% cho giai tri
            "tu_do_tai_chinh": 0.0, # 10% cho tu do tai chinh
            "cho_di": 0.0           # 5% cho viec cho di
        }
        self._tong_thu_nhap = tong_thu_nhap

    def phan_bo_thu_nhap(self):
        self._lo["thiet_yeu"] = self._tong_thu_nhap * 0.55
        self._lo["dai_han"] = self._tong_thu_nhap * 0.10
        self._lo["giao_duc"] = self._tong_thu_nhap * 0.10
        self._lo["giai_tri"] = self._tong_thu_nhap * 0.10
        self._lo["tu_do_tai_chinh"] = self._tong_thu_nhap * 0.10
        self._lo["cho_di"] = self._tong_thu_nhap * 0.05
       
    def cap_nhat_so_tien_lo(self, ten_lo: str, so_tien: float):
        if ten_lo in self._lo:
            self._lo[ten_lo] += so_tien
        else:
            raise ValueError(f"Lọ '{ten_lo}' không tồn tại.")
        
    def lay_so_du_lo(self, ten_lo: str) -> float:
         if ten_lo in self._lo:
            return self._lo[ten_lo]
         else:
            raise ValueError(f"Lọ '{ten_lo}' không tồn tại.")
         
    def chuyen_tien_giua_cac_lo(self, tu_lo: str, den_lo: str, so_tien: float):
        if tu_lo not in self._lo:
            raise ValueError(f"Lọ nguồn '{tu_lo}' không tồn tại.")
        if den_lo not in self._lo:
            raise ValueError(f"Lọ đích '{den_lo}' không tồn tại.")
        if self._lo[tu_lo] < so_tien:
            raise ValueError(f"Lọ nguồn '{tu_lo}' không đủ tiền để chuyển.")

        self._lo[tu_lo] -= so_tien
        self._lo[den_lo] += so_tien
