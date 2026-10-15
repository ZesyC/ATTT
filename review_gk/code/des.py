"""DES để học: ECB + PKCS#7; không dùng để bảo vệ dữ liệu thực tế."""

_DES_IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
]

_DES_IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
]

_DES_PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4,
]

_DES_PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]

_DES_SHIFTS = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1,
]

_DES_E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1,
]

_DES_P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25,
]

_DES_S = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]


def _hoan_vi(khoi: int, bang: list[int], so_bit: int) -> int:
    ket_qua = 0
    for vi_tri in bang:
        bit = (khoi >> (so_bit - vi_tri)) & 1
        ket_qua = (ket_qua << 1) | bit
    return ket_qua


def _tao_khoa_con(khoa: bytes) -> list[int]:
    khoa_so = int.from_bytes(khoa, "big")
    khoa_56_bit = _hoan_vi(khoa_so, _DES_PC1, 64)
    trai = khoa_56_bit >> 28
    phai = khoa_56_bit & 0x0FFFFFFF
    cac_khoa_con = []
    for so_dich in _DES_SHIFTS:
        trai = ((trai << so_dich) | (trai >> (28 - so_dich))) & 0x0FFFFFFF
        phai = ((phai << so_dich) | (phai >> (28 - so_dich))) & 0x0FFFFFFF
        ghep = (trai << 28) | phai
        cac_khoa_con.append(_hoan_vi(ghep, _DES_PC2, 56))
    return cac_khoa_con


def _ham_f(phai: int, khoa_con: int) -> int:
    mo_rong = _hoan_vi(phai, _DES_E, 32)
    tron_khoa = mo_rong ^ khoa_con
    thay_the = 0
    for chi_so in range(8):
        nhom = (tron_khoa >> (42 - 6 * chi_so)) & 0x3F
        hang = ((nhom & 0x20) >> 4) | (nhom & 1)
        cot = (nhom >> 1) & 0x0F
        thay_the = (thay_the << 4) | _DES_S[chi_so][hang][cot]
    return _hoan_vi(thay_the, _DES_P, 32)


def _bien_doi_khoi(khoi: bytes, cac_khoa_con: list[int]) -> bytes:
    khoi_so = int.from_bytes(khoi, "big")
    ban_dau = _hoan_vi(khoi_so, _DES_IP, 64)
    trai = ban_dau >> 32
    phai = ban_dau & 0xFFFFFFFF
    for khoa_con in cac_khoa_con:
        trai, phai = phai, trai ^ _ham_f(phai, khoa_con)
    ghep = (phai << 32) | trai
    ket_qua = _hoan_vi(ghep, _DES_IP_INV, 64)
    return ket_qua.to_bytes(8, "big")


def _kiem_tra_khoa(khoa: bytes) -> None:
    if not isinstance(khoa, bytes) or len(khoa) != 8:
        raise ValueError("Khóa DES phải là bytes có đúng 8 byte.")


def ma_hoa_khoi(khoi: bytes, khoa: bytes) -> bytes:
    _kiem_tra_khoa(khoa)
    if not isinstance(khoi, bytes) or len(khoi) != 8:
        raise ValueError("Khối DES phải là bytes có đúng 8 byte.")
    return _bien_doi_khoi(khoi, _tao_khoa_con(khoa))


def giai_ma_khoi(khoi: bytes, khoa: bytes) -> bytes:
    _kiem_tra_khoa(khoa)
    if not isinstance(khoi, bytes) or len(khoi) != 8:
        raise ValueError("Khối DES phải là bytes có đúng 8 byte.")
    cac_khoa_con = _tao_khoa_con(khoa)
    cac_khoa_con.reverse()
    return _bien_doi_khoi(khoi, cac_khoa_con)


def ma_hoa(van_ban: str, khoa: bytes) -> str:
    _kiem_tra_khoa(khoa)
    du_lieu = van_ban.encode("utf-8")
    so_dem = 8 - len(du_lieu) % 8
    du_lieu += bytes([so_dem] * so_dem)
    cac_khoa_con = _tao_khoa_con(khoa)
    ket_qua = bytearray()
    for vi_tri in range(0, len(du_lieu), 8):
        khoi = du_lieu[vi_tri:vi_tri + 8]
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_con))
    return ket_qua.hex().upper()


def giai_ma(ban_ma_hex: str, khoa: bytes) -> str:
    _kiem_tra_khoa(khoa)
    du_lieu = bytes.fromhex(ban_ma_hex)
    if not du_lieu or len(du_lieu) % 8 != 0:
        raise ValueError("Bản mã DES phải có độ dài dương và chia hết cho 8 byte.")
    cac_khoa_con = _tao_khoa_con(khoa)
    cac_khoa_con.reverse()
    ket_qua = bytearray()
    for vi_tri in range(0, len(du_lieu), 8):
        khoi = du_lieu[vi_tri:vi_tri + 8]
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_con))
    so_dem = ket_qua[-1]
    if not 1 <= so_dem <= 8:
        raise ValueError("Đệm PKCS#7 DES không hợp lệ; có thể sai khóa hoặc bản mã.")
    if ket_qua[-so_dem:] != bytes([so_dem] * so_dem):
        raise ValueError("Đệm PKCS#7 DES không hợp lệ; có thể sai khóa hoặc bản mã.")
    return ket_qua[:-so_dem].decode("utf-8")


if __name__ == "__main__":
    van_ban = "Xin chào DES!"
    khoa = b"12345678"
    ban_ma = ma_hoa(van_ban, khoa)
    ban_ro = giai_ma(ban_ma, khoa)
    print("Bản rõ:", van_ban)
    print("Bản mã hex:", ban_ma)
    print("Giải mã:", ban_ro)
    assert ban_ro == van_ban
    khoa_mau = bytes.fromhex("133457799BBCDFF1")
    khoi_mau = bytes.fromhex("0123456789ABCDEF")
    ma_mau = bytes.fromhex("85E813540F0AB405")
    assert ma_hoa_khoi(khoi_mau, khoa_mau) == ma_mau
    assert giai_ma_khoi(ma_mau, khoa_mau) == khoi_mau
