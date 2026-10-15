# Mã affine dùng công thức y = (a*x + b) mod 26, với A = 0, ..., Z = 25.
CHU_HOA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Bảng chữ hoa để đổi qua lại giữa chữ và số.
CHU_THUONG = "abcdefghijklmnopqrstuvwxyz"  # Bảng chữ thường để giữ nguyên kiểu chữ của đầu vào.


def nghich_dao_mod_26(a):  # Tìm số nhân với a cho phần dư bằng 1 khi chia 26.
    for so in range(1, 26):  # Thử 25 giá trị vì bảng chữ cái chỉ có 26 chữ.
        if (a * so) % 26 == 1:  # Điều kiện định nghĩa nghịch đảo nhân modulo 26.
            return so  # Trả về nghịch đảo đầu tiên tìm được.
    raise ValueError("a phải nguyên tố cùng nhau với 26, ví dụ 5 hoặc 7.")  # Không có nghịch đảo thì không thể giải mã duy nhất.


def kiem_tra_khoa(a, b):  # Kiểm tra hai số tạo thành khóa affine.
    if type(a) is not int or type(b) is not int:  # a và b phải là số nguyên để tính chỉ số chữ.
        raise ValueError("Hai thành phần a và b phải là số nguyên.")  # Từ chối khóa sai kiểu.
    return nghich_dao_mod_26(a)  # Đồng thời kiểm tra tính khả nghịch của a và trả về nghịch đảo.


def bien_doi(van_ban, he_so, do_dich):  # Áp dụng công thức tuyến tính cho cả mã hóa và giải mã.
    ket_qua = []  # Thu thập từng ký tự kết quả.
    for ky_tu in van_ban:  # Duyệt lần lượt từng ký tự đầu vào.
        if ky_tu in CHU_HOA:  # Xử lý chữ hoa thuộc A-Z.
            vi_tri = CHU_HOA.index(ky_tu)  # Quy đổi chữ hoa thành chỉ số 0 đến 25.
            ket_qua.append(CHU_HOA[(he_so * vi_tri + do_dich) % 26])  # Tính chỉ số mới rồi đổi về chữ hoa.
        elif ky_tu in CHU_THUONG:  # Xử lý riêng chữ thường để giữ nguyên kiểu chữ.
            vi_tri = CHU_THUONG.index(ky_tu)  # Quy đổi chữ thường thành chỉ số 0 đến 25.
            ket_qua.append(CHU_THUONG[(he_so * vi_tri + do_dich) % 26])  # Áp dụng cùng công thức trong bảng chữ thường.
        else:  # Số, dấu câu và chữ ngoài bảng ASCII không tham gia phép tính.
            ket_qua.append(ky_tu)  # Giữ nguyên những ký tự không mã hóa.
    return "".join(ket_qua)  # Ghép danh sách ký tự thành chuỗi.


def ma_hoa(van_ban, a, b):  # Nhận bản rõ và hai thành phần khóa affine.
    kiem_tra_khoa(a, b)  # Bảo đảm dữ liệu mã hóa sẽ giải mã được bằng khóa này.
    return bien_doi(van_ban, a, b)  # Tính y = (a*x + b) mod 26 cho từng chữ.


def giai_ma(ban_ma, a, b):  # Khôi phục chữ từ bản mã bằng nghịch đảo của a.
    a_nghich_dao = kiem_tra_khoa(a, b)  # Lấy a^(-1) modulo 26 sau khi kiểm tra khóa.
    return bien_doi(ban_ma, a_nghich_dao, -a_nghich_dao * b)  # Tính x = a^(-1)*(y-b) mod 26.


if __name__ == "__main__":  # Chỉ chạy phần minh họa khi file được thực thi trực tiếp.
    ban_ro = "Affine Cipher!"  # Chuỗi mẫu gồm chữ hoa, chữ thường và dấu câu.
    a, b = 5, 8  # Chọn a có nghịch đảo modulo 26 và độ dịch b bằng 8.
    ban_ma = ma_hoa(ban_ro, a, b)  # Mã hóa chuỗi bằng công thức affine.
    ban_giai_ma = giai_ma(ban_ma, a, b)  # Giải mã bằng nghịch đảo nhân của a.
    print("Bản rõ:", ban_ro)  # In chuỗi gốc.
    print("Khóa (a, b):", (a, b))  # In hai thành phần của khóa.
    print("Bản mã:", ban_ma)  # In chuỗi đã mã hóa.
    print("Giải mã:", ban_giai_ma)  # In chuỗi sau khi khôi phục.
    assert ban_giai_ma == ban_ro  # Kiểm tra kết quả giải mã trùng hoàn toàn chuỗi gốc.
    assert ma_hoa("AFFINECIPHER", 5, 8) == "IHHWVCSWFRCP"  # Kiểm tra một ví dụ affine có kết quả cố định.
