"""MD5 viết tay bằng mảng 0/1; chỉ dùng học tập, không dùng cho bảo mật mới."""

# Hằng số theo RFC 1321: https://www.rfc-editor.org/rfc/rfc1321
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


def bam_md5(van_ban: str) -> str:
    if not isinstance(van_ban, str):
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")
    du_lieu = [bit for byte in van_ban.encode("utf-8") for bit in so_sang_mang(byte, 8)]
    do_dai_ban_dau = len(du_lieu)
    du_lieu.append(1)
    du_lieu.extend([0] * ((448 - len(du_lieu)) % 512))
    du_lieu.extend(doi_thu_tu_byte(so_sang_mang(do_dai_ban_dau, 64)))
    trang_thai = [so_sang_mang(so, 32) for so in [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]]
    bang_k = [so_sang_mang(so, 32) for so in BANG_K]

    for dau_khoi in range(0, len(du_lieu), 512):
        khoi = du_lieu[dau_khoi:dau_khoi + 512]
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


if __name__ == "__main__":
    van_ban = "Xin chào Python!"
    assert bam_md5("abc") == "900150983cd24fb0d6963f7d28e17f72"
    print("Văn bản:", van_ban)
    print("MD5 (128 bit, 32 ký tự hex):", bam_md5(van_ban))
    print("Băm là một chiều: không có hàm giải mã.")
