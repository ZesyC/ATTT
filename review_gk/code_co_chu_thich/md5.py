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


def so_sang_mang(so: int, do_dai: int) -> list[int]:  # Biểu diễn số thành mảng cố định độ dài, phần tử lớn nhất ở đầu.
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


def bam_md5(van_ban: str) -> str:  # Tự thực hiện đủ đệm dữ liệu, vòng nén và xuất MD5, không gọi thư viện băm.
    if not isinstance(van_ban, str):  # Chỉ nhận chuỗi văn bản để việc mã hóa UTF-8 được rõ ràng.
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")  # Giữ cách báo lỗi đầu vào giống phiên bản cũ.
    du_lieu = [bit for byte in van_ban.encode("utf-8") for bit in so_sang_mang(byte, 8)]  # UTF-8 đổi chữ thành byte; tự tách mỗi byte thành 8 phần tử 0/1.
    do_dai_ban_dau = len(du_lieu)  # Lưu độ dài tính bằng bit trước khi thêm phần đệm.
    du_lieu.append(1)  # Bắt đầu phần đệm bằng đúng một phần tử 1.
    du_lieu.extend([0] * ((448 - len(du_lieu)) % 512))  # Thêm 0 để còn 64 vị trí cuối khối 512 dành cho độ dài ban đầu.
    du_lieu.extend(doi_thu_tu_byte(so_sang_mang(do_dai_ban_dau, 64)))  # Ghi độ dài 64 bit theo little-endian như chuẩn MD5.
    trang_thai = [so_sang_mang(so, 32) for so in [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]]  # Chuyển các giá trị khởi tạo chuẩn thành từng hàng 32 phần tử 0/1.
    bang_k = [so_sang_mang(so, 32) for so in BANG_K]  # Đổi bảng hằng số thành ma trận các từ 32 phần tử.

    for dau_khoi in range(0, len(du_lieu), 512):  # Xử lý lần lượt các khối, mỗi khối là một mảng 512 phần tử.
        khoi = du_lieu[dau_khoi:dau_khoi + 512]  # Lấy riêng khối hiện tại để xây ma trận các từ.
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
                f = xor(b, c, d)  # H hoặc hàm parity của SHA-1 lấy XOR của ba mảng.
                vi_tri = (3 * i + 5) % 16  # Lịch chọn từ của nhóm H.
            else:
                f = xor(c, hoac(b, dao(d)))  # Nhóm cuối dùng hàm I, kết hợp XOR, OR và NOT trên mảng.
                vi_tri = (7 * i) % 16  # Lịch chọn từ của nhóm I.
            tong = cong(a, f, bang_k[i], ma_tran[vi_tri])  # Cộng mảng a, kết quả hàm phụ, hằng số bước và một hàng dữ liệu.
            b_moi = cong(b, xoay_trai(tong, SO_BUOC_XOAY[i]))  # Xoay mảng tổng rồi cộng vào b để tạo b mới.
            a, b, c, d = d, b_moi, b, c  # Cập nhật đồng thời để mọi vế phải vẫn dùng giá trị của bước cũ.
        trang_thai = [cong(cu, moi) for cu, moi in zip(trang_thai, [a, b, c, d])]  # Cộng trạng thái trước khối với kết quả sau 64 bước để nối chuỗi các khối.

    return "".join(f"{mang_sang_so(doi_thu_tu_byte(tu)):08x}" for tu in trang_thai)  # Xuất bốn từ little-endian thành 32 ký tự hex viết thường.


if __name__ == "__main__":  # Chỉ chạy minh họa khi thực thi trực tiếp file này.
    van_ban = "Xin chào Python!"  # Đổi chuỗi này để thử băm dữ liệu tiếng Việt khác.
    assert bam_md5("abc") == "900150983cd24fb0d6963f7d28e17f72"  # Tự kiểm tra bằng mã băm chuẩn của chuỗi abc.
    print("Văn bản:", van_ban)  # In dữ liệu gốc để đối chiếu với mã băm.
    print("MD5 (128 bit, 32 ký tự hex):", bam_md5(van_ban))  # Tự tính và hiển thị giá trị băm viết thường của văn bản mẫu.
    print("Băm là một chiều: không có hàm giải mã.")  # Mã băm không chứa thao tác giải mã để lấy lại văn bản.
