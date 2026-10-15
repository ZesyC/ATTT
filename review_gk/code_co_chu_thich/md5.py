"""MD5 là hàm băm một chiều; không có thao tác giải mã, không dùng cho bảo mật mới."""  # MD5 đã có lỗ hổng va chạm nên ví dụ này chỉ phục vụ học tập.

import hashlib  # Thư viện chuẩn của Python cung cấp sẵn các thuật toán băm.


def bam_md5(van_ban: str) -> str:  # Nhận văn bản và trả chuỗi biểu diễn giá trị băm MD5.
    if not isinstance(van_ban, str):  # Chỉ chấp nhận chuỗi văn bản để chuyển sang UTF-8.
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")  # Báo lỗi đầu vào thay vì gọi encode trên kiểu dữ liệu sai.
    du_lieu = van_ban.encode("utf-8")  # Chuyển chuỗi, gồm cả tiếng Việt, thành dữ liệu byte.
    ket_qua = hashlib.md5(du_lieu, usedforsecurity=False)  # Tính MD5 và khai báo đây là mục đích học tập, không phục vụ bảo mật.
    return ket_qua.hexdigest()  # Trả kết quả 128 bit dưới dạng 32 ký tự hệ 16.


if __name__ == "__main__":  # Chỉ chạy ví dụ khi thực thi file này trực tiếp.
    van_ban = "Xin chào Python!"  # Thay chuỗi này để thử băm văn bản khác.
    assert bam_md5("abc") == "900150983cd24fb0d6963f7d28e17f72"  # Đối chiếu với giá trị MD5 chuẩn của chuỗi abc.
    print("Văn bản:", van_ban)  # Hiển thị dữ liệu trước khi băm.
    print("MD5 (128 bit, 32 ký tự hex):", bam_md5(van_ban))  # Tính và in mã băm MD5 của văn bản.
    print("Băm là một chiều: không có hàm giải mã.")  # Nhắc rằng hàm băm không phải thuật toán mã hóa có thể đảo ngược.
