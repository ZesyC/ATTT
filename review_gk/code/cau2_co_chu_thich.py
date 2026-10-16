from pathlib import Path  # Xác định vị trí X.txt cạnh file chương trình; không dùng để tính thuật toán.


BANG_K = [  # 64 hằng số chuẩn MD5 theo RFC 1321.
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,  # Bốn hằng số liên tiếp, lần lượt dùng trong bốn bước MD5.
]  # Kết thúc bảng BANG_K.
SO_BUOC_XOAY = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4  # Số bit xoay trái tại từng bước trong 64 bước MD5.


def so_sang_mang(so: int, do_dai: int) -> list[int]:  # Đổi số thành mảng bit có độ dài cố định, bit cao nhất đứng đầu.
    mang = [0] * do_dai  # Khởi tạo mảng gồm các phần tử 0.
    for i in range(do_dai - 1, -1, -1):  # Đi từ cuối mảng về đầu để lấy từng chữ số nhị phân.
        mang[i] = so % 2  # Chia dư 2 cho chữ số cuối: chỉ có thể là 0 hoặc 1.
        so //= 2  # Chia nguyên cho 2 để bỏ chữ số vừa lấy.
    return mang  # Trả mảng số 0/1; các phép xử lý phía sau làm việc trên mảng này.


def mang_sang_so(mang: list[int]) -> int:  # Chỉ đổi mảng thành số khi cần xuất kết quả dạng hex.
    so = 0  # Bắt đầu tích lũy giá trị từ 0.
    for bit in mang:  # Đọc mảng từ trái sang phải, từ chữ số lớn đến nhỏ.
        so = so * 2 + bit  # Nhân 2 rồi cộng chữ số tiếp theo, tương tự đọc một số nhị phân.
    return so  # Trả số nguyên tương ứng với mảng.


def xor(*cac_mang: list[int]) -> list[int]:  # XOR từng cột: số lượng phần tử 1 lẻ thì kết quả là 1.
    return [sum(cot) % 2 for cot in zip(*cac_mang)]  # zip ghép các phần tử cùng vị trí; tổng chia dư 2 chính là XOR.


def va(a: list[int], b: list[int]) -> list[int]:  # AND từng cặp phần tử: chỉ 1 AND 1 mới bằng 1.
    return [x * y for x, y in zip(a, b)]  # Nhân hai phần tử 0/1 thực hiện đúng bảng chân trị AND.


def hoac(a: list[int], b: list[int]) -> list[int]:  # OR từng cặp phần tử: có ít nhất một số 1 thì trả 1.
    return [max(x, y) for x, y in zip(a, b)]  # Giá trị lớn nhất trong hai số 0/1 thực hiện đúng OR.


def dao(mang: list[int]) -> list[int]:  # NOT bằng cách đổi mọi phần tử 0 thành 1 và 1 thành 0.
    return [1 - bit for bit in mang]  # Mỗi phần tử mới bằng 1 trừ phần tử cũ.


def cong(*cac_mang: list[int]) -> list[int]:  # Cộng nhị phân có nhớ, giữ nguyên độ dài từ 32 hoặc 64 phần tử.
    ket_qua = [0] * len(cac_mang[0])  # Kết quả có cùng số phần tử với mỗi từ đầu vào.
    nho = 0  # Chưa có số nhớ khi bắt đầu cộng từ cột ngoài cùng bên phải.
    for i in range(len(ket_qua) - 1, -1, -1):  # Cộng từ phải sang trái giống phép cộng bằng tay.
        tong = nho + sum(mang[i] for mang in cac_mang)  # Tổng cột hiện tại gồm tất cả phần tử cùng vị trí và số nhớ.
        ket_qua[i] = tong % 2  # Chữ số nhị phân của cột là phần dư khi chia tổng cho 2.
        nho = tong // 2  # Chuyển phần nguyên sang cột tiếp theo.
    return ket_qua  # Bỏ số nhớ vượt đầu mảng: tương đương cộng modulo 2 mũ độ dài từ.


def xoay_trai(mang: list[int], so_buoc: int) -> list[int]:  # Xoay vòng trái bằng cắt và ghép mảng; không dùng toán tử dịch bit.
    so_buoc %= len(mang)  # Xoay đủ một vòng sẽ trở lại mảng ban đầu.
    return mang[so_buoc:] + mang[:so_buoc]  # Đưa các phần tử đầu mảng xuống cuối mảng.


def doi_thu_tu_byte(mang: list[int]) -> list[int]:  # MD5 dùng little-endian: đảo các nhóm 8 phần tử, không đảo bên trong nhóm.
    return [bit for i in range(len(mang) - 8, -1, -8) for bit in mang[i:i + 8]]  # Đọc các nhóm byte từ cuối về đầu rồi ghép thành mảng mới.


def bam_md5(du_lieu: bytes) -> str:  # Tính MD5 bằng mảng 0/1 như bài cũ; nhận trực tiếp dữ liệu nhị phân của tệp.
    if not isinstance(du_lieu, bytes):  # Kiểm tra đầu vào là bytes để băm đúng nội dung gốc của mọi loại tệp.
        raise ValueError("Dữ liệu cần băm phải là bytes.")  # Báo lỗi nếu đầu vào không phải dữ liệu nhị phân.
    cac_bit = [bit for byte in du_lieu for bit in so_sang_mang(byte, 8)]  # Tách mỗi byte của tệp thành 8 bit rồi ghép thành một mảng 0/1.
    do_dai_ban_dau = len(cac_bit)  # Lưu độ dài tính bằng bit trước khi thêm phần đệm.
    cac_bit.append(1)  # Bắt đầu phần đệm bằng đúng một phần tử 1.
    cac_bit.extend([0] * ((448 - len(cac_bit)) % 512))  # Thêm 0 để còn 64 vị trí cuối khối 512 dành cho độ dài ban đầu.
    cac_bit.extend(doi_thu_tu_byte(so_sang_mang(do_dai_ban_dau, 64)))  # Ghi độ dài 64 bit theo little-endian như chuẩn MD5.
    trang_thai = [so_sang_mang(so, 32) for so in [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]]  # Chuyển các giá trị khởi tạo chuẩn thành từng hàng 32 phần tử 0/1.
    bang_k = [so_sang_mang(so, 32) for so in BANG_K]  # Đổi bảng hằng số thành ma trận các từ 32 phần tử.

    for dau_khoi in range(0, len(cac_bit), 512):  # Xử lý lần lượt các khối, mỗi khối là một mảng 512 phần tử.
        khoi = cac_bit[dau_khoi:dau_khoi + 512]  # Lấy riêng khối hiện tại để xây ma trận các từ.
        ma_tran = [doi_thu_tu_byte(khoi[i:i + 32]) for i in range(0, 512, 32)]  # Ma trận MD5 có 16 hàng, mỗi hàng 32 phần tử; đọc từng từ theo little-endian.
        a, b, c, d = trang_thai  # Bốn biến là bốn mảng 32 phần tử, không phải số nguyên để xử lý bit.
        for i in range(64):  # Thực hiện 64 bước nén, chia thành bốn nhóm 16 bước.
            if i < 16:  # Nhóm thứ nhất của MD5 dùng hàm F và đọc các từ theo thứ tự.
                f = hoac(va(b, c), va(dao(b), d))  # F chọn phần tử của c khi b là 1; còn lại chọn d.
                vi_tri = i  # Chỉ số từ trong ma trận 16 hàng của khối hiện tại.
            elif i < 32:  # Nhóm thứ hai của MD5 dùng hàm G.
                f = hoac(va(b, d), va(c, dao(d)))  # G chọn phần tử của b khi d là 1; còn lại chọn c.
                vi_tri = (5 * i + 1) % 16  # Lịch chọn từ của nhóm G theo chuẩn MD5.
            elif i < 48:  # Nhóm thứ ba của MD5 dùng hàm H.
                f = xor(b, c, d)  # H là XOR của ba mảng b, c và d.
                vi_tri = (3 * i + 5) % 16  # Lịch chọn từ của nhóm H.
            else:  # Các bước 48 đến 63 sử dụng hàm I của MD5.
                f = xor(c, hoac(b, dao(d)))  # Nhóm cuối dùng hàm I, kết hợp XOR, OR và NOT trên mảng.
                vi_tri = (7 * i) % 16  # Lịch chọn từ của nhóm I.
            tong = cong(a, f, bang_k[i], ma_tran[vi_tri])  # Cộng mảng a, kết quả hàm phụ, hằng số bước và một hàng dữ liệu.
            b_moi = cong(b, xoay_trai(tong, SO_BUOC_XOAY[i]))  # Xoay mảng tổng rồi cộng vào b để tạo b mới.
            a, b, c, d = d, b_moi, b, c  # Cập nhật đồng thời để mọi vế phải vẫn dùng giá trị của bước cũ.
        trang_thai = [cong(cu, moi) for cu, moi in zip(trang_thai, [a, b, c, d])]  # Cộng trạng thái trước khối với kết quả sau 64 bước để nối chuỗi các khối.

    return "".join(f"{mang_sang_so(doi_thu_tu_byte(tu)):08x}" for tu in trang_thai)  # Xuất bốn từ little-endian thành 32 ký tự hex viết thường.


_DES_IP = [  # Bảng hoán vị đầu vào 64 bit của DES.
    58, 50, 42, 34, 26, 18, 10, 2,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
    60, 52, 44, 36, 28, 20, 12, 4,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
    62, 54, 46, 38, 30, 22, 14, 6,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
    64, 56, 48, 40, 32, 24, 16, 8,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
    57, 49, 41, 33, 25, 17, 9, 1,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
    59, 51, 43, 35, 27, 19, 11, 3,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
    61, 53, 45, 37, 29, 21, 13, 5,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
    63, 55, 47, 39, 31, 23, 15, 7,  # Các vị trí bit cố định của bảng _DES_IP, đếm từ 1 bên trái.
]  # Kết thúc bảng _DES_IP.

_DES_IP_INV = [  # Bảng hoán vị cuối, đảo lại hoán vị IP.
    40, 8, 48, 16, 56, 24, 64, 32,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
    39, 7, 47, 15, 55, 23, 63, 31,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
    38, 6, 46, 14, 54, 22, 62, 30,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
    37, 5, 45, 13, 53, 21, 61, 29,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
    36, 4, 44, 12, 52, 20, 60, 28,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
    35, 3, 43, 11, 51, 19, 59, 27,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
    34, 2, 42, 10, 50, 18, 58, 26,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
    33, 1, 41, 9, 49, 17, 57, 25,  # Các vị trí bit cố định của bảng _DES_IP_INV, đếm từ 1 bên trái.
]  # Kết thúc bảng _DES_IP_INV.

_DES_PC1 = [  # Bảng chọn 56 bit từ khóa 64 bit và bỏ các bit chẵn lẻ.
    57, 49, 41, 33, 25, 17, 9,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
    1, 58, 50, 42, 34, 26, 18,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
    10, 2, 59, 51, 43, 35, 27,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
    19, 11, 3, 60, 52, 44, 36,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
    63, 55, 47, 39, 31, 23, 15,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
    7, 62, 54, 46, 38, 30, 22,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
    14, 6, 61, 53, 45, 37, 29,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
    21, 13, 5, 28, 20, 12, 4,  # Các vị trí bit cố định của bảng _DES_PC1, đếm từ 1 bên trái.
]  # Kết thúc bảng _DES_PC1.

_DES_PC2 = [  # Bảng chọn 48 bit từ 56 bit để tạo khóa con.
    14, 17, 11, 24, 1, 5,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
    3, 28, 15, 6, 21, 10,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
    23, 19, 12, 4, 26, 8,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
    16, 7, 27, 20, 13, 2,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
    41, 52, 31, 37, 47, 55,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
    30, 40, 51, 45, 33, 48,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
    44, 49, 39, 56, 34, 53,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
    46, 42, 50, 36, 29, 32,  # Các vị trí bit cố định của bảng _DES_PC2, đếm từ 1 bên trái.
]  # Kết thúc bảng _DES_PC2.

_DES_SHIFTS = [  # Số bit xoay hai nửa khóa tại mỗi vòng trong 16 vòng DES.
    1, 1, 2, 2, 2, 2, 2, 2,  # Các vị trí bit cố định của bảng _DES_SHIFTS, đếm từ 1 bên trái.
    1, 2, 2, 2, 2, 2, 2, 1,  # Các vị trí bit cố định của bảng _DES_SHIFTS, đếm từ 1 bên trái.
]  # Kết thúc bảng _DES_SHIFTS.

_DES_E = [  # Bảng mở rộng 32 bit thành 48 bit bằng cách chọn lặp một số bit.
    32, 1, 2, 3, 4, 5,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
    4, 5, 6, 7, 8, 9,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
    8, 9, 10, 11, 12, 13,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
    12, 13, 14, 15, 16, 17,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
    16, 17, 18, 19, 20, 21,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
    20, 21, 22, 23, 24, 25,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
    24, 25, 26, 27, 28, 29,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
    28, 29, 30, 31, 32, 1,  # Các vị trí bit cố định của bảng _DES_E, đếm từ 1 bên trái.
]  # Kết thúc bảng _DES_E.

_DES_P = [  # Bảng hoán vị 32 bit sau khi qua S-box.
    16, 7, 20, 21, 29, 12, 28, 17,  # Các vị trí bit cố định của bảng _DES_P, đếm từ 1 bên trái.
    1, 15, 23, 26, 5, 18, 31, 10,  # Các vị trí bit cố định của bảng _DES_P, đếm từ 1 bên trái.
    2, 8, 24, 14, 32, 27, 3, 9,  # Các vị trí bit cố định của bảng _DES_P, đếm từ 1 bên trái.
    19, 13, 30, 6, 22, 11, 4, 25,  # Các vị trí bit cố định của bảng _DES_P, đếm từ 1 bên trái.
]  # Kết thúc bảng _DES_P.

_DES_S = [  # Tám S-box DES, mỗi S-box gồm 4 hàng và 16 cột.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
    [  # Bắt đầu một S-box với 4 hàng, mỗi hàng 16 giá trị.
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],  # Một hàng gồm 16 giá trị 4 bit của S-box hiện tại.
    ],  # Kết thúc S-box hiện tại.
]  # Kết thúc bảng _DES_S.


def _so_thanh_bit(so: int, do_dai: int) -> list[int]:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.

    cac_bit = [0] * do_dai  # Tạo đủ các ô để giữ cả các chữ số 0 ở đầu.
    for vi_tri in range(do_dai - 1, -1, -1):  # Đi từ cuối mảng về đầu để điền chữ số nhị phân.
        cac_bit[vi_tri] = so % 2  # Phần dư chia 2 là chữ số cuối.
        so = so // 2  # Bỏ chữ số vừa lấy bằng phép chia nguyên.
    return cac_bit  # Trả kết quả đã tạo.


def _bit_thanh_so(cac_bit: list[int]) -> int:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.
    ket_qua = 0  # Bắt đầu đọc số từ giá trị 0.
    for bit in cac_bit:  # Duyệt lần lượt các phần tử cần xử lý.
        ket_qua = ket_qua * 2 + bit  # Đọc thêm một chữ số nhị phân ở bên phải.
    return ket_qua  # Trả kết quả đã tạo.


def _byte_thanh_bit(du_lieu: bytes) -> list[int]:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.
    cac_bit = []  # Khởi tạo danh sách kết quả rỗng.
    for byte in du_lieu:  # Duyệt lần lượt các phần tử cần xử lý.
        cac_bit.extend(_so_thanh_bit(byte, 8))  # Mỗi byte trở thành 8 ô 0/1 rồi nối vào mảng.
    return cac_bit  # Trả kết quả đã tạo.


def _bit_thanh_byte(cac_bit: list[int]) -> bytes:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.
    cac_byte = []  # Khởi tạo danh sách kết quả rỗng.
    for vi_tri in range(0, len(cac_bit), 8):  # Duyệt lần lượt các phần tử cần xử lý.
        cac_byte.append(_bit_thanh_so(cac_bit[vi_tri:vi_tri + 8]))  # Đọc từng nhóm 8 ô thành một byte.
    return bytes(cac_byte)  # Trả kết quả đã tạo.


def _xor(trai: list[int], phai: list[int]) -> list[int]:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.

    ket_qua = []  # Khởi tạo danh sách kết quả rỗng.
    for vi_tri in range(len(trai)):  # Duyệt lần lượt các phần tử cần xử lý.
        ket_qua.append((trai[vi_tri] + phai[vi_tri]) % 2)  # Hai ô giống nhau cho 0, khác nhau cho 1.
    return ket_qua  # Trả kết quả đã tạo.


def _hoan_vi(khoi: list[int], bang: list[int]) -> list[int]:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.
    ket_qua = []  # Khởi tạo danh sách kết quả rỗng.
    for vi_tri in bang:  # Duyệt lần lượt các phần tử cần xử lý.
        ket_qua.append(khoi[vi_tri - 1])  # Bảng DES đếm từ 1; chỉ số danh sách đếm từ 0.
    return ket_qua  # Trả kết quả đã tạo.


def _tao_khoa_con(khoa: bytes) -> list[list[int]]:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.
    khoa_64_bit = _byte_thanh_bit(khoa)  # Khóa 8 byte trở thành mảng 64 phần tử.
    khoa_56_bit = _hoan_vi(khoa_64_bit, _DES_PC1)  # PC-1 chọn 56 ô, bỏ các bit chẵn lẻ.
    trai = khoa_56_bit[:28]  # C0 lấy 28 phần tử đầu.
    phai = khoa_56_bit[28:]  # D0 lấy 28 phần tử còn lại.
    cac_khoa_con = []  # Khởi tạo danh sách kết quả rỗng.
    for so_dich in _DES_SHIFTS:  # Duyệt lần lượt các phần tử cần xử lý.
        trai = trai[so_dich:] + trai[:so_dich]  # Đưa các phần tử đầu sang cuối để dịch vòng C.
        phai = phai[so_dich:] + phai[:so_dich]  # Dịch vòng D tương tự C.
        ghep = trai + phai  # Nối hai nửa thành 56 ô.
        cac_khoa_con.append(_hoan_vi(ghep, _DES_PC2))  # PC-2 chọn 48 ô cho khóa con vòng này.
    return cac_khoa_con  # Trả kết quả đã tạo.


def _ham_f(phai: list[int], khoa_con: list[int]) -> list[int]:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.
    mo_rong = _hoan_vi(phai, _DES_E)  # E chọn lặp một số ô, mở rộng 32 thành 48.
    tron_khoa = _xor(mo_rong, khoa_con)  # XOR từng cặp ô với khóa con.
    thay_the = []  # Khởi tạo danh sách kết quả rỗng.
    for chi_so in range(8):  # Duyệt lần lượt các phần tử cần xử lý.
        nhom = tron_khoa[6 * chi_so:6 * chi_so + 6]  # Cắt đúng 6 ô dành cho S-box đang xét.
        hang = _bit_thanh_so([nhom[0], nhom[5]])  # Hai ô ngoài chọn hàng 0 đến 3.
        cot = _bit_thanh_so(nhom[1:5])  # Bốn ô giữa chọn cột 0 đến 15.
        gia_tri = _DES_S[chi_so][hang][cot]  # Tra phần tử trong ma trận S-box.
        thay_the.extend(_so_thanh_bit(gia_tri, 4))  # Nối 4 bit của kết quả vào mảng sau thay thế.
    return _hoan_vi(thay_the, _DES_P)  # Hoán vị mảng 32 phần tử sau S-box.


def _bien_doi_khoi(khoi: bytes, cac_khoa_con: list[list[int]]) -> bytes:  # Hàm tự viết, xử lý bằng danh sách và phép toán số học.
    cac_bit = _byte_thanh_bit(khoi)  # Biểu diễn khối 8 byte bằng mảng 64 ô.
    ban_dau = _hoan_vi(cac_bit, _DES_IP)  # Đổi thứ tự các ô theo IP.
    trai = ban_dau[:32]  # L0 lấy 32 ô đầu.
    phai = ban_dau[32:]  # R0 lấy 32 ô sau.
    for khoa_con in cac_khoa_con:  # Duyệt lần lượt các phần tử cần xử lý.
        trai_moi = phai  # Trái mới lấy nguyên mảng phải cũ.
        phai_moi = _xor(trai, _ham_f(phai, khoa_con))  # Phải mới lấy trái cũ XOR với F của phải cũ.
        trai, phai = trai_moi, phai_moi  # Cập nhật sau khi đã tính xong hai mảng mới.
    ghep = phai + trai  # Sau vòng 16, R16 đứng trước L16.
    ket_qua = _hoan_vi(ghep, _DES_IP_INV)  # Hoán vị cuối bằng IP nghịch đảo.
    return _bit_thanh_byte(ket_qua)  # Đóng gói mảng 64 bit về 8 byte.


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


def ma_hoa(du_lieu: bytes, khoa: bytes) -> bytes:  # DES-ECB từ bài cũ; nhận bytes, thêm đệm PKCS#7 và trả bản mã bytes.
    _kiem_tra_khoa(khoa)  # Kiểm tra khóa trước khi xử lý văn bản.
    so_dem = 8 - len(du_lieu) % 8  # PKCS#7 luôn thêm từ 1 đến 8 byte, kể cả khi đủ khối.
    du_lieu += bytes([so_dem] * so_dem)  # Mỗi byte đệm đều chứa số lượng byte đệm.
    cac_khoa_con = _tao_khoa_con(khoa)  # Chỉ sinh khóa con một lần cho toàn bộ văn bản.
    ket_qua = bytearray()  # Bộ đệm để nối các khối mã hóa.
    for vi_tri in range(0, len(du_lieu), 8):  # Đọc lần lượt các khối 8 byte độc lập theo ECB.
        khoi = du_lieu[vi_tri:vi_tri + 8]  # Tách đúng một khối từ dữ liệu đã đệm.
        ket_qua.extend(_bien_doi_khoi(khoi, cac_khoa_con))  # Mã hóa khối rồi nối vào bản mã.
    return bytes(ket_qua)  # Trả bản mã nhị phân để ghi trực tiếp xuống tệp .des.


def giai_ma(du_lieu: bytes, khoa: bytes) -> bytes:  # Giải mã bản mã nhị phân bằng DES-ECB và kiểm tra phần đệm PKCS#7.
    _kiem_tra_khoa(khoa)  # Khóa sai độ dài bị từ chối ngay.
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
        raise ValueError("Đệm PKCS#7 DES không hợp lệ; có thể sai khóa hoặc bản mã.")  # Không bỏ đệm khi chỉ byte cuối có vẻ hợp lệ.
    if ket_qua[-so_dem:] != bytes([so_dem] * so_dem):  # Toàn bộ phần đệm phải lặp đúng cùng giá trị.
        raise ValueError("Đệm PKCS#7 DES không hợp lệ; có thể sai khóa hoặc bản mã.")  # Không bỏ đệm khi chỉ byte cuối có vẻ hợp lệ.
    return bytes(ket_qua[:-so_dem])  # Bỏ phần đệm và trả bytes gốc, không ép dữ liệu tệp thành văn bản.


def ma_hoa_tep(ten_tep, khoa):  # Tính MD5, ghép vào cuối dữ liệu rồi mã hóa và lưu tệp.
    with open(ten_tep, "rb") as tep:  # Mở tệp gốc ở chế độ đọc nhị phân để dùng được cho mọi loại tệp.
        du_lieu = tep.read()  # Đọc toàn bộ nội dung tệp gốc.
    y = bam_md5(du_lieu)  # Tính MD5 của riêng nội dung gốc, trước khi ghép mã băm.
    du_lieu += y.encode("ascii")  # Thêm 32 byte ký tự hex của Y vào cuối dữ liệu X.
    ban_ma = ma_hoa(du_lieu, khoa)  # Mã hóa toàn bộ X ghép Y bằng DES.
    ten_ma = ten_tep + ".des"  # Đặt tên tệp mã hóa, ví dụ X.txt.des.
    with open(ten_ma, "xb") as tep:  # Tạo tệp mới; báo lỗi nếu tên này đã tồn tại để tránh ghi đè.
        tep.write(ban_ma)  # Lưu bản mã xuống hệ thống tệp.
    return ten_ma, y  # Trả về tên tệp vừa lưu và MD5 ban đầu.


def kiem_tra_tep(ten_tep, khoa):  # Kiểm tra tệp mã hóa đã lưu bằng cách giải mã và đối chiếu MD5.
    with open(ten_tep, "rb") as tep:  # Mở tệp .des ở chế độ nhị phân.
        ban_ma = tep.read()  # Đọc bản mã đang được lưu trên hệ thống.
    try:  # Bắt lỗi giải mã để kết luận không xác nhận được tính toàn vẹn.
        du_lieu = giai_ma(ban_ma, khoa)  # Giải mã DES và bỏ đệm để lấy X ghép Y.
    except ValueError:  # Xử lý khi sai khóa, sai độ dài hoặc phần đệm bị hỏng.
        return False  # Không xác nhận tính toàn vẹn khi giải mã thất bại.
    if len(du_lieu) < 32:  # Dữ liệu phải có ít nhất 32 byte để chứa MD5 đã lưu.
        return False  # Từ chối dữ liệu thiếu mã băm.
    x = du_lieu[:-32]  # Tách nội dung gốc bằng cách bỏ 32 byte cuối.
    y_cu = du_lieu[-32:]  # Lấy 32 byte MD5 đã lưu ở cuối dữ liệu.
    y_moi = bam_md5(x).encode("ascii")  # Tính lại MD5 của nội dung vừa giải mã.
    return y_moi == y_cu  # Hai mã băm bằng nhau nghĩa là kiểm tra MD5 đạt.


if __name__ == "__main__":  # Chỉ chạy giao diện nhập liệu khi thực thi trực tiếp file này.
    print("1. Tính MD5, ghép vào cuối dữ liệu và mã hóa DES")  # Hiển thị lựa chọn tạo tệp mã hóa.
    print("2. Kiểm tra tính toàn vẹn của tệp .des đã lưu")  # Hiển thị lựa chọn kiểm tra ở lần chạy sau.
    try:  # Bắt lỗi nhập liệu và lỗi đọc ghi tệp để thông báo dễ hiểu.
        chon = input("Chọn 1 hoặc 2: ").strip()  # Đọc lựa chọn của người dùng.
        if chon not in ("1", "2"):  # Kiểm tra lựa chọn có hợp lệ không.
            raise ValueError("Chỉ được chọn 1 hoặc 2.")  # Báo lỗi nếu nhập lựa chọn khác.
        ten_tep = str(Path(__file__).with_name("X.txt"))  # Cố định tệp X.txt nằm cùng thư mục với chương trình.
        khoa = input("Nhập khóa DES gồm đúng 8 ký tự ASCII: ").encode("ascii")  # Đổi khóa sang bytes; không chấp nhận chữ có dấu.
        if len(khoa) != 8:  # Kiểm tra khóa trước khi đọc hay ghi dữ liệu.
            raise ValueError("Khóa phải gồm đúng 8 ký tự ASCII.")  # Thông báo kích thước khóa yêu cầu.
        if chon == "1":  # Thực hiện nhánh mã hóa tệp.
            ten_ma, y = ma_hoa_tep(ten_tep, khoa)  # Tính MD5, ghép vào dữ liệu, mã hóa và lưu.
            print("MD5 ban đầu:", y)  # Hiển thị Y để người học quan sát.
            print("Đã lưu tệp mã hóa:", ten_ma)  # Hiển thị đường dẫn tệp kết quả.
        else:  # Thực hiện lựa chọn 2: kiểm tra tệp mã hóa đã lưu.
            if kiem_tra_tep(ten_tep + ".des", khoa):  # Kiểm tra tệp X.txt.des bằng cách giải mã và so sánh MD5.
                print("MD5 khớp: chưa phát hiện thay đổi nội dung tệp.")  # Thông báo kiểm tra MD5 đạt.
            else:  # Xử lý khi giải mã lỗi hoặc hai mã băm khác nhau.
                print("Kiểm tra không đạt: tệp đã bị thay đổi, bị hỏng hoặc khóa không đúng.")  # Thông báo không xác nhận được tính toàn vẹn.
    except (OSError, ValueError) as loi:  # Bắt lỗi tệp, lựa chọn hoặc khóa không hợp lệ.
        print("Lỗi:", loi)  # In nguyên nhân để người dùng sửa dữ liệu nhập.
