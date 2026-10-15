CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"


def kiem_tra_khoa(khoa):
    if not isinstance(khoa, str) or not khoa:
        raise ValueError("Khóa Vigenere phải là chuỗi chữ cái không rỗng.")
    for ky_tu in khoa:
        if ky_tu not in CHU_HOA + CHU_THUONG:
            raise ValueError("Khóa Vigenere chỉ chứa chữ A-Z hoặc a-z.")
    return khoa.upper()


def bien_doi(van_ban, khoa, huong):
    khoa = kiem_tra_khoa(khoa)
    ket_qua = []
    vi_tri_khoa = 0
    for ky_tu in van_ban:
        if ky_tu in CHU_HOA:
            bang_chu = CHU_HOA
        elif ky_tu in CHU_THUONG:
            bang_chu = CHU_THUONG
        else:
            ket_qua.append(ky_tu)
            continue
        chu_khoa = khoa[vi_tri_khoa % len(khoa)]
        do_dich = CHU_HOA.index(chu_khoa)
        vi_tri = bang_chu.index(ky_tu)
        ket_qua.append(bang_chu[(vi_tri + huong * do_dich) % 26])
        vi_tri_khoa += 1
    return "".join(ket_qua)


def ma_hoa(van_ban, khoa):
    return bien_doi(van_ban, khoa, 1)


def giai_ma(ban_ma, khoa):
    return bien_doi(ban_ma, khoa, -1)


if __name__ == "__main__":
    ban_ro = "Attack at dawn!"
    khoa = "LEMON"
    ban_ma = ma_hoa(ban_ro, khoa)
    ban_giai_ma = giai_ma(ban_ma, khoa)
    print("Bản rõ:", ban_ro)
    print("Khóa:", khoa)
    print("Bản mã:", ban_ma)
    print("Giải mã:", ban_giai_ma)
    assert ban_giai_ma == ban_ro
    assert ma_hoa("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
