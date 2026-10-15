"""AES-128 để học: ECB + PKCS#7; không dùng để bảo vệ dữ liệu thực tế."""

SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

SBOX_NGUOC = [0] * 256
for gia_tri in range(256):
    SBOX_NGUOC[SBOX[gia_tri]] = gia_tri


def _nhan_gf(a: int, b: int) -> int:
    ket_qua = 0
    for _ in range(8):
        if b & 1:
            ket_qua ^= a
        bit_cao = a & 0x80
        a = (a << 1) & 0xFF
        if bit_cao:
            a ^= 0x1B
        b >>= 1
    return ket_qua


def _tao_khoa_vong(khoa: bytes) -> list[list[int]]:
    cac_tu = []
    for vi_tri in range(0, 16, 4):
        cac_tu.append(list(khoa[vi_tri:vi_tri + 4]))
    rcon = 1
    while len(cac_tu) < 44:
        tu = cac_tu[-1][:]
        if len(cac_tu) % 4 == 0:
            tu = tu[1:] + tu[:1]
            for chi_so in range(4):
                tu[chi_so] = SBOX[tu[chi_so]]
            tu[0] ^= rcon
            rcon = _nhan_gf(rcon, 2)
        tu_moi = []
        for chi_so in range(4):
            tu_moi.append(cac_tu[-4][chi_so] ^ tu[chi_so])
        cac_tu.append(tu_moi)
    cac_khoa_vong = []
    for vi_tri in range(0, 44, 4):
        khoa_vong = []
        for tu in cac_tu[vi_tri:vi_tri + 4]:
            khoa_vong.extend(tu)
        cac_khoa_vong.append(khoa_vong)
    return cac_khoa_vong


def _them_khoa(trang_thai: list[int], khoa_vong: list[int]) -> None:
    for chi_so in range(16):
        trang_thai[chi_so] ^= khoa_vong[chi_so]


def _thay_byte(trang_thai: list[int], nguoc: bool = False) -> None:
    bang = SBOX_NGUOC if nguoc else SBOX
    for chi_so in range(16):
        trang_thai[chi_so] = bang[trang_thai[chi_so]]


def _dich_hang(trang_thai: list[int], nguoc: bool = False) -> None:
    ban_cu = trang_thai[:]
    for hang in range(4):
        for cot in range(4):
            cot_nguon = (cot - hang if nguoc else cot + hang) % 4
            trang_thai[4 * cot + hang] = ban_cu[4 * cot_nguon + hang]


def _tron_cot(trang_thai: list[int], nguoc: bool = False) -> None:
    he_so = (14, 11, 13, 9) if nguoc else (2, 3, 1, 1)
    for cot in range(4):
        vi_tri = 4 * cot
        gia_tri = trang_thai[vi_tri:vi_tri + 4]
        for hang in range(4):
            ket_qua = 0
            for chi_so in range(4):
                he_so_hien_tai = he_so[(chi_so - hang) % 4]
                ket_qua ^= _nhan_gf(gia_tri[chi_so], he_so_hien_tai)
            trang_thai[vi_tri + hang] = ket_qua


def _bien_doi_khoi(khoi: bytes, cac_khoa_vong: list[list[int]], giai: bool) -> bytes:
    trang_thai = list(khoi)
    if giai:
        _them_khoa(trang_thai, cac_khoa_vong[10])
        for vong in range(9, 0, -1):
            _dich_hang(trang_thai, nguoc=True)
            _thay_byte(trang_thai, nguoc=True)
            _them_khoa(trang_thai, cac_khoa_vong[vong])
            _tron_cot(trang_thai, nguoc=True)
        _dich_hang(trang_thai, nguoc=True)
        _thay_byte(trang_thai, nguoc=True)
        _them_khoa(trang_thai, cac_khoa_vong[0])
    else:
        _them_khoa(trang_thai, cac_khoa_vong[0])
        for vong in range(1, 10):
            _thay_byte(trang_thai)
            _dich_hang(trang_thai)
            _tron_cot(trang_thai)
            _them_khoa(trang_thai, cac_khoa_vong[vong])
        _thay_byte(trang_thai)
        _dich_hang(trang_thai)
        _them_khoa(trang_thai, cac_khoa_vong[10])
    return bytes(trang_thai)


def _kiem_tra_khoa(khoa: bytes) -> None:
    if not isinstance(khoa, bytes) or len(khoa) != 16:
        raise ValueError("Khóa AES-128 phải là bytes có đúng 16 byte.")


def ma_hoa_khoi(khoi: bytes, khoa: bytes) -> bytes:
    _kiem_tra_khoa(khoa)
    if not isinstance(khoi, bytes) or len(khoi) != 16:
        raise ValueError("Khối AES phải là bytes có đúng 16 byte.")
    return _bien_doi_khoi(khoi, _tao_khoa_vong(khoa), False)


def giai_ma_khoi(khoi: bytes, khoa: bytes) -> bytes:
    _kiem_tra_khoa(khoa)
    if not isinstance(khoi, bytes) or len(khoi) != 16:
        raise ValueError("Khối AES phải là bytes có đúng 16 byte.")
    return _bien_doi_khoi(khoi, _tao_khoa_vong(khoa), True)


def ma_hoa(van_ban: str, khoa: bytes) -> str:
    _kiem_tra_khoa(khoa)
    du_lieu = van_ban.encode("utf-8")
    so_dem = 16 - len(du_lieu) % 16
    du_lieu += bytes([so_dem] * so_dem)
    cac_khoa_vong = _tao_khoa_vong(khoa)
    ket_qua = bytearray()
    for vi_tri in range(0, len(du_lieu), 16):
        khoi = du_lieu[vi_tri:vi_tri + 16]
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_vong, False))
    return ket_qua.hex().upper()


def giai_ma(ban_ma_hex: str, khoa: bytes) -> str:
    _kiem_tra_khoa(khoa)
    du_lieu = bytes.fromhex(ban_ma_hex)
    if not du_lieu or len(du_lieu) % 16 != 0:
        raise ValueError("Bản mã AES phải có độ dài dương và chia hết cho 16 byte.")
    cac_khoa_vong = _tao_khoa_vong(khoa)
    ket_qua = bytearray()
    for vi_tri in range(0, len(du_lieu), 16):
        khoi = du_lieu[vi_tri:vi_tri + 16]
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_vong, True))
    so_dem = ket_qua[-1]
    if not 1 <= so_dem <= 16:
        raise ValueError("Đệm PKCS#7 AES không hợp lệ; có thể sai khóa hoặc bản mã.")
    if ket_qua[-so_dem:] != bytes([so_dem] * so_dem):
        raise ValueError("Đệm PKCS#7 AES không hợp lệ; có thể sai khóa hoặc bản mã.")
    return ket_qua[:-so_dem].decode("utf-8")


if __name__ == "__main__":
    van_ban = "Xin chào AES!"
    khoa = b"1234567890abcdef"
    ban_ma = ma_hoa(van_ban, khoa)
    ban_ro = giai_ma(ban_ma, khoa)
    print("Bản rõ:", van_ban)
    print("Bản mã hex:", ban_ma)
    print("Giải mã:", ban_ro)
    assert ban_ro == van_ban
    khoa_mau = bytes.fromhex("000102030405060708090A0B0C0D0E0F")
    khoi_mau = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
    ma_mau = bytes.fromhex("69C4E0D86A7B0430D8CDB78070B4C55A")
    assert ma_hoa_khoi(khoi_mau, khoa_mau) == ma_mau
    assert giai_ma_khoi(ma_mau, khoa_mau) == khoi_mau
