"""RSA không có padding, dùng số nguyên tố nhỏ: chỉ để học, không dùng bảo mật thực tế."""

def uoc_chung_lon_nhat(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def nghich_dao_modulo(so: int, modulo: int) -> int:
    du_cu, du = modulo, so % modulo
    he_so_cu, he_so = 0, 1
    while du != 0:
        thuong = du_cu // du
        du_cu, du = du, du_cu - thuong * du
        he_so_cu, he_so = he_so, he_so_cu - thuong * he_so
    if du_cu != 1:
        raise ValueError("Không tồn tại nghịch đảo mô-đun.")
    return he_so_cu % modulo


def luy_thua_modulo(co_so: int, so_mu: int, modulo: int) -> int:
    if so_mu < 0 or modulo <= 0:
        raise ValueError("Số mũ phải không âm và mô-đun phải dương.")
    ket_qua = 1 % modulo
    co_so = co_so % modulo
    while so_mu > 0:
        if so_mu % 2 == 1:
            ket_qua = (ket_qua * co_so) % modulo
        co_so = (co_so * co_so) % modulo
        so_mu = so_mu // 2
    return ket_qua


def la_so_nguyen_to(so: int) -> bool:
    if type(so) is not int or so < 2:
        return False
    uoc = 2
    while uoc * uoc <= so:
        if so % uoc == 0:
            return False
        uoc += 1
    return True


def tao_khoa(p: int, q: int, e: int = 17) -> tuple[tuple[int, int], tuple[int, int]]:
    if not la_so_nguyen_to(p) or not la_so_nguyen_to(q) or p == q:
        raise ValueError("p và q phải là hai số nguyên tố khác nhau.")
    n = p * q
    phi = (p - 1) * (q - 1)
    if n <= 255:
        raise ValueError("p * q phải lớn hơn 255 để mã hóa từng byte UTF-8.")
    if type(e) is not int or not 1 < e < phi or uoc_chung_lon_nhat(e, phi) != 1:
        raise ValueError("e phải là số nguyên, 1 < e < phi và gcd(e, phi) = 1.")
    d = nghich_dao_modulo(e, phi)
    return (e, n), (d, n)


def kiem_tra_khoa(khoa: tuple[int, int]) -> None:
    if not isinstance(khoa, tuple) or len(khoa) != 2:
        raise ValueError("Khóa phải có dạng (số mũ, n).")
    so_mu, n = khoa
    if type(so_mu) is not int or type(n) is not int:
        raise ValueError("Số mũ và n phải là số nguyên.")
    if n <= 255 or not 1 < so_mu < n:
        raise ValueError("Khóa phải có n > 255 và 1 < số mũ < n.")


def ma_hoa(van_ban: str, khoa_cong_khai: tuple[int, int]) -> list[int]:
    kiem_tra_khoa(khoa_cong_khai)
    if not isinstance(van_ban, str):
        raise ValueError("Văn bản cần mã hóa phải là chuỗi.")
    e, n = khoa_cong_khai
    ban_ma = []
    for byte in van_ban.encode("utf-8"):
        ban_ma.append(luy_thua_modulo(byte, e, n))
    return ban_ma


def giai_ma(ban_ma: list[int], khoa_bi_mat: tuple[int, int]) -> str:
    kiem_tra_khoa(khoa_bi_mat)
    if not isinstance(ban_ma, list):
        raise ValueError("Bản mã phải là danh sách các số nguyên.")
    d, n = khoa_bi_mat
    du_lieu = bytearray()
    for so in ban_ma:
        if type(so) is not int or not 0 <= so < n:
            raise ValueError("Mỗi số trong bản mã phải thỏa mãn 0 <= số < n.")
        byte = luy_thua_modulo(so, d, n)
        if byte > 255:
            raise ValueError("Bản mã hoặc khóa không hợp lệ: kết quả không phải byte.")
        du_lieu.append(byte)
    try:
        return du_lieu.decode("utf-8")
    except UnicodeDecodeError as loi:
        raise ValueError("Bản mã hoặc khóa không tạo ra văn bản UTF-8 hợp lệ.") from loi


if __name__ == "__main__":
    p, q, e = 61, 53, 17
    khoa_cong_khai, khoa_bi_mat = tao_khoa(p, q, e)
    van_ban = "Xin chào Python!"
    ban_ma = ma_hoa(van_ban, khoa_cong_khai)
    ban_giai_ma = giai_ma(ban_ma, khoa_bi_mat)
    assert ban_giai_ma == van_ban
    assert luy_thua_modulo(65, e, p * q) == 2790
    assert luy_thua_modulo(2790, khoa_bi_mat[0], p * q) == 65
    print("p, q, e:", p, q, e)
    print("Khóa công khai (e, n):", khoa_cong_khai)
    print("Khóa bí mật (d, n):", khoa_bi_mat)
    print("Bản gốc:", van_ban)
    print("Bản mã:", ban_ma)
    print("Giải mã:", ban_giai_ma)
