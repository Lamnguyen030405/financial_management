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
        # TODO: Thuc hien phan bo thu nhap
        pass

    def cap_nhat_so_tien_lo(self, ten_lo: str, so_tien: float):
        # TODO: Thuc hien cap nhat so tien trong lo
        pass

    def lay_so_du_lo(self, ten_lo: str) -> float:
        # TODO: Thuc hien lay so du lo
        pass

    def chuyen_tien_giua_cac_lo(self, tu_lo: str, den_lo: str, so_tien: float):
        # TODO: Thuc hien chuyen tien giua cac lo
        pass