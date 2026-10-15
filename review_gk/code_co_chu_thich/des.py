"""DES để học: ECB + PKCS#7; không dùng để bảo vệ dữ liệu thực tế."""  # Mô tả mục đích; DES đã lỗi thời và ECB làm lộ các khối lặp.

_DES_IP = [  # Hoán vị đầu: chọn thứ tự 64 bit đầu vào.
    58, 50, 42, 34, 26, 18, 10, 2,  # Các vị trí 1 đến 8 của bảng _DES_IP.
    60, 52, 44, 36, 28, 20, 12, 4,  # Các vị trí 9 đến 16 của bảng _DES_IP.
    62, 54, 46, 38, 30, 22, 14, 6,  # Các vị trí 17 đến 24 của bảng _DES_IP.
    64, 56, 48, 40, 32, 24, 16, 8,  # Các vị trí 25 đến 32 của bảng _DES_IP.
    57, 49, 41, 33, 25, 17, 9, 1,  # Các vị trí 33 đến 40 của bảng _DES_IP.
    59, 51, 43, 35, 27, 19, 11, 3,  # Các vị trí 41 đến 48 của bảng _DES_IP.
    61, 53, 45, 37, 29, 21, 13, 5,  # Các vị trí 49 đến 56 của bảng _DES_IP.
    63, 55, 47, 39, 31, 23, 15, 7,  # Các vị trí 57 đến 64 của bảng _DES_IP.
]  # Kết thúc bảng _DES_IP.

_DES_IP_INV = [  # Hoán vị cuối: đảo ngược hoán vị đầu.
    40, 8, 48, 16, 56, 24, 64, 32,  # Các vị trí 1 đến 8 của bảng _DES_IP_INV.
    39, 7, 47, 15, 55, 23, 63, 31,  # Các vị trí 9 đến 16 của bảng _DES_IP_INV.
    38, 6, 46, 14, 54, 22, 62, 30,  # Các vị trí 17 đến 24 của bảng _DES_IP_INV.
    37, 5, 45, 13, 53, 21, 61, 29,  # Các vị trí 25 đến 32 của bảng _DES_IP_INV.
    36, 4, 44, 12, 52, 20, 60, 28,  # Các vị trí 33 đến 40 của bảng _DES_IP_INV.
    35, 3, 43, 11, 51, 19, 59, 27,  # Các vị trí 41 đến 48 của bảng _DES_IP_INV.
    34, 2, 42, 10, 50, 18, 58, 26,  # Các vị trí 49 đến 56 của bảng _DES_IP_INV.
    33, 1, 41, 9, 49, 17, 57, 25,  # Các vị trí 57 đến 64 của bảng _DES_IP_INV.
]  # Kết thúc bảng _DES_IP_INV.

_DES_PC1 = [  # Chọn 56 bit khóa, bỏ 8 bit kiểm tra chẵn lẻ.
    57, 49, 41, 33, 25, 17, 9,  # Các vị trí 1 đến 7 của bảng _DES_PC1.
    1, 58, 50, 42, 34, 26, 18,  # Các vị trí 8 đến 14 của bảng _DES_PC1.
    10, 2, 59, 51, 43, 35, 27,  # Các vị trí 15 đến 21 của bảng _DES_PC1.
    19, 11, 3, 60, 52, 44, 36,  # Các vị trí 22 đến 28 của bảng _DES_PC1.
    63, 55, 47, 39, 31, 23, 15,  # Các vị trí 29 đến 35 của bảng _DES_PC1.
    7, 62, 54, 46, 38, 30, 22,  # Các vị trí 36 đến 42 của bảng _DES_PC1.
    14, 6, 61, 53, 45, 37, 29,  # Các vị trí 43 đến 49 của bảng _DES_PC1.
    21, 13, 5, 28, 20, 12, 4,  # Các vị trí 50 đến 56 của bảng _DES_PC1.
]  # Kết thúc bảng _DES_PC1.

_DES_PC2 = [  # Chọn 48 bit từ hai nửa khóa 28 bit.
    14, 17, 11, 24, 1, 5,  # Các vị trí 1 đến 6 của bảng _DES_PC2.
    3, 28, 15, 6, 21, 10,  # Các vị trí 7 đến 12 của bảng _DES_PC2.
    23, 19, 12, 4, 26, 8,  # Các vị trí 13 đến 18 của bảng _DES_PC2.
    16, 7, 27, 20, 13, 2,  # Các vị trí 19 đến 24 của bảng _DES_PC2.
    41, 52, 31, 37, 47, 55,  # Các vị trí 25 đến 30 của bảng _DES_PC2.
    30, 40, 51, 45, 33, 48,  # Các vị trí 31 đến 36 của bảng _DES_PC2.
    44, 49, 39, 56, 34, 53,  # Các vị trí 37 đến 42 của bảng _DES_PC2.
    46, 42, 50, 36, 29, 32,  # Các vị trí 43 đến 48 của bảng _DES_PC2.
]  # Kết thúc bảng _DES_PC2.

_DES_SHIFTS = [  # Số bit dịch vòng trái của khóa trong 16 vòng.
    1, 1, 2, 2, 2, 2, 2, 2,  # Các vị trí 1 đến 8 của bảng _DES_SHIFTS.
    1, 2, 2, 2, 2, 2, 2, 1,  # Các vị trí 9 đến 16 của bảng _DES_SHIFTS.
]  # Kết thúc bảng _DES_SHIFTS.

_DES_E = [  # Mở rộng nửa phải từ 32 bit thành 48 bit.
    32, 1, 2, 3, 4, 5,  # Các vị trí 1 đến 6 của bảng _DES_E.
    4, 5, 6, 7, 8, 9,  # Các vị trí 7 đến 12 của bảng _DES_E.
    8, 9, 10, 11, 12, 13,  # Các vị trí 13 đến 18 của bảng _DES_E.
    12, 13, 14, 15, 16, 17,  # Các vị trí 19 đến 24 của bảng _DES_E.
    16, 17, 18, 19, 20, 21,  # Các vị trí 25 đến 30 của bảng _DES_E.
    20, 21, 22, 23, 24, 25,  # Các vị trí 31 đến 36 của bảng _DES_E.
    24, 25, 26, 27, 28, 29,  # Các vị trí 37 đến 42 của bảng _DES_E.
    28, 29, 30, 31, 32, 1,  # Các vị trí 43 đến 48 của bảng _DES_E.
]  # Kết thúc bảng _DES_E.

_DES_P = [  # Hoán vị 32 bit sau bước thay thế S-box.
    16, 7, 20, 21, 29, 12, 28, 17,  # Các vị trí 1 đến 8 của bảng _DES_P.
    1, 15, 23, 26, 5, 18, 31, 10,  # Các vị trí 9 đến 16 của bảng _DES_P.
    2, 8, 24, 14, 32, 27, 3, 9,  # Các vị trí 17 đến 24 của bảng _DES_P.
    19, 13, 30, 6, 22, 11, 4, 25,  # Các vị trí 25 đến 32 của bảng _DES_P.
]  # Kết thúc bảng _DES_P.

_DES_S = [  # Tám S-box; mỗi S-box biến nhóm 6 bit thành 4 bit.
    [  # S-box thứ 1, chứa bốn hàng và mười sáu cột.
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],  # Hàng 0: tra cột 0 đến 15 trong S-box 1.
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],  # Hàng 1: tra cột 0 đến 15 trong S-box 1.
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],  # Hàng 2: tra cột 0 đến 15 trong S-box 1.
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],  # Hàng 3: tra cột 0 đến 15 trong S-box 1.
    ],  # Kết thúc S-box thứ 1.
    [  # S-box thứ 2, chứa bốn hàng và mười sáu cột.
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],  # Hàng 0: tra cột 0 đến 15 trong S-box 2.
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],  # Hàng 1: tra cột 0 đến 15 trong S-box 2.
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],  # Hàng 2: tra cột 0 đến 15 trong S-box 2.
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],  # Hàng 3: tra cột 0 đến 15 trong S-box 2.
    ],  # Kết thúc S-box thứ 2.
    [  # S-box thứ 3, chứa bốn hàng và mười sáu cột.
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],  # Hàng 0: tra cột 0 đến 15 trong S-box 3.
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],  # Hàng 1: tra cột 0 đến 15 trong S-box 3.
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],  # Hàng 2: tra cột 0 đến 15 trong S-box 3.
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],  # Hàng 3: tra cột 0 đến 15 trong S-box 3.
    ],  # Kết thúc S-box thứ 3.
    [  # S-box thứ 4, chứa bốn hàng và mười sáu cột.
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],  # Hàng 0: tra cột 0 đến 15 trong S-box 4.
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],  # Hàng 1: tra cột 0 đến 15 trong S-box 4.
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],  # Hàng 2: tra cột 0 đến 15 trong S-box 4.
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],  # Hàng 3: tra cột 0 đến 15 trong S-box 4.
    ],  # Kết thúc S-box thứ 4.
    [  # S-box thứ 5, chứa bốn hàng và mười sáu cột.
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],  # Hàng 0: tra cột 0 đến 15 trong S-box 5.
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],  # Hàng 1: tra cột 0 đến 15 trong S-box 5.
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],  # Hàng 2: tra cột 0 đến 15 trong S-box 5.
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],  # Hàng 3: tra cột 0 đến 15 trong S-box 5.
    ],  # Kết thúc S-box thứ 5.
    [  # S-box thứ 6, chứa bốn hàng và mười sáu cột.
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],  # Hàng 0: tra cột 0 đến 15 trong S-box 6.
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],  # Hàng 1: tra cột 0 đến 15 trong S-box 6.
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],  # Hàng 2: tra cột 0 đến 15 trong S-box 6.
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],  # Hàng 3: tra cột 0 đến 15 trong S-box 6.
    ],  # Kết thúc S-box thứ 6.
    [  # S-box thứ 7, chứa bốn hàng và mười sáu cột.
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],  # Hàng 0: tra cột 0 đến 15 trong S-box 7.
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],  # Hàng 1: tra cột 0 đến 15 trong S-box 7.
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],  # Hàng 2: tra cột 0 đến 15 trong S-box 7.
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],  # Hàng 3: tra cột 0 đến 15 trong S-box 7.
    ],  # Kết thúc S-box thứ 7.
    [  # S-box thứ 8, chứa bốn hàng và mười sáu cột.
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],  # Hàng 0: tra cột 0 đến 15 trong S-box 8.
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],  # Hàng 1: tra cột 0 đến 15 trong S-box 8.
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],  # Hàng 2: tra cột 0 đến 15 trong S-box 8.
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],  # Hàng 3: tra cột 0 đến 15 trong S-box 8.
    ],  # Kết thúc S-box thứ 8.
]  # Kết thúc tám S-box chuẩn của DES.


def _hoan_vi(khoi: int, bang: list[int], so_bit: int) -> int:  # Đọc bit theo bảng đánh số từ 1 ở phía trái.
    ket_qua = 0  # Chưa có bit nào trong kết quả hoán vị.
    for vi_tri in bang:  # Lần lượt lấy từng vị trí được bảng quy định.
        bit = (khoi >> (so_bit - vi_tri)) & 1  # >> đưa bit cần lấy về cuối; & 1 giữ riêng bit đó.
        ket_qua = (ket_qua << 1) | bit  # << 1 chừa một chỗ bên phải; | ghép bit mới vào.
    return ket_qua  # Trả lại số nguyên chứa các bit đã sắp xếp.


def _tao_khoa_con(khoa: bytes) -> list[int]:  # Sinh 16 khóa con, mỗi khóa dài 48 bit.
    khoa_so = int.from_bytes(khoa, "big")  # Đổi 8 byte thành số nguyên, byte đầu nằm bên trái.
    khoa_56_bit = _hoan_vi(khoa_so, _DES_PC1, 64)  # PC-1 loại bit chẵn lẻ và hoán vị khóa.
    trai = khoa_56_bit >> 28  # Lấy nửa trái gồm 28 bit cao.
    phai = khoa_56_bit & 0x0FFFFFFF  # & mặt nạ giữ 28 bit thấp cho nửa phải.
    cac_khoa_con = []  # Lưu khóa con theo thứ tự dùng khi mã hóa.
    for so_dich in _DES_SHIFTS:  # Mỗi vòng dịch khóa một hoặc hai bit theo lịch chuẩn.
        trai = ((trai << so_dich) | (trai >> (28 - so_dich))) & 0x0FFFFFFF  # Dịch vòng trái rồi giữ đúng 28 bit.
        phai = ((phai << so_dich) | (phai >> (28 - so_dich))) & 0x0FFFFFFF  # Dịch vòng độc lập cho nửa phải.
        ghep = (trai << 28) | phai  # Nối nửa trái với nửa phải thành 56 bit.
        cac_khoa_con.append(_hoan_vi(ghep, _DES_PC2, 56))  # PC-2 chọn 48 bit làm khóa của vòng này.
    return cac_khoa_con  # Trả danh sách 16 khóa con.


def _ham_f(phai: int, khoa_con: int) -> int:  # Hàm F biến nửa phải 32 bit bằng khóa con 48 bit.
    mo_rong = _hoan_vi(phai, _DES_E, 32)  # Bảng E lặp lại một số bit để tạo 48 bit.
    tron_khoa = mo_rong ^ khoa_con  # ^ là XOR: hai bit khác nhau cho 1, giống nhau cho 0.
    thay_the = 0  # Ghép dần tám đầu ra S-box, mỗi đầu ra dài 4 bit.
    for chi_so in range(8):  # Một S-box xử lý một nhóm 6 bit.
        nhom = (tron_khoa >> (42 - 6 * chi_so)) & 0x3F  # Dịch đến nhóm cần lấy, & 0x3F giữ 6 bit.
        hang = ((nhom & 0x20) >> 4) | (nhom & 1)  # Bit đầu và bit cuối của nhóm chọn hàng 0..3.
        cot = (nhom >> 1) & 0x0F  # Bốn bit giữa chọn cột 0..15.
        thay_the = (thay_the << 4) | _DES_S[chi_so][hang][cot]  # Nối giá trị 4 bit tra được vào kết quả.
    return _hoan_vi(thay_the, _DES_P, 32)  # Bảng P hoán vị đầu ra thành kết quả F 32 bit.


def _bien_doi_khoi(khoi: bytes, cac_khoa_con: list[int]) -> bytes:  # Cấu trúc Feistel dùng chung cho mã hóa và giải mã.
    khoi_so = int.from_bytes(khoi, "big")  # Biểu diễn khối 8 byte bằng số nguyên 64 bit.
    ban_dau = _hoan_vi(khoi_so, _DES_IP, 64)  # Thực hiện hoán vị đầu IP.
    trai = ban_dau >> 32  # Lấy 32 bit cao làm nửa trái.
    phai = ban_dau & 0xFFFFFFFF  # Lấy 32 bit thấp làm nửa phải.
    for khoa_con in cac_khoa_con:  # DES chạy 16 vòng với thứ tự khóa được truyền vào.
        trai, phai = phai, trai ^ _ham_f(phai, khoa_con)  # L mới = R cũ; R mới = L cũ XOR F(R cũ, khóa).
    ghep = (phai << 32) | trai  # Sau vòng cuối, ghép R16 trước L16 theo quy định DES.
    ket_qua = _hoan_vi(ghep, _DES_IP_INV, 64)  # Thực hiện hoán vị cuối IP nghịch đảo.
    return ket_qua.to_bytes(8, "big")  # Đổi kết quả 64 bit về đúng 8 byte.


def _kiem_tra_khoa(khoa: bytes) -> None:  # Chặn khóa sai trước khi thực hiện thuật toán.
    if not isinstance(khoa, bytes) or len(khoa) != 8:  # DES nhận đúng 8 byte, không tự đoán chuỗi hay hex.
        raise ValueError("Khóa DES phải là bytes có đúng 8 byte.")  # Báo lỗi rõ để người học sửa dữ liệu đầu vào.


def ma_hoa_khoi(khoi: bytes, khoa: bytes) -> bytes:  # Mã hóa đúng một khối 8 byte, không thêm đệm.
    _kiem_tra_khoa(khoa)  # Kiểm tra khóa trước khi sinh khóa con.
    if not isinstance(khoi, bytes) or len(khoi) != 8:  # Một khối DES luôn dài đúng 64 bit.
        raise ValueError("Khối DES phải là bytes có đúng 8 byte.")  # Không âm thầm cắt hoặc thêm byte cho khối.
    return _bien_doi_khoi(khoi, _tao_khoa_con(khoa))  # Dùng khóa con từ vòng 1 đến vòng 16.


def giai_ma_khoi(khoi: bytes, khoa: bytes) -> bytes:  # Giải mã một khối DES, không xử lý đệm.
    _kiem_tra_khoa(khoa)  # Khóa giải mã phải cùng định dạng với khóa mã hóa.
    if not isinstance(khoi, bytes) or len(khoi) != 8:  # Không cho khối thiếu hoặc thừa byte đi vào lõi DES.
        raise ValueError("Khối DES phải là bytes có đúng 8 byte.")  # Báo lỗi nếu kích thước khối sai.
    cac_khoa_con = _tao_khoa_con(khoa)  # Sinh lại 16 khóa con từ khóa gốc.
    cac_khoa_con.reverse()  # Feistel giải mã bằng chính cấu trúc mã hóa nhưng đảo thứ tự khóa con.
    return _bien_doi_khoi(khoi, cac_khoa_con)  # Thu được đúng 8 byte bản rõ của khối.


def ma_hoa(van_ban: str, khoa: bytes) -> str:  # Mã hóa văn bản UTF-8 nhiều khối và trả chuỗi hex.
    _kiem_tra_khoa(khoa)  # Kiểm tra khóa trước khi xử lý văn bản.
    du_lieu = van_ban.encode("utf-8")  # UTF-8 giữ được tiếng Việt, khoảng trắng và xuống dòng.
    so_dem = 8 - len(du_lieu) % 8  # PKCS#7 luôn thêm từ 1 đến 8 byte, kể cả khi đủ khối.
    du_lieu += bytes([so_dem] * so_dem)  # Mỗi byte đệm đều chứa số lượng byte đệm.
    cac_khoa_con = _tao_khoa_con(khoa)  # Chỉ sinh khóa con một lần cho toàn bộ văn bản.
    ket_qua = bytearray()  # Bộ đệm để nối các khối mã hóa.
    for vi_tri in range(0, len(du_lieu), 8):  # Đọc lần lượt các khối 8 byte độc lập theo ECB.
        khoi = du_lieu[vi_tri:vi_tri + 8]  # Tách đúng một khối từ dữ liệu đã đệm.
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_con))  # Mã hóa khối rồi nối vào bản mã.
    return ket_qua.hex().upper()  # Hai chữ số hex biểu diễn một byte, tiện xem và sao chép.


def giai_ma(ban_ma_hex: str, khoa: bytes) -> str:  # Giải mã hex, kiểm tra PKCS#7 rồi đọc lại UTF-8.
    _kiem_tra_khoa(khoa)  # Khóa sai độ dài bị từ chối ngay.
    du_lieu = bytes.fromhex(ban_ma_hex)  # Hex sai định dạng tự phát sinh ValueError.
    if not du_lieu or len(du_lieu) % 8 != 0:  # Bản mã có đệm phải có ít nhất một khối đầy đủ.
        raise ValueError("Bản mã DES phải có độ dài dương và chia hết cho 8 byte.")  # Không giải mã bản mã bị thiếu khối.
    cac_khoa_con = _tao_khoa_con(khoa)  # Sinh các khóa con như khi mã hóa.
    cac_khoa_con.reverse()  # Đảo thứ tự khóa để cùng hàm Feistel thực hiện giải mã.
    ket_qua = bytearray()  # Gom bản rõ của các khối, vẫn còn đệm ở cuối.
    for vi_tri in range(0, len(du_lieu), 8):  # Giải mã từng khối 8 byte của bản mã ECB.
        khoi = du_lieu[vi_tri:vi_tri + 8]  # Lấy khối bản mã hiện tại.
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_con))  # Ghép bản rõ khối vào bộ đệm.
    so_dem = ket_qua[-1]  # Byte cuối ghi số lượng byte PKCS#7 phải bỏ.
    if not 1 <= so_dem <= 8:  # Số byte đệm hợp lệ phải nằm trong kích thước khối DES.
        raise ValueError("Đệm PKCS#7 DES không hợp lệ; có thể sai khóa hoặc bản mã.")  # Báo lỗi thay vì trả dữ liệu rác.
    if ket_qua[-so_dem:] != bytes([so_dem] * so_dem):  # Toàn bộ phần đệm phải lặp đúng cùng giá trị.
        raise ValueError("Đệm PKCS#7 DES không hợp lệ; có thể sai khóa hoặc bản mã.")  # Không bỏ đệm khi chỉ byte cuối có vẻ hợp lệ.
    return ket_qua[:-so_dem].decode("utf-8")  # Bỏ đúng phần đệm rồi đọc tiếng Việt; UTF-8 sai cũng báo lỗi.


if __name__ == "__main__":  # Chỉ chạy ví dụ khi thực thi trực tiếp file này.
    van_ban = "Xin chào DES!"  # Sửa văn bản này để thử dữ liệu khác, kể cả chuỗi rỗng.
    khoa = b"12345678"  # Khóa ví dụ có đúng 8 byte ASCII; tiền tố b tạo dữ liệu bytes.
    ban_ma = ma_hoa(van_ban, khoa)  # Mã hóa văn bản với đệm PKCS#7.
    ban_ro = giai_ma(ban_ma, khoa)  # Dùng cùng khóa để khôi phục văn bản ban đầu.
    print("Bản rõ:", van_ban)  # Hiển thị dữ liệu trước mã hóa.
    print("Bản mã hex:", ban_ma)  # Hiển thị kết quả để dễ quan sát.
    print("Giải mã:", ban_ro)  # Hiển thị văn bản sau giải mã.
    assert ban_ro == van_ban  # Tự kiểm tra mã hóa và giải mã khớp nhau.
    khoa_mau = bytes.fromhex("133457799BBCDFF1")  # Khóa của vector kiểm tra DES chuẩn, viết bằng hex.
    khoi_mau = bytes.fromhex("0123456789ABCDEF")  # Khối rõ 8 byte, không phải văn bản UTF-8.
    ma_mau = bytes.fromhex("85E813540F0AB405")  # Kết quả DES đã biết để đối chiếu độc lập với giải mã.
    assert ma_hoa_khoi(khoi_mau, khoa_mau) == ma_mau  # Đảm bảo lõi mã hóa đúng vector chuẩn.
    assert giai_ma_khoi(ma_mau, khoa_mau) == khoi_mau  # Đảm bảo lõi giải mã cũng đúng vector chuẩn.
