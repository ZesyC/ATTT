CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"


def nghich_dao_mod_26(a):
    for so in range(1, 26):
        if (a * so) % 26 == 1:
            return so
    raise ValueError("a phải nguyên tố cùng nhau với 26, ví dụ 5 hoặc 7.")


def kiem_tra_khoa(a, b):
    if type(a) is not int or type(b) is not int:
        raise ValueError("Hai thành phần a và b phải là số nguyên.")
    return nghich_dao_mod_26(a)


def bien_doi(van_ban, he_so, do_dich):
    ket_qua = []
    for ky_tu in van_ban:
        if ky_tu in CHU_HOA:
            vi_tri = CHU_HOA.index(ky_tu)
            ket_qua.append(CHU_HOA[(he_so * vi_tri + do_dich) % 26])
        elif ky_tu in CHU_THUONG:
            vi_tri = CHU_THUONG.index(ky_tu)
            ket_qua.append(CHU_THUONG[(he_so * vi_tri + do_dich) % 26])
        else:
            ket_qua.append(ky_tu)
    return "".join(ket_qua)


def ma_hoa(van_ban, a, b):
    kiem_tra_khoa(a, b)
    return bien_doi(van_ban, a, b)


def giai_ma(ban_ma, a, b):
    a_nghich_dao = kiem_tra_khoa(a, b)
    return bien_doi(ban_ma, a_nghich_dao, -a_nghich_dao * b)


if __name__ == "__main__":
    ban_ro = "Affine Cipher!"
    a, b = 5, 8
    ban_ma = ma_hoa(ban_ro, a, b)
    ban_giai_ma = giai_ma(ban_ma, a, b)
    print("Bản rõ:", ban_ro)
    print("Khóa (a, b):", (a, b))
    print("Bản mã:", ban_ma)
    print("Giải mã:", ban_giai_ma)
    assert ban_giai_ma == ban_ro
    assert ma_hoa("AFFINECIPHER", 5, 8) == "IHHWVCSWFRCP"
