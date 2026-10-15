# Hill 2x2: chỉ chấp nhận chữ A-Z viết hoa, không nhận khoảng trắng, chữ thường hay chữ có dấu.
# Mỗi cặp chữ là một vector cột; mã hóa bằng phép nhân ma trận khóa modulo 26.
# Lưu so_ky_tu_dem cùng bản mã để bỏ đúng chữ X được thêm, không làm mất chữ X thật.
CHU_CAI = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Bảng chữ dùng để quy đổi A = 0, B = 1, ..., Z = 25.


def ma_tran_nghich_dao(khoa):  # Kiểm tra khóa 2x2 và tính ma trận đảo modulo 26.
    if not isinstance(khoa, (list, tuple)) or len(khoa) != 2:  # Ma trận cần có đúng hai hàng.
        raise ValueError("Khóa Hill phải là ma trận 2x2.")  # Từ chối khóa có cấu trúc không đúng.
    for hang in khoa:  # Kiểm tra lần lượt hai hàng của ma trận.
        if not isinstance(hang, (list, tuple)) or len(hang) != 2:  # Mỗi hàng phải chứa đúng hai phần tử.
            raise ValueError("Mỗi hàng của khóa Hill phải có 2 số nguyên.")  # Báo lỗi nếu hàng không đủ hoặc thừa phần tử.
        for so in hang:  # Duyệt từng phần tử trong hàng hiện tại.
            if type(so) is not int:  # Phép nhân ma trận này chỉ dùng số nguyên.
                raise ValueError("Các phần tử khóa Hill phải là số nguyên.")  # Từ chối số thực, chuỗi và giá trị bool.
    a, b = khoa[0]  # Lấy hai phần tử ở hàng đầu của ma trận khóa.
    c, d = khoa[1]  # Lấy hai phần tử ở hàng thứ hai của ma trận khóa.
    dinh_thuc = (a * d - b * c) % 26  # Tính định thức ad-bc theo modulo 26.
    for so in range(1, 26):  # Thử tìm nghịch đảo nhân của định thức trong các số 1 đến 25.
        if (dinh_thuc * so) % 26 == 1:  # Ma trận đảo tồn tại khi tìm được tích có phần dư bằng 1.
            return [[d * so % 26, -b * so % 26], [-c * so % 26, a * so % 26]]  # Nhân ma trận phụ hợp [[d,-b],[-c,a]] với nghịch đảo định thức.
    raise ValueError("Định thức khóa Hill phải nguyên tố cùng nhau với 26.")  # Ma trận không khả nghịch sẽ không giải mã duy nhất được.


def kiem_tra_van_ban(van_ban):  # Giới hạn đầu vào rõ ràng để ví dụ Hill tập trung vào toán ma trận.
    for ky_tu in van_ban:  # Kiểm tra từng ký tự trước khi chuyển chữ thành số.
        if ky_tu not in CHU_CAI:  # Chỉ chữ hoa A-Z mới có giá trị trong bảng mã.
            raise ValueError("Hill chỉ nhận A-Z viết hoa, không có khoảng trắng hay dấu.")  # Yêu cầu người dùng chuẩn bị chuỗi đúng định dạng.


def bien_doi_cap(van_ban, ma_tran):  # Nhân từng cặp ký tự với ma trận được cung cấp.
    ket_qua = []  # Lưu các chữ sau phép nhân ma trận.
    for vi_tri in range(0, len(van_ban), 2):  # Bắt đầu tại 0, 2, 4, ... để chia chuỗi thành từng cặp.
        x = CHU_CAI.index(van_ban[vi_tri])  # Lấy số tương ứng với chữ thứ nhất trong cặp.
        y = CHU_CAI.index(van_ban[vi_tri + 1])  # Lấy số tương ứng với chữ thứ hai trong cặp.
        so_dau = (ma_tran[0][0] * x + ma_tran[0][1] * y) % 26  # Hàng đầu nhân vector cột [x,y] tạo chữ đầu.
        so_sau = (ma_tran[1][0] * x + ma_tran[1][1] * y) % 26  # Hàng thứ hai nhân vector cột [x,y] tạo chữ sau.
        ket_qua.append(CHU_CAI[so_dau])  # Chuyển kết quả đầu từ số về chữ.
        ket_qua.append(CHU_CAI[so_sau])  # Chuyển kết quả sau từ số về chữ.
    return "".join(ket_qua)  # Nối các cặp đã biến đổi thành chuỗi kết quả.


def ma_hoa(van_ban, khoa):  # Nhận bản rõ A-Z và ma trận khóa 2x2.
    ma_tran_nghich_dao(khoa)  # Kiểm tra khóa khả nghịch trước khi tạo bản mã.
    kiem_tra_van_ban(van_ban)  # Từ chối ký tự ngoài A-Z thay vì âm thầm xóa hoặc đổi chữ.
    so_ky_tu_dem = len(van_ban) % 2  # Cần thêm một chữ X nếu số lượng chữ ban đầu là lẻ.
    van_ban = van_ban + "X" * so_ky_tu_dem  # Đệm X để luôn có đủ hai chữ trong mỗi cặp.
    ban_ma = bien_doi_cap(van_ban, khoa)  # Nhân từng cặp bản rõ với ma trận khóa modulo 26.
    return ban_ma, so_ky_tu_dem  # Trả cả bản mã lẫn số chữ đệm để giải mã khôi phục chính xác.


def giai_ma(ban_ma, khoa, so_ky_tu_dem=0):  # Số chữ đệm mặc định bằng 0 nếu bản rõ không cần đệm.
    khoa_dao = ma_tran_nghich_dao(khoa)  # Tính ma trận khóa đảo để hoàn tác phép nhân khi mã hóa.
    kiem_tra_van_ban(ban_ma)  # Bản mã cũng chỉ được chứa chữ hoa A-Z.
    if len(ban_ma) % 2 != 0:  # Mỗi khối Hill 2x2 phải có đúng hai chữ.
        raise ValueError("Độ dài bản mã Hill phải là số chẵn.")  # Không thể giải mã một cặp bị thiếu chữ.
    if type(so_ky_tu_dem) is not int or so_ky_tu_dem not in (0, 1):  # Hill 2x2 chỉ thêm 0 hoặc 1 chữ X.
        raise ValueError("Số ký tự đệm Hill phải bằng 0 hoặc 1.")  # Ngăn việc xóa sai số lượng chữ cuối.
    ban_ro = bien_doi_cap(ban_ma, khoa_dao)  # Nhân bản mã với ma trận đảo để thu được bản rõ còn đệm.
    if so_ky_tu_dem == 1:  # Chỉ bỏ chữ cuối khi người gọi xác nhận có một chữ đệm.
        if not ban_ro.endswith("X"):  # Chuỗi rỗng hoặc chuỗi không kết thúc bằng X không phù hợp số đệm.
            raise ValueError("Số ký tự đệm không khớp bản rõ sau giải mã.")  # Báo sai dữ liệu thay vì xóa mất một chữ thật.
        ban_ro = ban_ro[:-1]  # Bỏ đúng một chữ X thêm vào lúc mã hóa.
    return ban_ro  # Giữ nguyên mọi chữ X thật vốn có trong bản rõ.


if __name__ == "__main__":  # Chỉ chạy ví dụ khi file được thực thi trực tiếp.
    ban_ro = "HELLO"  # Chuỗi có 5 chữ nên cần thêm một chữ X khi mã hóa.
    khoa = [[3, 3], [2, 5]]  # Ma trận có định thức bằng 9 và có nghịch đảo modulo 26.
    ban_ma, so_ky_tu_dem = ma_hoa(ban_ro, khoa)  # Nhận bản mã và lưu thông tin về chữ đệm.
    ban_giai_ma = giai_ma(ban_ma, khoa, so_ky_tu_dem)  # Truyền cả số đệm để khôi phục đúng 5 chữ ban đầu.
    print("Bản rõ:", ban_ro)  # In chuỗi trước khi thêm chữ đệm.
    print("Khóa:", khoa)  # In ma trận khóa 2x2.
    print("Bản mã:", ban_ma)  # In chuỗi được mã hóa theo từng cặp.
    print("Số ký tự đệm:", so_ky_tu_dem)  # In thông tin cần giữ cùng bản mã.
    print("Giải mã:", ban_giai_ma)  # In kết quả giải mã sau khi bỏ đúng phần đệm.
    assert ban_giai_ma == ban_ro  # Kiểm tra bản rõ có độ dài lẻ được khôi phục chính xác.
    assert ma_hoa("HELP", khoa) == ("HIAT", 0)  # Kiểm tra phép nhân ma trận theo quy ước vector cột.
    ban_ma_x, so_dem_x = ma_hoa("BOX", khoa)  # Thử bản rõ có một chữ X thật ở cuối và một X đệm.
    assert giai_ma(ban_ma_x, khoa, so_dem_x) == "BOX"  # Chắc chắn chỉ xóa chữ X đệm và giữ chữ X thật.
