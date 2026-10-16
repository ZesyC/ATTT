def giai_ma(ban_ma, khoa):  # Tạo hàm giải mã dịch vòng với bản mã và khóa số.
    ban_ro = ""  # Tạo chuỗi rỗng để lưu bản rõ.
    for chu in ban_ma:  # Duyệt lần lượt từng chữ cái trong bản mã.
        vi_tri = ord(chu) - ord("a")  # Đổi chữ thành số từ 0 đến 25: a = 0, b = 1, ...
        vi_tri_moi = (vi_tri - khoa) % 26  # Trừ khóa và lấy dư 26 để quay vòng trong bảng chữ cái.
        ban_ro += chr(vi_tri_moi + ord("a"))  # Đổi số về chữ và nối vào bản rõ.
    return ban_ro  # Trả về chuỗi đã giải mã bằng khóa đang thử.


def giai_ma_vigenere(ban_ma, khoa):  # Giải mã Vigenere cho bản mã và khóa chỉ gồm chữ thường a-z.
    if not khoa or any(chu < "a" or chu > "z" for chu in khoa):  # Từ chối khóa rỗng hoặc chứa ký tự ngoài a-z.
        raise ValueError("Khóa Vigenere phải gồm các chữ thường a-z.")  # Báo lỗi khi khóa không hợp lệ.
    ban_ro = ""  # Chuẩn bị chuỗi chứa kết quả giải mã.
    for i in range(len(ban_ma)):  # Duyệt từng vị trí ký tự của bản mã.
        vi_tri = ord(ban_ma[i]) - ord("a")  # Đổi chữ bản mã thành số từ 0 đến 25.
        do_dich = ord(khoa[i % len(khoa)]) - ord("a")  # Lặp lại khóa và lấy số dịch riêng cho vị trí hiện tại.
        vi_tri_moi = (vi_tri - do_dich) % 26  # Trừ số dịch rồi lấy dư 26 để quay vòng bảng chữ cái.
        ban_ro += chr(vi_tri_moi + ord("a"))  # Đổi vị trí đã giải mã về chữ và ghép vào bản rõ.
    return ban_ro  # Trả về bản rõ theo khóa Vigenere đang thử.


def tham_ma_vigenere(ban_ma):  # Vét cạn khóa dài 1 đến 3 chữ; chưa thử các khóa dài hơn.
    with open("ket_qua_vigenere.txt", "w", encoding="utf-8") as tep:  # Ghi lại các ứng viên vào tệp trong thư mục đang chạy.
        for do_dai in range(1, 4):  # Thử lần lượt các độ dài khóa 1, 2 và 3.
            for so in range(26 ** do_dai):  # Có 26 mũ độ dài cách chọn khóa với từng độ dài.
                khoa = ""  # Khởi tạo khóa mới cho mỗi số đang xét.
                for i in range(do_dai):  # Chuyển số thành đúng số chữ cái của độ dài khóa.
                    khoa = chr(so % 26 + ord("a")) + khoa  # Đổi phần dư thành chữ a-z và thêm vào đầu khóa.
                    so //= 26  # Bỏ chữ số cơ số 26 vừa chuyển để xử lý chữ tiếp theo.
                ban_ro = giai_ma_vigenere(ban_ma, khoa)  # Giải mã bằng khóa vừa sinh mà không cần biết khóa trước.
                tep.write(f"Khóa: {khoa} | Bản rõ: {ban_ro}\n")  # Lưu từng khóa và bản rõ để người đọc tìm kết quả có nghĩa.


if __name__ == "__main__":  # Chạy phần bên dưới khi mở trực tiếp tệp này bằng Python.
    ban_ma = "tyltsrekyreytfex"  # Lưu bản mã chữ thường a-z theo đề bài.
    print("Thử 26 khóa dịch vòng:")  # Hiển thị phần vét cạn mã dịch vòng.
    for khoa in range(26):  # Thử tất cả 26 khóa dịch vòng, từ 0 đến 25.
        ban_ro = giai_ma(ban_ma, khoa)  # Giải mã bằng từng khóa, chưa cần biết khóa đúng.
        print(f"Khóa: {khoa:2} | Bản rõ: {ban_ro}")  # In ứng viên của mã dịch vòng để tự chọn dòng có nghĩa.
    tham_ma_vigenere(ban_ma)  # Thử thêm toàn bộ khóa Vigenere dài từ 1 đến 3 chữ.
    print("Đã thử mọi khóa Vigenere dài 1 đến 3 chữ.")  # Thông báo phạm vi khóa đã thử, không kết luận khóa dài hơn.
    print("Xem các bản rõ ứng viên trong ket_qua_vigenere.txt.")  # Chỉ nơi xem kết quả để chọn bản rõ có nghĩa.
