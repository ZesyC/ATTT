# Mã Vigenere dùng các chữ của khóa làm số bước dịch; chỉ tiến khóa khi gặp A-Z hoặc a-z.
CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Bảng chữ hoa dùng để đổi chữ khóa thành độ dịch.
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"  # Bảng chữ thường giúp giữ nguyên kiểu chữ trong bản rõ.


def kiem_tra_khoa(khoa):  # Kiểm tra từ khóa và chuyển về dạng chữ hoa.
    if not isinstance(khoa, str) or not khoa:  # Khóa phải là một chuỗi không rỗng.
        raise ValueError("Khóa Vigenere phải là chuỗi chữ cái không rỗng.")  # Từ chối khóa rỗng để tránh chia dư cho 0.
    for ky_tu in khoa:  # Xét từng ký tự khóa trước khi chuyển hoa.
        if ky_tu not in CHU_HOA + CHU_THUONG:  # Chỉ cho dùng chữ cái tiếng Anh ASCII.
            raise ValueError("Khóa Vigenere chỉ chứa chữ A-Z hoặc a-z.")  # Không chấp nhận dấu cách, số hoặc chữ có dấu trong khóa.
    return khoa.upper()  # Chuẩn hóa chữ khóa để tra cứu chỉ trong một bảng.


def bien_doi(van_ban, khoa, huong):  # huong bằng 1 để mã hóa và -1 để giải mã.
    khoa = kiem_tra_khoa(khoa)  # Đảm bảo từ khóa dùng được và đã viết hoa.
    ket_qua = []  # Danh sách lưu từng ký tự đã xử lý.
    vi_tri_khoa = 0  # Đếm số chữ cái đã xử lý để biết dùng chữ khóa nào.
    for ky_tu in van_ban:  # Duyệt từng ký tự trong chuỗi cần biến đổi.
        if ky_tu in CHU_HOA:  # Chọn bảng chữ hoa nếu gặp ký tự A-Z.
            bang_chu = CHU_HOA  # Kết quả của chữ hoa sẽ tiếp tục là chữ hoa.
        elif ky_tu in CHU_THUONG:  # Chọn bảng chữ thường nếu gặp ký tự a-z.
            bang_chu = CHU_THUONG  # Kết quả của chữ thường sẽ tiếp tục là chữ thường.
        else:  # Không mã hóa ký tự ngoài hai bảng ASCII.
            ket_qua.append(ky_tu)  # Giữ nguyên dấu câu, khoảng trắng, số và chữ có dấu.
            continue  # Chuyển sang ký tự tiếp theo mà không tăng vị trí khóa.
        chu_khoa = khoa[vi_tri_khoa % len(khoa)]  # Lặp lại từ khóa khi đã dùng hết các chữ.
        do_dich = CHU_HOA.index(chu_khoa)  # A tương ứng dịch 0 bước, B dịch 1 bước, ..., Z dịch 25 bước.
        vi_tri = bang_chu.index(ky_tu)  # Đổi ký tự đầu vào thành chỉ số trong bảng phù hợp.
        ket_qua.append(bang_chu[(vi_tri + huong * do_dich) % 26])  # Cộng độ dịch để mã hóa hoặc trừ để giải mã.
        vi_tri_khoa += 1  # Chỉ chuyển chữ khóa sau khi đã xử lý một chữ cái.
    return "".join(ket_qua)  # Ghép các ký tự kết quả thành chuỗi.


def ma_hoa(van_ban, khoa):  # Cung cấp hàm mã hóa với tên dễ gọi.
    return bien_doi(van_ban, khoa, 1)  # Dịch sang phải theo từng chữ khóa.


def giai_ma(ban_ma, khoa):  # Cung cấp hàm giải mã dùng cùng từ khóa.
    return bien_doi(ban_ma, khoa, -1)  # Dịch sang trái để hoàn tác phép mã hóa.


if __name__ == "__main__":  # Chạy phần minh họa khi mở trực tiếp file này.
    ban_ro = "Attack at dawn!"  # Ví dụ có khoảng trắng và dấu chấm than không làm tiến khóa.
    khoa = "LEMON"  # Từ khóa được lặp lại trên các chữ của bản rõ.
    ban_ma = ma_hoa(ban_ro, khoa)  # Áp dụng các độ dịch từ khóa để tạo bản mã.
    ban_giai_ma = giai_ma(ban_ma, khoa)  # Áp dụng độ dịch ngược để khôi phục chuỗi ban đầu.
    print("Bản rõ:", ban_ro)  # In thông điệp trước khi mã hóa.
    print("Khóa:", khoa)  # In từ khóa đang sử dụng.
    print("Bản mã:", ban_ma)  # In chuỗi mã hóa giữ nguyên bố cục và kiểu chữ.
    print("Giải mã:", ban_giai_ma)  # In thông điệp sau khi giải mã.
    assert ban_giai_ma == ban_ro  # Xác nhận giải mã trả về đúng chuỗi ban đầu.
    assert ma_hoa("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"  # Kiểm tra ví dụ Vigenere có kết quả cố định.
