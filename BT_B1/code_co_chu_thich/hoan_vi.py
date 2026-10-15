# Hoán vị theo khối: khóa [3,1,4,2] biến ABCD thành CADB bằng cách đọc vị trí 3,1,4,2.
# Đệm khoảng trắng cho khối cuối; lưu số đệm để giữ nguyên khoảng trắng thật ở cuối bản rõ.


def kiem_tra_khoa(khoa):  # Kiểm tra khóa là một hoán vị của các vị trí từ 1 đến n.
    if not isinstance(khoa, (list, tuple)) or not khoa:  # Khóa phải là danh sách hoặc tuple không rỗng.
        raise ValueError("Khóa hoán vị phải là danh sách vị trí không rỗng.")  # Không thể chia chuỗi thành khối có độ dài 0.
    for vi_tri in khoa:  # Kiểm tra kiểu dữ liệu của từng vị trí.
        if type(vi_tri) is not int:  # Mỗi phần tử phải là số nguyên, không dùng bool hoặc số thực.
            raise ValueError("Các vị trí trong khóa phải là số nguyên.")  # Chỉ số chuỗi cần có kiểu nguyên.
    if sorted(khoa) != list(range(1, len(khoa) + 1)):  # Khóa phải chứa đủ 1 đến n, mỗi vị trí xuất hiện đúng một lần.
        raise ValueError("Khóa phải là hoán vị của các số từ 1 đến độ dài khóa.")  # Loại bỏ khóa trùng, thiếu hoặc vượt phạm vi.


def ma_hoa(van_ban, khoa):  # Hoán đổi vị trí ký tự trong từng khối có độ dài bằng độ dài khóa.
    kiem_tra_khoa(khoa)  # Bảo đảm mỗi ký tự trong khối xuất hiện đúng một lần ở đầu ra.
    kich_thuoc = len(khoa)  # Một khối có n ký tự khi khóa có n vị trí.
    so_ky_tu_dem = (-len(van_ban)) % kich_thuoc  # Tính số khoảng trắng ít nhất cần thêm để đủ khối.
    van_ban = van_ban + " " * so_ky_tu_dem  # Chỉ thêm đệm ở cuối chuỗi, giữ nguyên nội dung ban đầu.
    ket_qua = []  # Lưu các ký tự sau khi sắp xếp lại trong từng khối.
    for bat_dau in range(0, len(van_ban), kich_thuoc):  # Lần lượt lấy các khối liên tiếp không chồng lấn.
        khoi = van_ban[bat_dau:bat_dau + kich_thuoc]  # Cắt đúng một khối có đủ n ký tự.
        for vi_tri in khoa:  # Đọc các vị trí trong khối theo thứ tự được ghi trong khóa.
            ket_qua.append(khoi[vi_tri - 1])  # Trừ 1 vì khóa đánh số từ 1 nhưng Python đánh chỉ số từ 0.
    return "".join(ket_qua), so_ky_tu_dem  # Trả về bản mã và số khoảng trắng đã thêm.


def giai_ma(ban_ma, khoa, so_ky_tu_dem=0):  # Đưa ký tự về vị trí cũ và bỏ đúng số khoảng trắng đệm.
    kiem_tra_khoa(khoa)  # Áp dụng cùng quy tắc khóa như khi mã hóa.
    kich_thuoc = len(khoa)  # Xác định số ký tự cần có trong từng khối mã.
    if len(ban_ma) % kich_thuoc != 0:  # Bản mã phải gồm các khối đầy đủ, không được thiếu ký tự.
        raise ValueError("Độ dài bản mã phải chia hết cho độ dài khóa.")  # Không thể đảo hoán vị của một khối thiếu chữ.
    if type(so_ky_tu_dem) is not int or not 0 <= so_ky_tu_dem < kich_thuoc:  # Số đệm hợp lệ nằm từ 0 đến n-1.
        raise ValueError("Số ký tự đệm phải từ 0 đến độ dài khóa trừ 1.")  # Tránh xóa quá nhiều ký tự cuối chuỗi.
    ket_qua = []  # Lưu các khối bản rõ được khôi phục.
    for bat_dau in range(0, len(ban_ma), kich_thuoc):  # Duyệt bản mã theo cùng kích thước khối lúc mã hóa.
        khoi = ban_ma[bat_dau:bat_dau + kich_thuoc]  # Lấy một khối mã đã bị đổi thứ tự ký tự.
        khoi_goc = [""] * kich_thuoc  # Tạo n ô trống để đặt ký tự về vị trí gốc.
        for chi_so in range(kich_thuoc):  # Duyệt lần lượt các ký tự trong khối mã.
            vi_tri_goc = khoa[chi_so] - 1  # Khóa chỉ ra vị trí gốc mà ký tự mã hiện tại được lấy từ đó.
            khoi_goc[vi_tri_goc] = khoi[chi_so]  # Đưa ký tự trở lại đúng ô trước khi hoán vị.
        ket_qua.append("".join(khoi_goc))  # Ghép các ô đã phục hồi thành một khối bản rõ.
    ban_ro = "".join(ket_qua)  # Ghép các khối theo thứ tự ban đầu.
    if so_ky_tu_dem > 0:  # Chỉ cắt phần cuối khi đã khai báo có khoảng trắng đệm.
        if len(ban_ro) < so_ky_tu_dem or not ban_ro.endswith(" " * so_ky_tu_dem):  # Kiểm tra độ dài và nội dung đệm có khớp khai báo không.
            raise ValueError("Số ký tự đệm không khớp bản rõ sau giải mã.")  # Không xóa ký tự khi dữ liệu đệm không hợp lệ.
        ban_ro = ban_ro[:-so_ky_tu_dem]  # Cắt đúng phần đệm, không dùng rstrip làm mất khoảng trắng thật.
    return ban_ro  # Trả về nguyên văn chuỗi ban đầu, kể cả khoảng trắng thật ở cuối.


if __name__ == "__main__":  # Chạy minh họa khi thực thi trực tiếp file này.
    ban_ro = "HOC PYTHON!  "  # Chuỗi mẫu cố ý có hai khoảng trắng thật ở cuối.
    khoa = [3, 1, 4, 2]  # Trong mỗi khối, lấy lần lượt ký tự thứ 3, 1, 4 rồi 2.
    ban_ma, so_ky_tu_dem = ma_hoa(ban_ro, khoa)  # Nhận bản mã và số khoảng trắng thêm cho khối cuối.
    ban_giai_ma = giai_ma(ban_ma, khoa, so_ky_tu_dem)  # Đảo hoán vị rồi chỉ bỏ phần đệm do mã hóa thêm.
    print("Bản rõ:", repr(ban_ro))  # repr giúp nhìn thấy ranh giới và khoảng trắng cuối chuỗi.
    print("Khóa:", khoa)  # In thứ tự vị trí sử dụng trong từng khối.
    print("Bản mã:", repr(ban_ma))  # In bản mã có dấu nháy để quan sát các khoảng trắng.
    print("Số ký tự đệm:", so_ky_tu_dem)  # In số đệm cần lưu cùng với bản mã.
    print("Giải mã:", repr(ban_giai_ma))  # Hiển thị chuỗi được khôi phục và khoảng trắng thật ở cuối.
    assert ban_giai_ma == ban_ro  # Kiểm tra giải mã giữ chính xác cả khoảng trắng thật.
    assert ma_hoa("ABCD", khoa) == ("CADB", 0)  # Kiểm tra quy ước đọc vị trí trong khóa bằng ví dụ cụ thể.
