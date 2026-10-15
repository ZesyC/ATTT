CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"


def kiem_tra_khoa(khoa):
    if not isinstance(khoa, str) or len(khoa) != 26:
        raise ValueError("Khóa phải chứa đúng 26 chữ cái A-Z khác nhau.")
    for ky_tu in khoa:
        if ky_tu not in CHU_HOA + CHU_THUONG:
            raise ValueError("Khóa chỉ được chứa chữ A-Z hoặc a-z.")
    khoa = khoa.upper()
    if set(khoa) != set(CHU_HOA):
        raise ValueError("Các chữ trong khóa không được trùng nhau.")
    return khoa


def thay_chu(van_ban, bang_nguon, bang_dich):
    ket_qua = []
    for ky_tu in van_ban:
        if ky_tu in CHU_HOA:
            vi_tri = bang_nguon.index(ky_tu)
            ket_qua.append(bang_dich[vi_tri])
        elif ky_tu in CHU_THUONG:
            vi_tri = bang_nguon.index(ky_tu.upper())
            ket_qua.append(bang_dich[vi_tri].lower())
        else:
            ket_qua.append(ky_tu)
    return "".join(ket_qua)


def ma_hoa(van_ban, khoa):
    khoa = kiem_tra_khoa(khoa)
    return thay_chu(van_ban, CHU_HOA, khoa)


def giai_ma(ban_ma, khoa):
    khoa = kiem_tra_khoa(khoa)
    return thay_chu(ban_ma, khoa, CHU_HOA)


if __name__ == "__main__":
    ban_ro = "Hello, Python! 123"
    khoa = "QWERTYUIOPASDFGHJKLZXCVBNM"
    ban_ma = ma_hoa(ban_ro, khoa)
    ban_giai_ma = giai_ma(ban_ma, khoa)
    print("Bản rõ:", ban_ro)
    print("Khóa:", khoa)
    print("Bản mã:", ban_ma)
    print("Giải mã:", ban_giai_ma)
    assert ban_giai_ma == ban_ro
    assert ma_hoa("Abc xyz", khoa) == "Qwe bnm"
