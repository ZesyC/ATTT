from pathlib import Path


BANG_K = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
]
SO_BUOC_XOAY = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4


def so_sang_mang(so: int, do_dai: int) -> list[int]:
    mang = [0] * do_dai
    for i in range(do_dai - 1, -1, -1):
        mang[i] = so % 2
        so //= 2
    return mang


def mang_sang_so(mang: list[int]) -> int:
    so = 0
    for bit in mang:
        so = so * 2 + bit
    return so


def xor(*cac_mang: list[int]) -> list[int]:
    return [sum(cot) % 2 for cot in zip(*cac_mang)]


def va(a: list[int], b: list[int]) -> list[int]:
    return [x * y for x, y in zip(a, b)]


def hoac(a: list[int], b: list[int]) -> list[int]:
    return [max(x, y) for x, y in zip(a, b)]


def dao(mang: list[int]) -> list[int]:
    return [1 - bit for bit in mang]


def cong(*cac_mang: list[int]) -> list[int]:
    ket_qua = [0] * len(cac_mang[0])
    nho = 0
    for i in range(len(ket_qua) - 1, -1, -1):
        tong = nho + sum(mang[i] for mang in cac_mang)
        ket_qua[i] = tong % 2
        nho = tong // 2
    return ket_qua


def xoay_trai(mang: list[int], so_buoc: int) -> list[int]:
    so_buoc %= len(mang)
    return mang[so_buoc:] + mang[:so_buoc]


def doi_thu_tu_byte(mang: list[int]) -> list[int]:
    return [bit for i in range(len(mang) - 8, -1, -8) for bit in mang[i:i + 8]]


def bam_md5(du_lieu: bytes) -> str:
    if not isinstance(du_lieu, bytes):
        raise ValueError("Dữ liệu cần băm phải là bytes.")
    cac_bit = [bit for byte in du_lieu for bit in so_sang_mang(byte, 8)]
    do_dai_ban_dau = len(cac_bit)
    cac_bit.append(1)
    cac_bit.extend([0] * ((448 - len(cac_bit)) % 512))
    cac_bit.extend(doi_thu_tu_byte(so_sang_mang(do_dai_ban_dau, 64)))
    trang_thai = [so_sang_mang(so, 32) for so in [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]]
    bang_k = [so_sang_mang(so, 32) for so in BANG_K]

    for dau_khoi in range(0, len(cac_bit), 512):
        khoi = cac_bit[dau_khoi:dau_khoi + 512]
        ma_tran = [doi_thu_tu_byte(khoi[i:i + 32]) for i in range(0, 512, 32)]
        a, b, c, d = trang_thai
        for i in range(64):
            if i < 16:
                f = hoac(va(b, c), va(dao(b), d))
                vi_tri = i
            elif i < 32:
                f = hoac(va(b, d), va(c, dao(d)))
                vi_tri = (5 * i + 1) % 16
            elif i < 48:
                f = xor(b, c, d)
                vi_tri = (3 * i + 5) % 16
            else:
                f = xor(c, hoac(b, dao(d)))
                vi_tri = (7 * i) % 16
            tong = cong(a, f, bang_k[i], ma_tran[vi_tri])
            b_moi = cong(b, xoay_trai(tong, SO_BUOC_XOAY[i]))
            a, b, c, d = d, b_moi, b, c
        trang_thai = [cong(cu, moi) for cu, moi in zip(trang_thai, [a, b, c, d])]

    return "".join(f"{mang_sang_so(doi_thu_tu_byte(tu)):08x}" for tu in trang_thai)


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


def _so_thanh_bit(so: int, do_dai: int) -> list[int]:

    cac_bit = [0] * do_dai
    for vi_tri in range(do_dai - 1, -1, -1):
        cac_bit[vi_tri] = so % 2
        so = so // 2
    return cac_bit


def _bit_thanh_so(cac_bit: list[int]) -> int:
    ket_qua = 0
    for bit in cac_bit:
        ket_qua = ket_qua * 2 + bit
    return ket_qua


def _byte_thanh_bit(du_lieu: bytes) -> list[int]:
    cac_bit = []
    for byte in du_lieu:
        cac_bit.extend(_so_thanh_bit(byte, 8))
    return cac_bit


def _bit_thanh_byte(cac_bit: list[int]) -> bytes:
    cac_byte = []
    for vi_tri in range(0, len(cac_bit), 8):
        cac_byte.append(_bit_thanh_so(cac_bit[vi_tri:vi_tri + 8]))
    return bytes(cac_byte)


def _xor(trai: list[int], phai: list[int]) -> list[int]:

    ket_qua = []
    for vi_tri in range(len(trai)):
        ket_qua.append((trai[vi_tri] + phai[vi_tri]) % 2)
    return ket_qua


def _hoan_vi(khoi: list[int], bang: list[int]) -> list[int]:
    ket_qua = []
    for vi_tri in bang:
        ket_qua.append(khoi[vi_tri - 1])
    return ket_qua


def _tao_khoa_con(khoa: bytes) -> list[list[int]]:
    khoa_64_bit = _byte_thanh_bit(khoa)
    khoa_56_bit = _hoan_vi(khoa_64_bit, _DES_PC1)
    trai = khoa_56_bit[:28]
    phai = khoa_56_bit[28:]
    cac_khoa_con = []
    for so_dich in _DES_SHIFTS:
        trai = trai[so_dich:] + trai[:so_dich]
        phai = phai[so_dich:] + phai[:so_dich]
        ghep = trai + phai
        cac_khoa_con.append(_hoan_vi(ghep, _DES_PC2))
    return cac_khoa_con


def _ham_f(phai: list[int], khoa_con: list[int]) -> list[int]:
    mo_rong = _hoan_vi(phai, _DES_E)
    tron_khoa = _xor(mo_rong, khoa_con)
    thay_the = []
    for chi_so in range(8):
        nhom = tron_khoa[6 * chi_so:6 * chi_so + 6]
        hang = _bit_thanh_so([nhom[0], nhom[5]])
        cot = _bit_thanh_so(nhom[1:5])
        gia_tri = _DES_S[chi_so][hang][cot]
        thay_the.extend(_so_thanh_bit(gia_tri, 4))
    return _hoan_vi(thay_the, _DES_P)


def _bien_doi_khoi(khoi: bytes, cac_khoa_con: list[list[int]]) -> bytes:
    cac_bit = _byte_thanh_bit(khoi)
    ban_dau = _hoan_vi(cac_bit, _DES_IP)
    trai = ban_dau[:32]
    phai = ban_dau[32:]
    for khoa_con in cac_khoa_con:
        trai_moi = phai
        phai_moi = _xor(trai, _ham_f(phai, khoa_con))
        trai, phai = trai_moi, phai_moi
    ghep = phai + trai
    ket_qua = _hoan_vi(ghep, _DES_IP_INV)
    return _bit_thanh_byte(ket_qua)


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


def ma_hoa(du_lieu: bytes, khoa: bytes) -> bytes:
    _kiem_tra_khoa(khoa)
    so_dem = 8 - len(du_lieu) % 8
    du_lieu += bytes([so_dem] * so_dem)
    cac_khoa_con = _tao_khoa_con(khoa)
    ket_qua = bytearray()
    for vi_tri in range(0, len(du_lieu), 8):
        khoi = du_lieu[vi_tri:vi_tri + 8]
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_con))
    return bytes(ket_qua)


def giai_ma(du_lieu: bytes, khoa: bytes) -> bytes:
    _kiem_tra_khoa(khoa)
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
    return bytes(ket_qua[:-so_dem])


def ma_hoa_tep(ten_tep, khoa):
    with open(ten_tep, "rb") as tep:
        du_lieu = tep.read()
    y = bam_md5(du_lieu)
    du_lieu += y.encode("ascii")
    ban_ma = ma_hoa(du_lieu, khoa)
    ten_ma = ten_tep + ".des"
    with open(ten_ma, "xb") as tep:
        tep.write(ban_ma)
    return ten_ma, y


def kiem_tra_tep(ten_tep, khoa):
    with open(ten_tep, "rb") as tep:
        ban_ma = tep.read()
    try:
        du_lieu = giai_ma(ban_ma, khoa)
    except ValueError:
        return False
    if len(du_lieu) < 32:
        return False
    x = du_lieu[:-32]
    y_cu = du_lieu[-32:]
    y_moi = bam_md5(x).encode("ascii")
    return y_moi == y_cu


if __name__ == "__main__":
    print("1. Tính MD5, ghép vào cuối dữ liệu và mã hóa DES")
    print("2. Kiểm tra tính toàn vẹn của tệp .des đã lưu")
    try:
        chon = input("Chọn 1 hoặc 2: ").strip()
        if chon not in ("1", "2"):
            raise ValueError("Chỉ được chọn 1 hoặc 2.")
        ten_tep = str(Path(__file__).with_name("X.txt"))
        khoa = input("Nhập khóa DES gồm đúng 8 ký tự ASCII: ").encode("ascii")
        if len(khoa) != 8:
            raise ValueError("Khóa phải gồm đúng 8 ký tự ASCII.")
        if chon == "1":
            ten_ma, y = ma_hoa_tep(ten_tep, khoa)
            print("MD5 ban đầu:", y)
            print("Đã lưu tệp mã hóa:", ten_ma)
        else:
            if kiem_tra_tep(ten_tep + ".des", khoa):
                print("MD5 khớp: chưa phát hiện thay đổi nội dung tệp.")
            else:
                print("Kiểm tra không đạt: tệp đã bị thay đổi, bị hỏng hoặc khóa không đúng.")
    except (OSError, ValueError) as loi:
        print("Lỗi:", loi)
