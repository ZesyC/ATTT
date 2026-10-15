"""RSA không có padding, dùng số nguyên tố nhỏ: chỉ để học, không dùng bảo mật thực tế."""  # Bản RSA sách giáo khoa này không có lớp đệm an toàn như RSA-OAEP.

from math import gcd, isqrt  # gcd tính ước chung lớn nhất; isqrt tính phần nguyên của căn bậc hai.


def la_so_nguyen_to(so: int) -> bool:  # Trả về True nếu số đầu vào là số nguyên tố.
    if type(so) is not int or so < 2:  # Số nguyên tố phải là số nguyên và ít nhất bằng 2; loại cả True/False.
        return False  # Dừng kiểm tra nếu đầu vào không thể là số nguyên tố.
    for uoc in range(2, isqrt(so) + 1):  # Chỉ cần thử các ước từ 2 đến căn bậc hai của số.
        if so % uoc == 0:  # Phép chia dư bằng 0 nghĩa là đã tìm thấy một ước khác 1 và chính nó.
            return False  # Có ước khác thì số đang xét không phải số nguyên tố.
    return True  # Không tìm được ước nào thì kết luận là số nguyên tố.


def tao_khoa(p: int, q: int, e: int = 17) -> tuple[tuple[int, int], tuple[int, int]]:  # Tạo cặp khóa công khai và bí mật; e mặc định là 17.
    if not la_so_nguyen_to(p) or not la_so_nguyen_to(q) or p == q:  # Công thức phi bên dưới cần hai số nguyên tố khác nhau.
        raise ValueError("p và q phải là hai số nguyên tố khác nhau.")  # Báo rõ lỗi đầu vào thay vì tạo khóa sai.
    n = p * q  # n là mô-đun chung xuất hiện trong cả hai khóa.
    phi = (p - 1) * (q - 1)  # Với hai số nguyên tố khác nhau, hàm Euler của n bằng tích này.
    if n <= 255:  # Mỗi byte UTF-8 nằm từ 0 đến 255 nên n phải lớn hơn 255.
        raise ValueError("p * q phải lớn hơn 255 để mã hóa từng byte UTF-8.")  # Yêu cầu chọn p và q lớn hơn nếu tích quá nhỏ.
    if type(e) is not int or not 1 < e < phi or gcd(e, phi) != 1:  # e phải nguyên tố cùng nhau với phi để có nghịch đảo.
        raise ValueError("e phải là số nguyên, 1 < e < phi và gcd(e, phi) = 1.")  # Thông báo đầy đủ điều kiện chọn số mũ e.
    d = pow(e, -1, phi)  # Tìm nghịch đảo mô-đun: e * d chia phi dư 1.
    return (e, n), (d, n)  # Trả lần lượt khóa công khai để mã hóa và khóa bí mật để giải mã.


def kiem_tra_khoa(khoa: tuple[int, int]) -> None:  # Kiểm tra dạng khóa trước khi thực hiện phép tính RSA.
    if not isinstance(khoa, tuple) or len(khoa) != 2:  # Mỗi khóa phải là một tuple chứa đúng hai phần tử.
        raise ValueError("Khóa phải có dạng (số mũ, n).")  # Tránh lỗi khi tách khóa sai cấu trúc.
    so_mu, n = khoa  # Tách số mũ và mô-đun để kiểm tra riêng.
    if type(so_mu) is not int or type(n) is not int:  # Loại chuỗi, số thực và giá trị boolean trong khóa.
        raise ValueError("Số mũ và n phải là số nguyên.")  # RSA thực hiện các phép toán trên số nguyên.
    if n <= 255 or not 1 < so_mu < n:  # Giới hạn phù hợp với khóa do tao_khoa tạo và cách mã hóa từng byte.
        raise ValueError("Khóa phải có n > 255 và 1 < số mũ < n.")  # Báo khóa không thỏa điều kiện của ví dụ này.


def ma_hoa(van_ban: str, khoa_cong_khai: tuple[int, int]) -> list[int]:  # Nhận chuỗi và khóa công khai, trả danh sách số mã hóa.
    kiem_tra_khoa(khoa_cong_khai)  # Kiểm tra cấu trúc và giá trị khóa trước khi dùng.
    if not isinstance(van_ban, str):  # Hàm này nhận văn bản thay vì dữ liệu nhị phân hay số.
        raise ValueError("Văn bản cần mã hóa phải là chuỗi.")  # Báo lỗi kiểu dữ liệu đầu vào dễ hiểu.
    e, n = khoa_cong_khai  # Lấy số mũ công khai e và mô-đun n.
    ban_ma = []  # Tạo danh sách rỗng để chứa kết quả mã hóa từng byte.
    for byte in van_ban.encode("utf-8"):  # Chuyển văn bản thành byte UTF-8 để hỗ trợ cả tiếng Việt.
        ban_ma.append(pow(byte, e, n))  # Mã hóa theo c = m^e mod n và thêm kết quả vào danh sách.
    return ban_ma  # Trả toàn bộ bản mã dạng danh sách số nguyên.


def giai_ma(ban_ma: list[int], khoa_bi_mat: tuple[int, int]) -> str:  # Nhận danh sách bản mã và khóa bí mật, trả văn bản gốc.
    kiem_tra_khoa(khoa_bi_mat)  # Kiểm tra khóa trước khi thực hiện phép giải mã.
    if not isinstance(ban_ma, list):  # Bản mã của ví dụ phải là một danh sách.
        raise ValueError("Bản mã phải là danh sách các số nguyên.")  # Báo sai cấu trúc bản mã.
    d, n = khoa_bi_mat  # Lấy số mũ bí mật d và mô-đun n.
    du_lieu = bytearray()  # bytearray cho phép thêm từng byte đã giải mã.
    for so in ban_ma:  # Xử lý lần lượt từng số nguyên trong bản mã.
        if type(so) is not int or not 0 <= so < n:  # Mỗi phần tử phải thuộc miền bản mã RSA từ 0 đến n - 1.
            raise ValueError("Mỗi số trong bản mã phải thỏa mãn 0 <= số < n.")  # Không âm thầm chấp nhận số ngoài miền hợp lệ.
        byte = pow(so, d, n)  # Giải mã theo m = c^d mod n.
        if byte > 255:  # Một kết quả vượt 255 không thể biểu diễn bằng một byte.
            raise ValueError("Bản mã hoặc khóa không hợp lệ: kết quả không phải byte.")  # Báo lỗi thường gặp khi dùng sai khóa hoặc bản mã.
        du_lieu.append(byte)  # Ghép byte đã giải mã vào chuỗi dữ liệu nhị phân.
    try:  # Thử chuyển dữ liệu nhị phân trở lại thành văn bản.
        return du_lieu.decode("utf-8")  # Giải mã UTF-8 để khôi phục đúng dấu tiếng Việt.
    except UnicodeDecodeError as loi:  # Bắt trường hợp các byte không tạo thành văn bản UTF-8 hợp lệ.
        raise ValueError("Bản mã hoặc khóa không tạo ra văn bản UTF-8 hợp lệ.") from loi  # Đổi lỗi kỹ thuật thành thông báo dễ hiểu và giữ nguyên nguyên nhân.


if __name__ == "__main__":  # Chỉ chạy ví dụ bên dưới khi thực thi trực tiếp file này.
    p, q, e = 61, 53, 17  # Chọn hai số nguyên tố nhỏ và số mũ quen thuộc trong ví dụ RSA.
    khoa_cong_khai, khoa_bi_mat = tao_khoa(p, q, e)  # Tạo khóa (17, 3233) và (2753, 3233).
    van_ban = "Xin chào Python!"  # Thay chuỗi này để thử mã hóa văn bản khác.
    ban_ma = ma_hoa(van_ban, khoa_cong_khai)  # Mã hóa các byte của văn bản bằng khóa công khai.
    ban_giai_ma = giai_ma(ban_ma, khoa_bi_mat)  # Dùng khóa bí mật khôi phục văn bản từ danh sách bản mã.
    assert ban_giai_ma == van_ban  # Kiểm tra vòng mã hóa rồi giải mã phải giữ nguyên văn bản.
    assert pow(65, e, p * q) == 2790  # Kiểm tra ví dụ số học chuẩn: 65^17 mod 3233 = 2790.
    assert pow(2790, khoa_bi_mat[0], p * q) == 65  # Kiểm tra giải mã số 2790 bằng d = 2753 thu được 65.
    print("p, q, e:", p, q, e)  # In các tham số ban đầu để dễ đối chiếu công thức.
    print("Khóa công khai (e, n):", khoa_cong_khai)  # Hiển thị cặp số dùng để mã hóa.
    print("Khóa bí mật (d, n):", khoa_bi_mat)  # Chỉ in khóa bí mật trong bài học; hệ thống thực tế phải giữ kín.
    print("Bản gốc:", van_ban)  # In văn bản trước khi mã hóa.
    print("Bản mã:", ban_ma)  # In danh sách số sau khi mã hóa RSA.
    print("Giải mã:", ban_giai_ma)  # In văn bản khôi phục để so sánh với bản gốc.
