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


def chon(x: list[int], y: list[int], z: list[int]) -> list[int]:  # Hàm Ch: tại mỗi cột, x quyết định chọn phần tử của y hay z.
    return [b if a == 1 else c for a, b, c in zip(x, y, z)]  # Nếu x là 1 thì chọn y; nếu x là 0 thì chọn z, giống công thức Ch chuẩn.


def da_so(x: list[int], y: list[int], z: list[int]) -> list[int]:  # Hàm Maj: lấy giá trị chiếm đa số trong ba phần tử cùng cột.
    return [int(a + b + c >= 2) for a, b, c in zip(x, y, z)]  # Có ít nhất hai phần tử 1 thì trả 1; int đổi True/False thành 1/0.


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


def xoay_phai(mang: list[int], so_buoc: int) -> list[int]:  # Xoay vòng phải: đưa các phần tử cuối mảng lên đầu mảng.
    so_buoc %= len(mang)  # Xoay đủ một vòng sẽ trở lại mảng ban đầu.
    return mang[-so_buoc:] + mang[:-so_buoc]  # Ghép đoạn cuối trước đoạn đầu, giữ nguyên tổng số phần tử.


def dich_phai(mang: list[int], so_buoc: int) -> list[int]:  # Dịch phải khác xoay vòng: chèn 0 ở đầu và bỏ phần tử cuối.
    so_buoc = min(so_buoc, len(mang))  # Dịch quá độ dài từ thì kết quả chỉ còn các số 0.
    return [0] * so_buoc + mang[:len(mang) - so_buoc]  # Thao tác trực tiếp trên các lát mảng, giữ nguyên độ dài.


def dem_du_lieu(van_ban: str, do_dai_khoi: int, do_dai_truong: int) -> list[int]:  # Chuẩn bị dữ liệu chung cho SHA-1, SHA-256 và SHA-512.
    if not isinstance(van_ban, str):  # Chỉ nhận chuỗi văn bản để việc mã hóa UTF-8 được rõ ràng.
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")  # Giữ cách báo lỗi đầu vào giống phiên bản cũ.
    du_lieu = [bit for byte in van_ban.encode("utf-8") for bit in so_sang_mang(byte, 8)]  # UTF-8 đổi chữ thành byte; tự tách mỗi byte thành 8 phần tử 0/1.
    do_dai_ban_dau = len(du_lieu)  # Lưu độ dài tính bằng bit trước khi thêm phần đệm.
    if do_dai_ban_dau >= 2 ** do_dai_truong:  # Chuẩn SHA giới hạn độ dài theo số bit của trường ghi độ dài.
        raise ValueError("Dữ liệu vượt quá độ dài mà chuẩn SHA cho phép.")  # Không âm thầm cắt mất phần cao của độ dài.
    du_lieu.append(1)  # Bắt đầu phần đệm bằng đúng một phần tử 1.
    du_lieu.extend([0] * ((do_dai_khoi - do_dai_truong - len(du_lieu)) % do_dai_khoi))  # Thêm 0 tới vị trí dành cho trường độ dài; tự tăng khối nếu thiếu chỗ.
    du_lieu.extend(so_sang_mang(do_dai_ban_dau, do_dai_truong))  # SHA ghi độ dài big-endian: phần tử lớn nhất xuất hiện trước.
    return du_lieu  # Kết quả có độ dài chia hết cho 512 hoặc 1024 phần tử.


def bam_sha1(van_ban: str) -> str:  # SHA-1 viết tay, xử lý từ 32 phần tử và thực hiện 80 bước mỗi khối.
    du_lieu = dem_du_lieu(van_ban, 512, 64)  # Đệm theo khối 512 phần tử, trường độ dài chiếm 64 phần tử cuối.
    trang_thai = [so_sang_mang(so, 32) for so in [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]]  # Chuyển các giá trị khởi tạo chuẩn thành từng hàng 32 phần tử 0/1.
    bang_k = [so_sang_mang(so, 32) for so in [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6]]  # Đổi bảng hằng số thành ma trận các từ 32 phần tử.
    for dau_khoi in range(0, len(du_lieu), 512):  # Xử lý lần lượt các khối, mỗi khối là một mảng 512 phần tử.
        khoi = du_lieu[dau_khoi:dau_khoi + 512]  # Lấy riêng khối hiện tại để xây ma trận các từ.
        lich_tu = [khoi[i:i + 32] for i in range(0, 512, 32)]  # Tách thành ma trận ban đầu 16 hàng, mỗi hàng 32 phần tử.
        for i in range(16, 80):  # Mở rộng lịch thông điệp từ 16 lên 80 hàng.
            lich_tu.append(xoay_trai(xor(lich_tu[i - 3], lich_tu[i - 8], lich_tu[i - 14], lich_tu[i - 16]), 1))  # XOR bốn hàng cũ rồi xoay trái 1 phần tử để tạo hàng mới.
        a, b, c, d, e = trang_thai  # Năm mảng làm việc được khởi tạo từ giá trị băm trước khối.
        for i in range(80):  # Mỗi bước dùng một hàng trong lịch thông điệp.
            if i < 20:  # 20 bước đầu SHA-1 dùng hàm chọn Ch.
                f = chon(b, c, d)  # Chọn c hoặc d tại từng cột dựa vào phần tử tương ứng của b.
            elif i < 40 or i >= 60:  # Các bước 20-39 và 60-79 dùng parity, tức XOR ba mảng.
                f = xor(b, c, d)  # H hoặc hàm parity của SHA-1 lấy XOR của ba mảng.
            else:
                f = da_so(b, c, d)  # Các bước 40-59 dùng giá trị đa số tại từng cột.
            a_moi = cong(xoay_trai(a, 5), f, e, bang_k[i // 20], lich_tu[i])  # Cộng năm mảng theo công thức nén SHA-1; mỗi 20 bước đổi hằng số.
            a, b, c, d, e = a_moi, a, xoay_trai(b, 30), c, d  # Cập nhật năm mảng đồng thời; b cũ được xoay trái 30 vị trí.
        trang_thai = [cong(cu, moi) for cu, moi in zip(trang_thai, [a, b, c, d, e])]  # Cộng từng cặp từ để gộp kết quả khối vào trạng thái SHA-1.
    return "".join(f"{mang_sang_so(tu):08x}" for tu in trang_thai)  # Ghép năm từ big-endian thành chuỗi SHA-1 dài 40 ký tự hex.


def bam_sha2(van_ban: str, do_dai_tu: int) -> str:  # SHA-256 và SHA-512 có cùng khung thuật toán nên dùng chung phần vòng nén.
    if do_dai_tu == 32:  # SHA-256 dùng từ 32 phần tử, khối 512 phần tử và 64 bước.
        gia_tri_dau = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]  # Tám giá trị khởi tạo theo chuẩn SHA-2 tương ứng.
        hang_so = BANG_K_256  # Bảng 64 hằng số chuẩn dành cho SHA-256.
        sigma_nho_0, sigma_nho_1 = (7, 18, 3), (17, 19, 10)  # Hai số đầu là bước xoay phải, số cuối là bước dịch phải khi mở rộng lịch SHA-256.
        sigma_lon_0, sigma_lon_1 = (2, 13, 22), (6, 11, 25)  # Mỗi bộ ba là các bước xoay phải dùng trong vòng nén SHA-256.
    elif do_dai_tu == 64:  # SHA-512 dùng từ 64 phần tử, khối 1024 phần tử và 80 bước.
        gia_tri_dau = [  # Tám giá trị khởi tạo theo chuẩn SHA-2 tương ứng.
            0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
            0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
        ]
        hang_so = BANG_K_512  # Bảng 80 hằng số chuẩn dành cho SHA-512.
        sigma_nho_0, sigma_nho_1 = (1, 8, 7), (19, 61, 6)  # Các bước xoay và dịch trong lịch thông điệp SHA-512.
        sigma_lon_0, sigma_lon_1 = (28, 34, 39), (14, 18, 41)  # Các bước xoay phải trong vòng nén SHA-512.
    else:
        raise ValueError("Một từ SHA-2 phải dài 32 hoặc 64 phần tử.")  # Chỉ hỗ trợ đúng hai kích thước từ của SHA-256 và SHA-512.

    do_dai_khoi = do_dai_tu * 16  # Mỗi khối ban đầu luôn gồm 16 từ.
    du_lieu = dem_du_lieu(van_ban, do_dai_khoi, do_dai_tu * 2)  # Trường độ dài bằng hai từ: 64 bit cho SHA-256, 128 bit cho SHA-512.
    trang_thai = [so_sang_mang(so, do_dai_tu) for so in gia_tri_dau]  # Tám giá trị khởi tạo trở thành tám mảng cùng độ dài.
    bang_k = [so_sang_mang(so, do_dai_tu) for so in hang_so]  # Các hằng số cũng được xử lý dưới dạng mảng 0/1.
    for dau_khoi in range(0, len(du_lieu), do_dai_khoi):  # Duyệt từng khối của toàn bộ văn bản đã đệm.
        khoi = du_lieu[dau_khoi:dau_khoi + do_dai_khoi]  # Lát mảng của một khối 512 hoặc 1024 phần tử.
        lich_tu = [khoi[i:i + do_dai_tu] for i in range(0, do_dai_khoi, do_dai_tu)]  # Ma trận lịch thông điệp ban đầu có 16 hàng.
        for i in range(16, len(bang_k)):  # Mở rộng thành 64 hàng cho SHA-256 hoặc 80 hàng cho SHA-512.
            x, y = lich_tu[i - 15], lich_tu[i - 2]  # Chọn hai hàng cần biến đổi bằng các hàm sigma nhỏ.
            s0 = xor(xoay_phai(x, sigma_nho_0[0]), xoay_phai(x, sigma_nho_0[1]), dich_phai(x, sigma_nho_0[2]))  # Sigma nhỏ 0 kết hợp hai lần xoay phải và một lần dịch phải.
            s1 = xor(xoay_phai(y, sigma_nho_1[0]), xoay_phai(y, sigma_nho_1[1]), dich_phai(y, sigma_nho_1[2]))  # Sigma nhỏ 1 biến đổi hàng i-2 theo cùng cách với tham số khác.
            lich_tu.append(cong(lich_tu[i - 16], s0, lich_tu[i - 7], s1))  # Cộng bốn mảng để tạo hàng thứ i của lịch thông điệp.
        a, b, c, d, e, f, g, h = trang_thai  # Tám mảng làm việc giữ trạng thái bên trong vòng nén.
        for i in range(len(bang_k)):  # Số bước tương ứng với số hằng số chuẩn của thuật toán.
            s1 = xor(*(xoay_phai(e, buoc) for buoc in sigma_lon_1))  # Sigma lớn 1 là XOR của ba mảng e xoay phải; dấu * truyền ba mảng vào xor.
            t1 = cong(h, s1, chon(e, f, g), bang_k[i], lich_tu[i])  # T1 gộp h, sigma của e, Ch, hằng số bước và từ thông điệp.
            s0 = xor(*(xoay_phai(a, buoc) for buoc in sigma_lon_0))  # Sigma lớn 0 là XOR của ba mảng a xoay phải.
            t2 = cong(s0, da_so(a, b, c))  # T2 cộng sigma của a với hàm đa số của a, b, c.
            a, b, c, d, e, f, g, h = cong(t1, t2), a, b, c, cong(d, t1), e, f, g  # Cập nhật đồng thời: a mới bằng T1+T2, e mới bằng d+T1, các từ còn lại chuyển vị trí.
        trang_thai = [cong(cu, moi) for cu, moi in zip(trang_thai, [a, b, c, d, e, f, g, h])]  # Gộp tám mảng sau vòng nén vào trạng thái trước khối.
    return "".join(f"{mang_sang_so(tu):0{do_dai_tu // 4}x}" for tu in trang_thai)  # Chỉ lúc xuất mới đổi từ thành số; 4 phần tử nhị phân tương ứng 1 ký tự hex.


def bam_sha256(van_ban: str) -> str:  # API SHA-256 giữ nguyên tên và kiểu kết quả như trước.
    return bam_sha2(van_ban, 32)  # Chạy thuật toán SHA-2 viết tay với các từ 32 phần tử.


def bam_sha512(van_ban: str) -> str:  # API SHA-512 giữ nguyên tên và kiểu kết quả như trước.
    return bam_sha2(van_ban, 64)  # Chạy thuật toán SHA-2 viết tay với các từ 64 phần tử.


if __name__ == "__main__":  # Chỉ chạy minh họa khi thực thi trực tiếp file này.
    van_ban = "Xin chào Python!"  # Đổi chuỗi này để thử băm dữ liệu tiếng Việt khác.
    assert bam_sha1("abc") == "a9993e364706816aba3e25717850c26c9cd0d89d"  # Kiểm tra vector SHA-1 chuẩn.
    assert bam_sha256("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"  # Tự kiểm tra bằng mã băm chuẩn của chuỗi abc.
    assert bam_sha512("abc") == (  # Kiểm tra vector SHA-512 chuẩn dài 128 ký tự hex.
        "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a"
        "2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f"
    )
    print("Văn bản:", van_ban)  # In dữ liệu gốc để đối chiếu với mã băm.
    print("SHA-1 (160 bit, 40 ký tự hex):", bam_sha1(van_ban))  # Tự tính và hiển thị giá trị băm viết thường của văn bản mẫu.
    print("SHA-256 (256 bit, 64 ký tự hex):", bam_sha256(van_ban))  # Tự tính và hiển thị giá trị băm viết thường của văn bản mẫu.
    print("SHA-512 (512 bit, 128 ký tự hex):", bam_sha512(van_ban))  # Tự tính và hiển thị giá trị băm viết thường của văn bản mẫu.
    print("Băm là một chiều: không có hàm giải mã.")  # Mã băm không chứa thao tác giải mã để lấy lại văn bản.
