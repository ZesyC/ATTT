CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"


def ma_hoa(van_ban, khoa):
    if type(khoa) is not int:
        raise ValueError("Khóa dịch vòng phải là số nguyên.")
    ket_qua = []
    for ky_tu in van_ban:
        if ky_tu in CHU_HOA:
            vi_tri = CHU_HOA.index(ky_tu)
            ket_qua.append(CHU_HOA[(vi_tri + khoa) % 26])
        elif ky_tu in CHU_THUONG:
            vi_tri = CHU_THUONG.index(ky_tu)
            ket_qua.append(CHU_THUONG[(vi_tri + khoa) % 26])
        else:
            ket_qua.append(ky_tu)
    return "".join(ket_qua)


def giai_ma(ban_ma, khoa):
    if type(khoa) is not int:
        raise ValueError("Khóa dịch vòng phải là số nguyên.")
    return ma_hoa(ban_ma, -khoa)


if __name__ == "__main__":
    ban_ro = "Hello, Python! 123"
    khoa = 3
    ban_ma = ma_hoa(ban_ro, khoa)
    ban_giai_ma = giai_ma(ban_ma, khoa)
    print("Bản rõ:", ban_ro)
    print("Khóa:", khoa)
    print("Bản mã:", ban_ma)
    print("Giải mã:", ban_giai_ma)
    assert ban_giai_ma == ban_ro
    assert ma_hoa("ABC xyz", 3) == "DEF abc"
