class DanhMuc:
    def __init__(self, id: str, ten: str, loai: str, mo_ta: str):
        """
        id: Mã định danh duy nhất cho danh mục
        ten: Tên của danh mục (ví dụ: "Ăn uống", "Lương")
        loai: Phân loại chính của danh mục (ví dụ: "Chi tiêu", "Thu nhập")
        mo_ta: Mô tả chi tiết về danh mục
        """
        self._id = id
        self._ten = ten
        self._loai = loai
        self._mo_ta = mo_ta
    
    def cap_nhat_danh_muc(self, ten: str, loai: str):
        """
        Phương thức cập nhật tên và loại của danh mục
        
        :param ten: Tên mới của danh mục
        :param loai: Loại mới của danh mục
        """
        # Kiểm tra tính hợp lệ của đầu vào
        if not ten or not loai:
            raise ValueError("Tên và loại danh mục không được để trống")
        
        # Cập nhật tên danh mục
        self._ten = ten
        
        # Cập nhật loại danh mục
        self._loai = loai