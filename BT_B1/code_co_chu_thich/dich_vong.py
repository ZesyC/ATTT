# Mã dịch vòng: dịch từng chữ A-Z hoặc a-z; giữ nguyên dấu, số và khoảng trắng.
CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Bảng chữ hoa gồm 26 chữ cái tiếng Anh.
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"  # Bảng chữ thường có cùng thứ tự với bảng chữ hoa.


def ma_hoa(van_ban, khoa):  # Nhận chuỗi cần mã hóa và số bước dịch nguyên.
    if type(khoa) is not int:  # Chỉ chấp nhận khóa là số nguyên, không chấp nhận số thực hay bool.
        raise ValueError("Khóa dịch vòng phải là số nguyên.")  # Báo lỗi nếu không thể dùng khóa để dịch chữ.
    ket_qua = []  # Gom từng ký tự đầu ra vào danh sách.
    for ky_tu in van_ban:  # Duyệt lần lượt các ký tự trong chuỗi đầu vào.
        if ky_tu in CHU_HOA:  # Chỉ xử lý ký tự thuộc bảng chữ hoa ASCII.
            vi_tri = CHU_HOA.index(ky_tu)  # Đổi A thành 0, B thành 1, ..., Z thành 25.
            ket_qua.append(CHU_HOA[(vi_tri + khoa) % 26])  # Dịch sang phải và quay vòng sau chữ Z.
        elif ky_tu in CHU_THUONG:  # Xử lý chữ thường bằng bảng riêng để giữ nguyên kiểu chữ.
            vi_tri = CHU_THUONG.index(ky_tu)  # Tìm vị trí từ 0 đến 25 của chữ thường.
            ket_qua.append(CHU_THUONG[(vi_tri + khoa) % 26])  # Dịch chữ thường với cùng khóa.
        else:  # Các ký tự ngoài A-Z và a-z không thuộc bảng mã này.
            ket_qua.append(ky_tu)  # Giữ nguyên dấu câu, số, khoảng trắng và chữ có dấu.
    return "".join(ket_qua)  # Nối các ký tự đã xử lý thành một chuỗi.


def giai_ma(ban_ma, khoa):  # Giải mã bằng cách dịch ngược đúng số bước đã dùng.
    if type(khoa) is not int:  # Kiểm tra kiểu trước khi lấy số đối của khóa.
        raise ValueError("Khóa dịch vòng phải là số nguyên.")  # Báo lỗi thống nhất với hàm mã hóa.
    return ma_hoa(ban_ma, -khoa)  # Khóa âm đưa từng chữ về vị trí ban đầu.


if __name__ == "__main__":  # Chỉ chạy ví dụ khi mở trực tiếp file này bằng Python.
    ban_ro = "Hello, Python! 123"  # Chuỗi mẫu có cả chữ hoa, chữ thường và ký tự giữ nguyên.
    khoa = 3  # Mỗi chữ được dịch sang phải 3 vị trí.
    ban_ma = ma_hoa(ban_ro, khoa)  # Tạo bản mã từ bản rõ.
    ban_giai_ma = giai_ma(ban_ma, khoa)  # Khôi phục bản rõ bằng cùng khóa.
    print("Bản rõ:", ban_ro)  # In dữ liệu trước khi mã hóa.
    print("Khóa:", khoa)  # In số bước dịch đang sử dụng.
    print("Bản mã:", ban_ma)  # In kết quả mã hóa để quan sát sự dịch chữ.
    print("Giải mã:", ban_giai_ma)  # In chuỗi sau khi giải mã.
    assert ban_giai_ma == ban_ro  # Kiểm tra mã hóa rồi giải mã không làm thay đổi chuỗi.
    assert ma_hoa("ABC xyz", 3) == "DEF abc"  # Kiểm tra cả phép dịch thường và phép quay vòng.
