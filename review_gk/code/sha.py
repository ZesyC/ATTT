"""SHA viết tay bằng mảng 0/1; SHA-1 chỉ dùng học tập, ưu tiên SHA-256 hoặc SHA-512."""

# Hằng số theo FIPS 180-4: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
BANG_K_256 = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
BANG_K_512 = [
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
    0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
    0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
    0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
    0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
    0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
    0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
    0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
    0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
    0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
    0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
    0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
    0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817,
]


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


def chon(x: list[int], y: list[int], z: list[int]) -> list[int]:
    return [b if a == 1 else c for a, b, c in zip(x, y, z)]


def da_so(x: list[int], y: list[int], z: list[int]) -> list[int]:
    return [int(a + b + c >= 2) for a, b, c in zip(x, y, z)]


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


def xoay_phai(mang: list[int], so_buoc: int) -> list[int]:
    so_buoc %= len(mang)
    return mang[-so_buoc:] + mang[:-so_buoc]


def dich_phai(mang: list[int], so_buoc: int) -> list[int]:
    so_buoc = min(so_buoc, len(mang))
    return [0] * so_buoc + mang[:len(mang) - so_buoc]


def dem_du_lieu(van_ban: str, do_dai_khoi: int, do_dai_truong: int) -> list[int]:
    if not isinstance(van_ban, str):
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")
    du_lieu = [bit for byte in van_ban.encode("utf-8") for bit in so_sang_mang(byte, 8)]
    do_dai_ban_dau = len(du_lieu)
    if do_dai_ban_dau >= 2 ** do_dai_truong:
        raise ValueError("Dữ liệu vượt quá độ dài mà chuẩn SHA cho phép.")
    du_lieu.append(1)
    du_lieu.extend([0] * ((do_dai_khoi - do_dai_truong - len(du_lieu)) % do_dai_khoi))
    du_lieu.extend(so_sang_mang(do_dai_ban_dau, do_dai_truong))
    return du_lieu


def bam_sha1(van_ban: str) -> str:
    du_lieu = dem_du_lieu(van_ban, 512, 64)
    trang_thai = [so_sang_mang(so, 32) for so in [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]]
    bang_k = [so_sang_mang(so, 32) for so in [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6]]
    for dau_khoi in range(0, len(du_lieu), 512):
        khoi = du_lieu[dau_khoi:dau_khoi + 512]
        lich_tu = [khoi[i:i + 32] for i in range(0, 512, 32)]
        for i in range(16, 80):
            lich_tu.append(xoay_trai(xor(lich_tu[i - 3], lich_tu[i - 8], lich_tu[i - 14], lich_tu[i - 16]), 1))
        a, b, c, d, e = trang_thai
        for i in range(80):
            if i < 20:
                f = chon(b, c, d)
            elif i < 40 or i >= 60:
                f = xor(b, c, d)
            else:
                f = da_so(b, c, d)
            a_moi = cong(xoay_trai(a, 5), f, e, bang_k[i // 20], lich_tu[i])
            a, b, c, d, e = a_moi, a, xoay_trai(b, 30), c, d
        trang_thai = [cong(cu, moi) for cu, moi in zip(trang_thai, [a, b, c, d, e])]
    return "".join(f"{mang_sang_so(tu):08x}" for tu in trang_thai)


def bam_sha2(van_ban: str, do_dai_tu: int) -> str:
    if do_dai_tu == 32:
        gia_tri_dau = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
        hang_so = BANG_K_256
        sigma_nho_0, sigma_nho_1 = (7, 18, 3), (17, 19, 10)
        sigma_lon_0, sigma_lon_1 = (2, 13, 22), (6, 11, 25)
    elif do_dai_tu == 64:
        gia_tri_dau = [
            0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
            0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
        ]
        hang_so = BANG_K_512
        sigma_nho_0, sigma_nho_1 = (1, 8, 7), (19, 61, 6)
        sigma_lon_0, sigma_lon_1 = (28, 34, 39), (14, 18, 41)
    else:
        raise ValueError("Một từ SHA-2 phải dài 32 hoặc 64 phần tử.")

    do_dai_khoi = do_dai_tu * 16
    du_lieu = dem_du_lieu(van_ban, do_dai_khoi, do_dai_tu * 2)
    trang_thai = [so_sang_mang(so, do_dai_tu) for so in gia_tri_dau]
    bang_k = [so_sang_mang(so, do_dai_tu) for so in hang_so]
    for dau_khoi in range(0, len(du_lieu), do_dai_khoi):
        khoi = du_lieu[dau_khoi:dau_khoi + do_dai_khoi]
        lich_tu = [khoi[i:i + do_dai_tu] for i in range(0, do_dai_khoi, do_dai_tu)]
        for i in range(16, len(bang_k)):
            x, y = lich_tu[i - 15], lich_tu[i - 2]
            s0 = xor(xoay_phai(x, sigma_nho_0[0]), xoay_phai(x, sigma_nho_0[1]), dich_phai(x, sigma_nho_0[2]))
            s1 = xor(xoay_phai(y, sigma_nho_1[0]), xoay_phai(y, sigma_nho_1[1]), dich_phai(y, sigma_nho_1[2]))
            lich_tu.append(cong(lich_tu[i - 16], s0, lich_tu[i - 7], s1))
        a, b, c, d, e, f, g, h = trang_thai
        for i in range(len(bang_k)):
            s1 = xor(*(xoay_phai(e, buoc) for buoc in sigma_lon_1))
            t1 = cong(h, s1, chon(e, f, g), bang_k[i], lich_tu[i])
            s0 = xor(*(xoay_phai(a, buoc) for buoc in sigma_lon_0))
            t2 = cong(s0, da_so(a, b, c))
            a, b, c, d, e, f, g, h = cong(t1, t2), a, b, c, cong(d, t1), e, f, g
        trang_thai = [cong(cu, moi) for cu, moi in zip(trang_thai, [a, b, c, d, e, f, g, h])]
    return "".join(f"{mang_sang_so(tu):0{do_dai_tu // 4}x}" for tu in trang_thai)


def bam_sha256(van_ban: str) -> str:
    return bam_sha2(van_ban, 32)


def bam_sha512(van_ban: str) -> str:
    return bam_sha2(van_ban, 64)


if __name__ == "__main__":
    van_ban = "Xin chào Python!"
    assert bam_sha1("abc") == "a9993e364706816aba3e25717850c26c9cd0d89d"
    assert bam_sha256("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert bam_sha512("abc") == (
        "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a"
        "2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f"
    )
    print("Văn bản:", van_ban)
    print("SHA-1 (160 bit, 40 ký tự hex):", bam_sha1(van_ban))
    print("SHA-256 (256 bit, 64 ký tự hex):", bam_sha256(van_ban))
    print("SHA-512 (512 bit, 128 ký tự hex):", bam_sha512(van_ban))
    print("Băm là một chiều: không có hàm giải mã.")
