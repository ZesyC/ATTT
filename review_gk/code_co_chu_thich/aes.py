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


def _byte_thanh_bits(gia_tri: int) -> list[int]:  # Đổi một byte thành mảng tám số 0 hoặc 1, không dùng dịch bit.
    """Ví dụ 6 thành [0, 0, 0, 0, 0, 1, 1, 0], bit cao ở đầu."""  # Giữ bit cao ở đầu mảng để đọc giống cách viết nhị phân.
    bits = [0] * 8  # Khởi tạo đủ tám vị trí, kể cả các số 0 ở đầu.
    for vi_tri in range(7, -1, -1):  # Điền từ phải sang trái, bắt đầu ở bit thấp nhất.
        bits[vi_tri] = gia_tri % 2  # Phần dư khi chia 2 là chữ số nhị phân cuối cùng.
        gia_tri //= 2  # Chia nguyên cho 2 để bỏ chữ số vừa lấy.
    return bits  # Trả mảng tám bit từ cao xuống thấp.


def _bits_thanh_byte(bits: list[int]) -> int:  # Đổi mảng bit từ cao xuống thấp về giá trị một byte.
    gia_tri = 0  # Chưa đọc chữ số nhị phân nào nên bắt đầu bằng 0.
    for bit in bits:  # Đọc lần lượt từ bit đầu tiên đến bit cuối cùng.
        gia_tri = gia_tri * 2 + bit  # Nhân 2 để dành chỗ rồi cộng chữ số mới vào cuối.
    return gia_tri  # Trả giá trị số đã ghép từ các bit.


def _xor_byte(a: int, b: int) -> int:  # Tự tính XOR hai byte bằng mảng; hai bit khác nhau cho kết quả 1.
    bits_a = _byte_thanh_bits(a)  # Tách byte thứ nhất thành tám bit.
    bits_b = _byte_thanh_bits(b)  # Tách byte thứ hai thành tám bit cùng thứ tự.
    ket_qua = []  # Tạo mảng để chứa từng bit kết quả.
    for vi_tri in range(8):  # Xét từng cặp bit cùng vị trí.
        ket_qua.append((bits_a[vi_tri] + bits_b[vi_tri]) % 2)  # Cộng modulo 2: 0+0 và 1+1 thành 0, 0+1 và 1+0 thành 1.
    return _bits_thanh_byte(ket_qua)  # Ghép tám bit kết quả thành một byte.


def _nhan_gf(a: int, b: int) -> int:  # Tự nhân hai byte theo trường GF(2^8), không dùng toán tử bit.
    """Nhân đa thức nhị phân rồi chia dư cho x^8 + x^4 + x^3 + x + 1."""  # Mỗi byte biểu diễn một đa thức với hệ số chỉ nhận 0 hoặc 1.
    da_thuc_a = _byte_thanh_bits(a)  # Hệ số của a theo thứ tự x^7, x^6, ..., x^0.
    da_thuc_b = _byte_thanh_bits(b)  # Hệ số của b cũng theo thứ tự từ bậc cao xuống thấp.
    tich = [0] * 15  # Hai đa thức bậc 7 nhân nhau cho tối đa 15 hệ số, từ bậc 14 đến 0.
    for i in range(8):  # Chọn một hệ số của đa thức thứ nhất.
        for j in range(8):  # Nhân với từng hệ số của đa thức thứ hai.
            tich[i + j] = (tich[i + j] + da_thuc_a[i] * da_thuc_b[j]) % 2  # Nhân chập hệ số: bậc cộng với nhau, hệ số được cộng modulo 2.
    da_thuc_aes = [1, 0, 0, 0, 1, 1, 0, 1, 1]  # Mảng hệ số của x^8 + x^4 + x^3 + x + 1, từ bậc 8 xuống bậc 0.
    for vi_tri in range(7):  # Khử lần lượt các hạng từ bậc 14 xuống bậc 8 như phép chia đa thức.
        if tich[vi_tri] == 1:  # Chỉ cần khử nếu hệ số đầu đoạn đang xét bằng 1.
            for chi_so in range(9):  # Đặt đủ chín hệ số của đa thức chia vào đúng đoạn hiện tại.
                tich[vi_tri + chi_so] = (tich[vi_tri + chi_so] + da_thuc_aes[chi_so]) % 2  # Cộng modulo 2 để triệt tiêu hệ số đầu và cập nhật các hệ số còn lại.
    return _bits_thanh_byte(tich[7:])  # Phần dư chỉ còn tám hệ số bậc 7 đến 0, ghép lại thành một byte.


def _tao_ma_tran(du_lieu: bytes) -> list[list[int]]:  # Đổi khối 16 byte thành ma trận 4 hàng × 4 cột.
    """AES xếp 16 byte theo cột: cột đầu chứa byte 0, 1, 2, 3."""  # Chuẩn AES nạp dữ liệu lần lượt theo từng cột, không theo từng hàng.
    ma_tran = []  # Chuẩn bị ma trận rỗng.
    for hang in range(4):  # Tạo bốn hàng riêng biệt để tránh các hàng dùng chung một list.
        ma_tran.append([0] * 4)  # Mỗi hàng có bốn ô ban đầu bằng 0.
    for cot in range(4):  # Lần lượt nạp bốn cột dữ liệu.
        for hang in range(4):  # Mỗi cột nhận bốn byte, từ hàng 0 đến hàng 3.
            ma_tran[hang][cot] = du_lieu[4 * cot + hang]  # Byte thứ 4*cột+hàng được đưa vào đúng ô [hàng][cột].
    return ma_tran  # Trả ma trận để các bước AES thao tác trực tiếp theo hàng và cột.


def _tao_khoa_vong(khoa: bytes) -> list[list[list[int]]]:  # Mở rộng khóa AES-128 thành 11 ma trận khóa vòng 4×4.
    cac_tu = []  # Danh sách chứa 44 từ, mỗi từ gồm bốn byte.
    for vi_tri in range(0, 16, 4):  # Đọc khóa gốc theo từng nhóm bốn byte.
        cac_tu.append(list(khoa[vi_tri:vi_tri + 4]))  # Lưu bốn nhóm đầu làm bốn từ ban đầu.
    rcon = 1  # Hằng số mở rộng khóa đầu tiên bằng 1.
    while len(cac_tu) < 44:  # Sinh từ mới cho đến khi đủ 44 từ.
        tu = cac_tu[-1][:]  # Sao chép từ cuối để không sửa dữ liệu đã lưu.
        if len(cac_tu) % 4 == 0:  # Mỗi khi bắt đầu nhóm bốn từ thì thực hiện biến đổi đặc biệt.
            tu = tu[1:] + tu[:1]  # RotWord: đưa byte đầu sang cuối từ bằng cách cắt và nối mảng.
            for chi_so in range(4):  # Duyệt cả bốn byte của từ vừa xoay.
                tu[chi_so] = SBOX[tu[chi_so]]  # SubWord: thay từng byte bằng giá trị tra S-box chuẩn.
            tu[0] = _xor_byte(tu[0], rcon)  # XOR byte đầu với hằng số vòng qua hàm xử lý mảng bit.
            rcon = _nhan_gf(rcon, 2)  # Nhân hằng số với 2 trong GF(2^8) để chuẩn bị vòng sau.
        tu_moi = []  # Chuẩn bị từ mới gồm bốn byte.
        for chi_so in range(4):  # Duyệt các vị trí tương ứng của hai từ.
            tu_moi.append(_xor_byte(cac_tu[-4][chi_so], tu[chi_so]))  # XOR với từ đứng trước bốn vị trí để sinh từng byte mới.
        cac_tu.append(tu_moi)  # Lưu từ mới để dùng cho các lần sinh tiếp theo.
    cac_khoa_vong = []  # Danh sách kết quả sẽ chứa 11 ma trận khóa vòng.
    for vi_tri in range(0, 44, 4):  # Ghép mỗi bốn từ liên tiếp thành một ma trận khóa.
        khoa_vong = []  # Chuẩn bị ma trận khóa vòng hiện tại.
        for hang in range(4):  # Xây dựng lần lượt bốn hàng của ma trận khóa.
            hang_khoa = []  # Tạo mảng riêng chứa một hàng khóa.
            for cot in range(4):  # Lấy một byte từ mỗi từ tương ứng với bốn cột.
                hang_khoa.append(cac_tu[vi_tri + cot][hang])  # Từ thứ cột trở thành cột của ma trận khóa, byte thứ hàng trở thành hàng.
            khoa_vong.append(hang_khoa)  # Thêm hàng đã đủ bốn ô vào khóa vòng.
        cac_khoa_vong.append(khoa_vong)  # Lưu ma trận khóa vòng đã hoàn chỉnh.
    return cac_khoa_vong  # Trả khóa vòng 0 đến 10, mỗi khóa có kích thước 4×4.


def _them_khoa(trang_thai: list[list[int]], khoa_vong: list[list[int]]) -> None:  # AddRoundKey: kết hợp ma trận trạng thái và ma trận khóa cùng kích thước.
    for hang in range(4):  # Duyệt từng hàng của trạng thái.
        for cot in range(4):  # Duyệt từng cột trong hàng hiện tại.
            trang_thai[hang][cot] = _xor_byte(trang_thai[hang][cot], khoa_vong[hang][cot])  # XOR hai byte ở cùng ô bằng hàm tự viết trên mảng bit.


def _thay_byte(trang_thai: list[list[int]], nguoc: bool = False) -> None:  # SubBytes hoặc InvSubBytes: thay từng ô của ma trận qua bảng chuẩn.
    bang = SBOX_NGUOC if nguoc else SBOX  # Giải mã dùng S-box ngược, mã hóa dùng S-box thuận.
    for hang in range(4):  # Duyệt bốn hàng của ma trận.
        for cot in range(4):  # Duyệt bốn byte trong hàng.
            trang_thai[hang][cot] = bang[trang_thai[hang][cot]]  # Lấy byte trong ô làm chỉ số tra bảng và ghi lại ô đó.


def _dich_hang(trang_thai: list[list[int]], nguoc: bool = False) -> None:  # ShiftRows: dịch vòng trên từng mảng hàng của trạng thái 4×4.
    for hang in range(1, 4):  # Hàng 0 giữ nguyên; hàng 1, 2, 3 dịch lần lượt 1, 2, 3 vị trí.
        dong = trang_thai[hang]  # Lấy mảng byte của hàng đang xử lý.
        if nguoc:  # Nhánh giải mã dịch sang phải để đảo phép dịch trái.
            trang_thai[hang] = dong[-hang:] + dong[:-hang]  # Cắt các byte cuối đưa lên đầu, nối với phần còn lại.
        else:  # Nhánh mã hóa dịch sang trái.
            trang_thai[hang] = dong[hang:] + dong[:hang]  # Cắt các byte đầu đưa xuống cuối, nối với phần còn lại.


def _tron_cot(trang_thai: list[list[int]], nguoc: bool = False) -> None:  # MixColumns: nhân ma trận hệ số 4×4 với từng cột trạng thái trong GF(2^8).
    if nguoc:  # Giải mã chọn ma trận nghịch đảo của MixColumns.
        ma_tran_he_so = [  # Khai báo trực tiếp ma trận nghịch đảo để dễ đối chiếu công thức.
            [14, 11, 13, 9],  # Hàng thứ nhất của ma trận nghịch đảo.
            [9, 14, 11, 13],  # Hàng thứ hai của ma trận nghịch đảo.
            [13, 9, 14, 11],  # Hàng thứ ba của ma trận nghịch đảo.
            [11, 13, 9, 14],  # Hàng thứ tư của ma trận nghịch đảo.
        ]  # Kết thúc ma trận nghịch đảo.
    else:  # Mã hóa chọn ma trận MixColumns thuận.
        ma_tran_he_so = [  # Khai báo đủ 16 hệ số của ma trận thuận.
            [2, 3, 1, 1],  # Hàng thứ nhất của ma trận thuận.
            [1, 2, 3, 1],  # Hàng thứ hai của ma trận thuận.
            [1, 1, 2, 3],  # Hàng thứ ba của ma trận thuận.
            [3, 1, 1, 2],  # Hàng thứ tư của ma trận thuận.
        ]  # Kết thúc ma trận thuận.
    for cot in range(4):  # Xử lý độc lập từng cột trạng thái.
        cot_cu = []  # Chuẩn bị bản sao cột để kết quả mới không ghi đè dữ liệu còn cần.
        for hang in range(4):  # Đọc lần lượt bốn byte trong cột hiện tại.
            cot_cu.append(trang_thai[hang][cot])  # Lưu byte cũ ở hàng tương ứng.
        for hang in range(4):  # Tính lần lượt bốn ô mới trong cột.
            ket_qua = 0  # Khởi tạo tổng GF bằng byte 0.
            for chi_so in range(4):  # Nhân hàng của ma trận hệ số với cột trạng thái.
                tich = _nhan_gf(ma_tran_he_so[hang][chi_so], cot_cu[chi_so])  # Mỗi tích dùng phép nhân đa thức rồi rút gọn bằng hàm tự viết.
                ket_qua = _xor_byte(ket_qua, tich)  # Cộng các tích trong GF bằng XOR trên mảng bit.
            trang_thai[hang][cot] = ket_qua  # Ghi byte kết quả về đúng ô [hàng][cột].


def _bien_doi_khoi(khoi: bytes, cac_khoa_vong: list[list[list[int]]], giai: bool) -> bytes:  # Lõi AES xử lý khối 16 byte với các khóa vòng là ma trận 4×4.
    trang_thai = _tao_ma_tran(khoi)  # Nạp khối vào ma trận trạng thái theo thứ tự cột của chuẩn AES.
    if giai:  # Nhánh giải mã đảo thứ tự khóa và các phép biến đổi.
        _them_khoa(trang_thai, cac_khoa_vong[10])  # Bỏ khóa vòng cuối đã thêm khi mã hóa.
        for vong in range(9, 0, -1):  # Giải mã lần lượt từ vòng 9 về vòng 1.
            _dich_hang(trang_thai, nguoc=True)  # Dịch các hàng sang phải để đảo ShiftRows.
            _thay_byte(trang_thai, nguoc=True)  # Thay các byte qua S-box ngược để đảo SubBytes.
            _them_khoa(trang_thai, cac_khoa_vong[vong])  # XOR khóa vòng hiện tại để bỏ phần khóa.
            _tron_cot(trang_thai, nguoc=True)  # Nhân ma trận nghịch đảo để đảo MixColumns.
        _dich_hang(trang_thai, nguoc=True)  # Đảo ShiftRows còn lại của bước đầu.
        _thay_byte(trang_thai, nguoc=True)  # Đảo SubBytes còn lại của bước đầu.
        _them_khoa(trang_thai, cac_khoa_vong[0])  # Bỏ khóa gốc để nhận ma trận bản rõ.
    else:  # Nhánh mã hóa AES-128 gồm 10 vòng.
        _them_khoa(trang_thai, cac_khoa_vong[0])  # Kết hợp khóa gốc với trạng thái trước vòng 1.
        for vong in range(1, 10):  # Chín vòng đầu có đủ SubBytes, ShiftRows, MixColumns và AddRoundKey.
            _thay_byte(trang_thai)  # Thay từng byte của trạng thái qua S-box thuận.
            _dich_hang(trang_thai)  # Dịch vòng trái các hàng bằng thao tác cắt và nối mảng.
            _tron_cot(trang_thai)  # Trộn mỗi cột bằng phép nhân ma trận trong GF(2^8).
            _them_khoa(trang_thai, cac_khoa_vong[vong])  # Kết hợp ma trận khóa của vòng hiện tại.
        _thay_byte(trang_thai)  # Vòng 10 bắt đầu bằng bước thay byte.
        _dich_hang(trang_thai)  # Dịch hàng ở vòng 10; vòng cuối không có MixColumns.
        _them_khoa(trang_thai, cac_khoa_vong[10])  # Kết hợp khóa vòng 10 để hoàn thành mã hóa.
    ket_qua = []  # Chuẩn bị danh sách 16 byte đầu ra.
    for cot in range(4):  # Đọc ma trận theo từng cột, giống thứ tự nạp khối đầu vào.
        for hang in range(4):  # Đọc từ trên xuống dưới trong cột hiện tại.
            ket_qua.append(trang_thai[hang][cot])  # Thêm byte trong ô vào cuối kết quả.
    return bytes(ket_qua)  # Đóng gói danh sách thành khối bytes có độ dài 16.


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
