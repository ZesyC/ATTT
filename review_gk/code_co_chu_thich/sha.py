"""SHA là họ hàm băm một chiều; SHA-1 chỉ dùng để học, ưu tiên SHA-256 hoặc SHA-512."""  # SHA-1 có lỗ hổng va chạm; các hàm SHA không có thao tác giải mã.

import hashlib  # Dùng thư viện chuẩn Python, không cần cài thêm gói bên ngoài.


def bam_sha1(van_ban: str) -> str:  # Nhận văn bản và trả giá trị băm SHA-1 dưới dạng hex.
    if not isinstance(van_ban, str):  # Kiểm tra đầu vào là chuỗi văn bản.
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")  # Báo lỗi rõ ràng nếu truyền kiểu dữ liệu khác.
    du_lieu = van_ban.encode("utf-8")  # Chuyển văn bản sang byte, giữ được dấu tiếng Việt.
    return hashlib.sha1(du_lieu, usedforsecurity=False).hexdigest()  # Băm SHA-1 cho học tập rồi chuyển 160 bit thành 40 ký tự hex.


def bam_sha256(van_ban: str) -> str:  # Hàm băm SHA-256 tạo giá trị băm dài 256 bit.
    if not isinstance(van_ban, str):  # Kiểm tra kiểu dữ liệu trước khi chuyển mã văn bản.
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")  # Không chấp nhận số hoặc các đối tượng khác thay cho chuỗi.
    du_lieu = van_ban.encode("utf-8")  # Biểu diễn văn bản thành byte theo mã hóa UTF-8.
    return hashlib.sha256(du_lieu).hexdigest()  # Tính SHA-256 và trả kết quả gồm 64 ký tự hex.


def bam_sha512(van_ban: str) -> str:  # Hàm băm SHA-512 tạo giá trị băm dài 512 bit.
    if not isinstance(van_ban, str):  # Bảo đảm đầu vào đúng kiểu chuỗi.
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")  # Dừng với thông báo dễ hiểu khi nhận kiểu sai.
    du_lieu = van_ban.encode("utf-8")  # Chuyển văn bản thành dữ liệu byte mà thuật toán băm xử lý.
    return hashlib.sha512(du_lieu).hexdigest()  # Tính SHA-512 và trả kết quả gồm 128 ký tự hex.


if __name__ == "__main__":  # Chỉ thực hiện phần minh họa khi chạy trực tiếp file này.
    van_ban = "Xin chào Python!"  # Đổi chuỗi này để so sánh kết quả của ba hàm băm.
    assert bam_sha256("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"  # Kiểm tra với giá trị SHA-256 chuẩn của abc.
    print("Văn bản:", van_ban)  # In dữ liệu đầu vào chung cho cả ba thuật toán.
    print("SHA-1 (160 bit, 40 ký tự hex):", bam_sha1(van_ban))  # Hiển thị mã băm SHA-1 của văn bản.
    print("SHA-256 (256 bit, 64 ký tự hex):", bam_sha256(van_ban))  # Hiển thị mã băm SHA-256 của văn bản.
    print("SHA-512 (512 bit, 128 ký tự hex):", bam_sha512(van_ban))  # Hiển thị mã băm SHA-512 của văn bản.
    print("Băm là một chiều: không có hàm giải mã.")  # Nhắc sự khác nhau giữa băm dữ liệu và mã hóa có giải mã.
