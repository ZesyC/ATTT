CHU_CAI = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def ma_tran_nghich_dao(khoa):
    if not isinstance(khoa, (list, tuple)) or len(khoa) != 2:
        raise ValueError("Khóa Hill phải là ma trận 2x2.")
    for hang in khoa:
        if not isinstance(hang, (list, tuple)) or len(hang) != 2:
            raise ValueError("Mỗi hàng của khóa Hill phải có 2 số nguyên.")
        for so in hang:
            if type(so) is not int:
                raise ValueError("Các phần tử khóa Hill phải là số nguyên.")
    a, b = khoa[0]
    c, d = khoa[1]
    dinh_thuc = (a * d - b * c) % 26
    for so in range(1, 26):
        if (dinh_thuc * so) % 26 == 1:
            return [[d * so % 26, -b * so % 26], [-c * so % 26, a * so % 26]]
    raise ValueError("Định thức khóa Hill phải nguyên tố cùng nhau với 26.")


def kiem_tra_van_ban(van_ban):
    for ky_tu in van_ban:
        if ky_tu not in CHU_CAI:
            raise ValueError("Hill chỉ nhận A-Z viết hoa, không có khoảng trắng hay dấu.")


def bien_doi_cap(van_ban, ma_tran):
    ket_qua = []
    for vi_tri in range(0, len(van_ban), 2):
        x = CHU_CAI.index(van_ban[vi_tri])
        y = CHU_CAI.index(van_ban[vi_tri + 1])
        so_dau = (ma_tran[0][0] * x + ma_tran[0][1] * y) % 26
        so_sau = (ma_tran[1][0] * x + ma_tran[1][1] * y) % 26
        ket_qua.append(CHU_CAI[so_dau])
        ket_qua.append(CHU_CAI[so_sau])
    return "".join(ket_qua)


def ma_hoa(van_ban, khoa):
    ma_tran_nghich_dao(khoa)
    kiem_tra_van_ban(van_ban)
    so_ky_tu_dem = len(van_ban) % 2
    van_ban = van_ban + "X" * so_ky_tu_dem
    ban_ma = bien_doi_cap(van_ban, khoa)
    return ban_ma, so_ky_tu_dem


def giai_ma(ban_ma, khoa, so_ky_tu_dem=0):
    khoa_dao = ma_tran_nghich_dao(khoa)
    kiem_tra_van_ban(ban_ma)
    if len(ban_ma) % 2 != 0:
        raise ValueError("Độ dài bản mã Hill phải là số chẵn.")
    if type(so_ky_tu_dem) is not int or so_ky_tu_dem not in (0, 1):
        raise ValueError("Số ký tự đệm Hill phải bằng 0 hoặc 1.")
    ban_ro = bien_doi_cap(ban_ma, khoa_dao)
    if so_ky_tu_dem == 1:
        if not ban_ro.endswith("X"):
            raise ValueError("Số ký tự đệm không khớp bản rõ sau giải mã.")
        ban_ro = ban_ro[:-1]
    return ban_ro


if __name__ == "__main__":
    ban_ro = "HELLO"
    khoa = [[3, 3], [2, 5]]
    ban_ma, so_ky_tu_dem = ma_hoa(ban_ro, khoa)
    ban_giai_ma = giai_ma(ban_ma, khoa, so_ky_tu_dem)
    print("Bản rõ:", ban_ro)
    print("Khóa:", khoa)
    print("Bản mã:", ban_ma)
    print("Số ký tự đệm:", so_ky_tu_dem)
    print("Giải mã:", ban_giai_ma)
    assert ban_giai_ma == ban_ro
    assert ma_hoa("HELP", khoa) == ("HIAT", 0)
    ban_ma_x, so_dem_x = ma_hoa("BOX", khoa)
    assert giai_ma(ban_ma_x, khoa, so_dem_x) == "BOX"
