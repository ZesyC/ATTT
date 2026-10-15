def kiem_tra_khoa(khoa):
    if not isinstance(khoa, (list, tuple)) or not khoa:
        raise ValueError("Khóa hoán vị phải là danh sách vị trí không rỗng.")
    for vi_tri in khoa:
        if type(vi_tri) is not int:
            raise ValueError("Các vị trí trong khóa phải là số nguyên.")
    if sorted(khoa) != list(range(1, len(khoa) + 1)):
        raise ValueError("Khóa phải là hoán vị của các số từ 1 đến độ dài khóa.")


def ma_hoa(van_ban, khoa):
    kiem_tra_khoa(khoa)
    kich_thuoc = len(khoa)
    so_ky_tu_dem = (-len(van_ban)) % kich_thuoc
    van_ban = van_ban + " " * so_ky_tu_dem
    ket_qua = []
    for bat_dau in range(0, len(van_ban), kich_thuoc):
        khoi = van_ban[bat_dau:bat_dau + kich_thuoc]
        for vi_tri in khoa:
            ket_qua.append(khoi[vi_tri - 1])
    return "".join(ket_qua), so_ky_tu_dem


def giai_ma(ban_ma, khoa, so_ky_tu_dem=0):
    kiem_tra_khoa(khoa)
    kich_thuoc = len(khoa)
    if len(ban_ma) % kich_thuoc != 0:
        raise ValueError("Độ dài bản mã phải chia hết cho độ dài khóa.")
    if type(so_ky_tu_dem) is not int or not 0 <= so_ky_tu_dem < kich_thuoc:
        raise ValueError("Số ký tự đệm phải từ 0 đến độ dài khóa trừ 1.")
    ket_qua = []
    for bat_dau in range(0, len(ban_ma), kich_thuoc):
        khoi = ban_ma[bat_dau:bat_dau + kich_thuoc]
        khoi_goc = [""] * kich_thuoc
        for chi_so in range(kich_thuoc):
            vi_tri_goc = khoa[chi_so] - 1
            khoi_goc[vi_tri_goc] = khoi[chi_so]
        ket_qua.append("".join(khoi_goc))
    ban_ro = "".join(ket_qua)
    if so_ky_tu_dem > 0:
        if len(ban_ro) < so_ky_tu_dem or not ban_ro.endswith(" " * so_ky_tu_dem):
            raise ValueError("Số ký tự đệm không khớp bản rõ sau giải mã.")
        ban_ro = ban_ro[:-so_ky_tu_dem]
    return ban_ro


if __name__ == "__main__":
    ban_ro = "HOC PYTHON!  "
    khoa = [3, 1, 4, 2]
    ban_ma, so_ky_tu_dem = ma_hoa(ban_ro, khoa)
    ban_giai_ma = giai_ma(ban_ma, khoa, so_ky_tu_dem)
    print("Bản rõ:", repr(ban_ro))
    print("Khóa:", khoa)
    print("Bản mã:", repr(ban_ma))
    print("Số ký tự đệm:", so_ky_tu_dem)
    print("Giải mã:", repr(ban_giai_ma))
    assert ban_giai_ma == ban_ro
    assert ma_hoa("ABCD", khoa) == ("CADB", 0)
