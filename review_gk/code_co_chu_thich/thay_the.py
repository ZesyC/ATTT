# Mã thay thế đơn bảng: khóa cho biết chữ thay thế cho A, B, ..., Z theo thứ tự.
CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Bảng chữ gốc dùng để tìm vị trí chữ.
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"  # Bảng chữ thường giúp nhận diện đúng ký tự ASCII.


def kiem_tra_khoa(khoa):  # Chuẩn hóa và kiểm tra bảng thay thế do người dùng cung cấp.
    if not isinstance(khoa, str) or len(khoa) != 26:  # Khóa phải là chuỗi gồm đúng 26 chữ.
        raise ValueError("Khóa phải chứa đúng 26 chữ cái A-Z khác nhau.")  # Từ chối khóa thiếu hoặc thừa ký tự.
    for ky_tu in khoa:  # Kiểm tra trước khi chuyển hoa để tránh chấp nhận ký tự Unicode đặc biệt.
        if ky_tu not in CHU_HOA + CHU_THUONG:  # Chỉ cho phép chữ cái tiếng Anh có hoặc không viết hoa.
            raise ValueError("Khóa chỉ được chứa chữ A-Z hoặc a-z.")  # Không cho dùng số, dấu hoặc chữ có dấu.
    khoa = khoa.upper()  # Đưa toàn bộ khóa về chữ hoa để dễ tra cứu.
    if set(khoa) != set(CHU_HOA):  # Tập ký tự phải bằng toàn bộ bảng chữ cái, không được lặp chữ.
        raise ValueError("Các chữ trong khóa không được trùng nhau.")  # Chữ trùng khiến phép giải mã không còn duy nhất.
    return khoa  # Trả về khóa hợp lệ đã viết hoa.


def thay_chu(van_ban, bang_nguon, bang_dich):  # Thay chữ theo vị trí tương ứng giữa hai bảng.
    ket_qua = []  # Lưu các ký tự đã thay thế.
    for ky_tu in van_ban:  # Duyệt từng ký tự của bản rõ hoặc bản mã.
        if ky_tu in CHU_HOA:  # Nhận diện chữ hoa trong bảng ASCII.
            vi_tri = bang_nguon.index(ky_tu)  # Tìm vị trí của chữ trong bảng nguồn.
            ket_qua.append(bang_dich[vi_tri])  # Lấy chữ ở cùng vị trí trong bảng đích.
        elif ky_tu in CHU_THUONG:  # Nhận diện chữ thường để bảo toàn kiểu chữ.
            vi_tri = bang_nguon.index(ky_tu.upper())  # Tra cứu bằng phiên bản chữ hoa của ký tự.
            ket_qua.append(bang_dich[vi_tri].lower())  # Chuyển kết quả về chữ thường như đầu vào.
        else:  # Những ký tự không phải chữ tiếng Anh không tham gia phép thay thế.
            ket_qua.append(ky_tu)  # Giữ nguyên ký tự ngoài bảng mã.
    return "".join(ket_qua)  # Ghép các ký tự thành chuỗi kết quả.


def ma_hoa(van_ban, khoa):  # Mã hóa bằng cách ánh xạ bảng gốc sang bảng khóa.
    khoa = kiem_tra_khoa(khoa)  # Đảm bảo khóa tạo thành một bảng thay thế đầy đủ.
    return thay_chu(van_ban, CHU_HOA, khoa)  # A được thay bằng chữ thứ nhất trong khóa, B bằng chữ thứ hai.


def giai_ma(ban_ma, khoa):  # Giải mã bằng cách đổi chiều ánh xạ.
    khoa = kiem_tra_khoa(khoa)  # Dùng cùng quy tắc kiểm tra khóa như khi mã hóa.
    return thay_chu(ban_ma, khoa, CHU_HOA)  # Tìm chữ trong bảng khóa rồi trả về chữ trong bảng gốc.


if __name__ == "__main__":  # Chạy ví dụ khi thực thi trực tiếp file này.
    ban_ro = "Hello, Python! 123"  # Bản rõ mẫu để quan sát cách giữ kiểu chữ và dấu câu.
    khoa = "QWERTYUIOPASDFGHJKLZXCVBNM"  # Một hoán vị gồm đủ 26 chữ cái tiếng Anh.
    ban_ma = ma_hoa(ban_ro, khoa)  # Thay các chữ của bản rõ theo bảng khóa.
    ban_giai_ma = giai_ma(ban_ma, khoa)  # Dùng bảng ngược để khôi phục bản rõ.
    print("Bản rõ:", ban_ro)  # Hiển thị chuỗi đầu vào.
    print("Khóa:", khoa)  # Hiển thị bảng thay thế đang sử dụng.
    print("Bản mã:", ban_ma)  # Hiển thị kết quả thay thế chữ.
    print("Giải mã:", ban_giai_ma)  # Hiển thị kết quả khôi phục.
    assert ban_giai_ma == ban_ro  # Xác nhận chu trình mã hóa và giải mã trả về đúng dữ liệu.
    assert ma_hoa("Abc xyz", khoa) == "Qwe bnm"  # Kiểm tra trực tiếp các vị trí đầu và cuối bảng khóa.
