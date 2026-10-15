"""AES-128 để học: ECB + PKCS#7; không dùng để bảo vệ dữ liệu thực tế."""  # ECB xử lý độc lập từng khối nên làm lộ các khối lặp.

SBOX = [  # Bảng thay thế byte cố định theo chuẩn AES, tra bằng giá trị 0..255.
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,  # Đầu vào 00..0F.
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,  # Đầu vào 10..1F.
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,  # Đầu vào 20..2F.
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,  # Đầu vào 30..3F.
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,  # Đầu vào 40..4F.
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,  # Đầu vào 50..5F.
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,  # Đầu vào 60..6F.
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,  # Đầu vào 70..7F.
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,  # Đầu vào 80..8F.
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,  # Đầu vào 90..9F.
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,  # Đầu vào A0..AF.
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,  # Đầu vào B0..BF.
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,  # Đầu vào C0..CF.
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,  # Đầu vào D0..DF.
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,  # Đầu vào E0..EF.
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,  # Đầu vào F0..FF.
]  # Kết thúc 256 phần tử của S-box chuẩn.

SBOX_NGUOC = [0] * 256  # Dành chỗ cho bảng đảo, phục vụ bước giải mã.
for gia_tri in range(256):  # Xét mọi byte có thể xuất hiện.
    SBOX_NGUOC[SBOX[gia_tri]] = gia_tri  # Nếu S-box biến x thành y thì bảng ngược biến y về x.


def _nhan_gf(a: int, b: int) -> int:  # Nhân hai byte trong trường hữu hạn GF(2^8) của AES.
    ket_qua = 0  # Chưa cộng đa thức thành phần nào.
    for _ in range(8):  # Byte b có đúng tám bit cần xét.
        if b & 1:  # & 1 kiểm tra bit thấp nhất của b có bằng 1 không.
            ket_qua ^= a  # ^ là XOR; phép cộng trong GF(2^8) dùng XOR thay cho cộng thường.
        bit_cao = a & 0x80  # Ghi nhớ bit 7 trước khi dịch, để biết có phải rút gọn đa thức không.
        a = (a << 1) & 0xFF  # << 1 nhân đa thức với x; & 0xFF chỉ giữ một byte.
        if bit_cao:  # Nếu phép dịch vượt tám bit thì phải rút gọn theo đa thức AES.
            a ^= 0x1B  # XOR phần thấp của đa thức x^8 + x^4 + x^3 + x + 1.
        b >>= 1  # >> 1 bỏ bit đã xét, đưa bit tiếp theo xuống cuối.
    return ket_qua  # Tích vẫn là một byte 0..255.


def _tao_khoa_vong(khoa: bytes) -> list[list[int]]:  # Mở rộng khóa AES-128 thành 11 khóa vòng 16 byte.
    cac_tu = []  # Mỗi từ gồm bốn byte; cần tổng cộng 44 từ.
    for vi_tri in range(0, 16, 4):  # Chia khóa gốc thành bốn từ liên tiếp.
        cac_tu.append(list(khoa[vi_tri:vi_tri + 4]))  # Chuyển mỗi từ sang list để tiện XOR từng byte.
    rcon = 1  # Hằng số vòng đầu tiên trong phép mở rộng khóa.
    while len(cac_tu) < 44:  # Sinh thêm từ cho đến khi đủ 11 khóa vòng.
        tu = cac_tu[-1][:]  # Sao chép từ liền trước để không sửa từ đã lưu.
        if len(cac_tu) % 4 == 0:  # Cứ mỗi bốn từ thì áp dụng biến đổi đặc biệt.
            tu = tu[1:] + tu[:1]  # RotWord: dịch vòng trái một byte.
            for chi_so in range(4):  # Thay thế cả bốn byte của từ.
                tu[chi_so] = SBOX[tu[chi_so]]  # SubWord: tra S-box cho từng byte.
            tu[0] ^= rcon  # XOR hằng số vòng vào byte đầu tiên.
            rcon = _nhan_gf(rcon, 2)  # Tính hằng số cho vòng mở rộng kế tiếp.
        tu_moi = []  # Chuẩn bị từ mới gồm bốn byte.
        for chi_so in range(4):  # XOR từ cách bốn vị trí với từ đã biến đổi.
            tu_moi.append(cac_tu[-4][chi_so] ^ tu[chi_so])  # Mỗi byte mới là XOR của hai byte tương ứng.
        cac_tu.append(tu_moi)  # Thêm từ mới để tiếp tục vòng lặp.
    cac_khoa_vong = []  # Sẽ có khóa vòng 0, 1, ..., 10.
    for vi_tri in range(0, 44, 4):  # Cứ bốn từ ghép thành một khóa 16 byte.
        khoa_vong = []  # Khóa vòng hiện tại chưa có byte nào.
        for tu in cac_tu[vi_tri:vi_tri + 4]:  # Đọc bốn từ theo đúng thứ tự đã sinh.
            khoa_vong.extend(tu)  # Nối bốn byte của từ vào khóa vòng.
        cac_khoa_vong.append(khoa_vong)  # Lưu khóa vòng đã đủ 16 byte.
    return cac_khoa_vong  # Trả 11 khóa cho AddRoundKey.


def _them_khoa(trang_thai: list[int], khoa_vong: list[int]) -> None:  # AddRoundKey sửa trực tiếp trạng thái.
    for chi_so in range(16):  # Trạng thái và khóa vòng đều có 16 byte.
        trang_thai[chi_so] ^= khoa_vong[chi_so]  # XOR từng byte trạng thái với byte khóa cùng vị trí.


def _thay_byte(trang_thai: list[int], nguoc: bool = False) -> None:  # SubBytes hoặc InvSubBytes tùy chiều xử lý.
    bang = SBOX_NGUOC if nguoc else SBOX  # Chọn bảng thay thế thuận hoặc bảng ngược.
    for chi_so in range(16):  # Mỗi byte được thay thế độc lập.
        trang_thai[chi_so] = bang[trang_thai[chi_so]]  # Dùng giá trị byte làm chỉ số tra bảng.


def _dich_hang(trang_thai: list[int], nguoc: bool = False) -> None:  # ShiftRows dịch hàng trong ma trận 4x4.
    ban_cu = trang_thai[:]  # Sao chép để các phép gán không làm mất byte chưa dùng.
    for hang in range(4):  # Hàng 0 giữ nguyên; các hàng 1, 2, 3 dịch lần lượt 1, 2, 3 ô.
        for cot in range(4):  # Xác định byte nguồn cho từng cột đích.
            cot_nguon = (cot - hang if nguoc else cot + hang) % 4  # Mã hóa dịch trái, giải mã dịch phải theo vòng tròn.
            trang_thai[4 * cot + hang] = ban_cu[4 * cot_nguon + hang]  # AES lưu theo cột: chỉ số = 4*cột + hàng.


def _tron_cot(trang_thai: list[int], nguoc: bool = False) -> None:  # MixColumns nhân mỗi cột với ma trận cố định trên GF(2^8).
    he_so = (14, 11, 13, 9) if nguoc else (2, 3, 1, 1)  # Hàng đầu của ma trận nghịch đảo hoặc ma trận thuận.
    for cot in range(4):  # Xử lý riêng từng cột của trạng thái AES.
        vi_tri = 4 * cot  # Mỗi cột chiếm bốn byte liên tiếp trong list.
        gia_tri = trang_thai[vi_tri:vi_tri + 4]  # Giữ bản cũ của cột để tính đủ bốn byte mới.
        for hang in range(4):  # Mỗi hàng của ma trận nhân cho ra một byte mới.
            ket_qua = 0  # Khởi tạo tổng GF bằng 0.
            for chi_so in range(4):  # Cộng bốn tích bằng XOR.
                he_so_hien_tai = he_so[(chi_so - hang) % 4]  # Các hàng sau của ma trận là dịch vòng hàng hệ số đầu.
                ket_qua ^= _nhan_gf(gia_tri[chi_so], he_so_hien_tai)  # Nhân byte trong GF rồi XOR vào tổng.
            trang_thai[vi_tri + hang] = ket_qua  # Ghi byte mới vào đúng hàng của cột.


def _bien_doi_khoi(khoi: bytes, cac_khoa_vong: list[list[int]], giai: bool) -> bytes:  # Lõi xử lý một khối AES-128.
    trang_thai = list(khoi)  # 16 byte xếp theo cột: byte 0..3 là cột đầu của ma trận 4x4.
    if giai:  # Nhánh giải mã đảo các bước và đảo thứ tự khóa vòng.
        _them_khoa(trang_thai, cac_khoa_vong[10])  # Bỏ khóa đã được thêm ở vòng mã hóa cuối.
        for vong in range(9, 0, -1):  # Duyệt vòng 9 đến 1 theo thứ tự giảm dần.
            _dich_hang(trang_thai, nguoc=True)  # Đảo phép ShiftRows của vòng mã hóa tương ứng.
            _thay_byte(trang_thai, nguoc=True)  # Đảo phép SubBytes bằng S-box ngược.
            _them_khoa(trang_thai, cac_khoa_vong[vong])  # XOR lại cùng khóa để loại khóa vòng.
            _tron_cot(trang_thai, nguoc=True)  # Nhân ma trận nghịch đảo để đảo MixColumns.
        _dich_hang(trang_thai, nguoc=True)  # Đảo ShiftRows của vòng đầu còn lại.
        _thay_byte(trang_thai, nguoc=True)  # Đảo SubBytes của vòng đầu còn lại.
        _them_khoa(trang_thai, cac_khoa_vong[0])  # Bỏ khóa ban đầu để thu lại bản rõ.
    else:  # Nhánh mã hóa AES-128 có 10 vòng.
        _them_khoa(trang_thai, cac_khoa_vong[0])  # Thêm khóa gốc trước vòng mã hóa thứ nhất.
        for vong in range(1, 10):  # Chín vòng đầu có đủ bốn bước biến đổi.
            _thay_byte(trang_thai)  # SubBytes thay từng byte qua S-box.
            _dich_hang(trang_thai)  # ShiftRows dịch vòng các hàng.
            _tron_cot(trang_thai)  # MixColumns trộn các byte trong từng cột.
            _them_khoa(trang_thai, cac_khoa_vong[vong])  # AddRoundKey trộn khóa của vòng hiện tại.
        _thay_byte(trang_thai)  # Bắt đầu vòng thứ 10 với SubBytes.
        _dich_hang(trang_thai)  # ShiftRows của vòng thứ 10; vòng này không có MixColumns.
        _them_khoa(trang_thai, cac_khoa_vong[10])  # Thêm khóa vòng cuối để hoàn tất mã hóa.
    return bytes(trang_thai)  # Trả khối kết quả đúng 16 byte.


def _kiem_tra_khoa(khoa: bytes) -> None:  # Phiên bản này chỉ triển khai AES-128.
    if not isinstance(khoa, bytes) or len(khoa) != 16:  # Khóa AES-128 phải là đúng 128 bit = 16 byte.
        raise ValueError("Khóa AES-128 phải là bytes có đúng 16 byte.")  # Không tự chuyển chuỗi hay đoán định dạng khóa.


def ma_hoa_khoi(khoi: bytes, khoa: bytes) -> bytes:  # Mã hóa một khối 16 byte, không thêm đệm.
    _kiem_tra_khoa(khoa)  # Chặn khóa sai trước khi mở rộng khóa.
    if not isinstance(khoi, bytes) or len(khoi) != 16:  # AES luôn dùng khối 128 bit dù độ dài khóa có thể khác.
        raise ValueError("Khối AES phải là bytes có đúng 16 byte.")  # Từ chối khối chưa đủ hoặc vượt 16 byte.
    return _bien_doi_khoi(khoi, _tao_khoa_vong(khoa), False)  # False chọn chiều mã hóa của lõi AES.


def giai_ma_khoi(khoi: bytes, khoa: bytes) -> bytes:  # Giải mã một khối 16 byte, không bỏ đệm.
    _kiem_tra_khoa(khoa)  # Khóa có cùng yêu cầu như khi mã hóa.
    if not isinstance(khoi, bytes) or len(khoi) != 16:  # Lõi AES cần đúng một khối đầy đủ.
        raise ValueError("Khối AES phải là bytes có đúng 16 byte.")  # Báo lỗi trước khi truy cập các vị trí của khối.
    return _bien_doi_khoi(khoi, _tao_khoa_vong(khoa), True)  # True chọn chiều giải mã của lõi AES.


def ma_hoa(van_ban: str, khoa: bytes) -> str:  # Mã hóa văn bản UTF-8 thành chuỗi hex bằng AES-128 ECB.
    _kiem_tra_khoa(khoa)  # Kiểm tra khóa trước khi xử lý văn bản.
    du_lieu = van_ban.encode("utf-8")  # Chuyển tiếng Việt và các ký tự khác sang byte UTF-8.
    so_dem = 16 - len(du_lieu) % 16  # PKCS#7 thêm từ 1 đến 16 byte để đủ khối.
    du_lieu += bytes([so_dem] * so_dem)  # Mỗi byte đệm ghi đúng số byte đệm được thêm.
    cac_khoa_vong = _tao_khoa_vong(khoa)  # Dùng chung một bộ khóa vòng cho mọi khối.
    ket_qua = bytearray()  # Nối bản mã của các khối vào bộ đệm.
    for vi_tri in range(0, len(du_lieu), 16):  # Chia dữ liệu thành các khối 16 byte độc lập theo ECB.
        khoi = du_lieu[vi_tri:vi_tri + 16]  # Lấy một khối đã đủ byte nhờ đệm.
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_vong, False))  # Mã hóa rồi nối khối vào kết quả.
    return ket_qua.hex().upper()  # Trả bản mã hex dạng chữ hoa để dễ xem.


def giai_ma(ban_ma_hex: str, khoa: bytes) -> str:  # Giải mã hex, bỏ đệm hợp lệ và đọc văn bản UTF-8.
    _kiem_tra_khoa(khoa)  # Chặn khóa không phải 16 byte.
    du_lieu = bytes.fromhex(ban_ma_hex)  # Hex sai định dạng làm Python phát sinh ValueError.
    if not du_lieu or len(du_lieu) % 16 != 0:  # Bản mã PKCS#7 phải có ít nhất một khối đầy đủ.
        raise ValueError("Bản mã AES phải có độ dài dương và chia hết cho 16 byte.")  # Không nhận bản mã thiếu byte.
    cac_khoa_vong = _tao_khoa_vong(khoa)  # Mở rộng khóa gốc một lần cho toàn bộ bản mã.
    ket_qua = bytearray()  # Gom các khối đã giải mã, kể cả phần đệm cuối.
    for vi_tri in range(0, len(du_lieu), 16):  # Duyệt mỗi khối bản mã AES.
        khoi = du_lieu[vi_tri:vi_tri + 16]  # Tách khối 16 byte hiện tại.
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_vong, True))  # Giải mã khối và nối vào bộ đệm.
    so_dem = ket_qua[-1]  # Byte cuối cho biết số byte đệm phải bỏ.
    if not 1 <= so_dem <= 16:  # Số byte đệm phải từ 1 đến kích thước khối AES.
        raise ValueError("Đệm PKCS#7 AES không hợp lệ; có thể sai khóa hoặc bản mã.")  # Từ chối dữ liệu sai thay vì trả hex thay thế.
    if ket_qua[-so_dem:] != bytes([so_dem] * so_dem):  # Kiểm tra mọi byte đệm đều có cùng giá trị.
        raise ValueError("Đệm PKCS#7 AES không hợp lệ; có thể sai khóa hoặc bản mã.")  # Không bỏ nhầm dữ liệu khi phần đệm bị hỏng.
    return ket_qua[:-so_dem].decode("utf-8")  # Bỏ đúng đệm, giữ nguyên khoảng trắng và giải mã UTF-8.


if __name__ == "__main__":  # Ví dụ chỉ chạy khi gọi trực tiếp file.
    van_ban = "Xin chào AES!"  # Sửa văn bản tại đây để thử tiếng Việt hay nhiều khối.
    khoa = b"1234567890abcdef"  # Khóa mẫu có đúng 16 byte; không dùng khóa mẫu cho dữ liệu thực.
    ban_ma = ma_hoa(van_ban, khoa)  # Mã hóa UTF-8 với đệm PKCS#7.
    ban_ro = giai_ma(ban_ma, khoa)  # Khôi phục văn bản bằng cùng khóa.
    print("Bản rõ:", van_ban)  # In dữ liệu đầu vào.
    print("Bản mã hex:", ban_ma)  # In các byte đã mã hóa dưới dạng hex.
    print("Giải mã:", ban_ro)  # In văn bản giải mã được.
    assert ban_ro == van_ban  # Tự kiểm tra luồng văn bản khôi phục chính xác.
    khoa_mau = bytes.fromhex("000102030405060708090A0B0C0D0E0F")  # Khóa AES-128 trong ví dụ FIPS 197.
    khoi_mau = bytes.fromhex("00112233445566778899AABBCCDDEEFF")  # Khối rõ chuẩn 16 byte, không thêm đệm.
    ma_mau = bytes.fromhex("69C4E0D86A7B0430D8CDB78070B4C55A")  # Kết quả chuẩn để kiểm tra AES độc lập với round-trip.
    assert ma_hoa_khoi(khoi_mau, khoa_mau) == ma_mau  # Kiểm tra mã hóa khớp vector FIPS 197.
    assert giai_ma_khoi(ma_mau, khoa_mau) == khoi_mau  # Kiểm tra giải mã khớp khối rõ chuẩn.
