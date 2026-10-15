# Ôn tập mã hóa bằng Python

Hai thư mục có cùng 11 chương trình, chạy độc lập:

- `code/`: bản gọn để đọc và thực hành.
- `code_co_chu_thich/`: cùng mã nguồn, có chú thích tiếng Việt từng dòng.

Chỉ cần **Python 3.10 trở lên**, không cần cài thêm gói nào. Các chương trình
dùng hàm, vòng lặp và danh sách; không cần học class trước.

Toàn bộ thuật toán được **tự viết**, không gọi `hashlib`, thư viện mã hóa,
`math.gcd` hay `pow`. DES, AES, MD5 và SHA không dùng các toán tử dịch bit
hoặc mặt nạ bit. Các hàm có sẵn như `encode`, `decode`, `bytes` và `hex`
chỉ dùng để chuyển định dạng đầu vào/đầu ra.

Nên đọc theo thứ tự: dịch vòng → thay thế → Affine → Vigenere → hoán vị →
Hill → RSA → MD5/SHA → DES/AES. DES/AES dài hơn vì có bảng tra và nhiều vòng;
hãy đọc ví dụ cuối file, rồi hàm `ma_hoa`, sau đó mới xem các hàm xử lý bên trong.

## Chạy chương trình

Mở PowerShell tại `C:\Users\PC\Desktop\ATTT`, chạy:

```powershell
python -X utf8 .\review_gk\code\dich_vong.py
python -X utf8 .\review_gk\code_co_chu_thich\dich_vong.py
```

`-X utf8` bật UTF-8 để in tiếng Việt ổn định cả khi terminal chuyển hướng đầu ra.
Thay `dich_vong.py` bằng tên file muốn học trong bảng dưới. Mỗi file có ví dụ
ở cuối, trong khối `if __name__ == "__main__":`. Sửa văn bản và khóa ngay tại
đó, lưu file rồi chạy lại. Chương trình in kết quả để dễ đối chiếu.

## Các file

| File | Nội dung | Khóa / quy ước |
| --- | --- | --- |
| `dich_vong.py` | Mã dịch vòng (Caesar) | Số bước dịch, ví dụ `3` |
| `thay_the.py` | Thay thế đơn bảng | Hoán vị đủ 26 chữ A–Z |
| `affine.py` | Mã Affine | Hai số `a`, `b`; `gcd(a, 26) = 1` |
| `vigenere.py` | Mã Vigenere | Từ khóa A–Z, ví dụ `LEMON` |
| `hill.py` | Mã Hill 2×2 | Ma trận khả nghịch modulo 26, ví dụ `[[3, 3], [2, 5]]` |
| `hoan_vi.py` | Hoán vị theo từng khối | Danh sách vị trí bắt đầu từ 1, ví dụ `[3, 1, 4, 2]` |
| `des.py` | DES tự viết bằng mảng 0/1, đủ 16 vòng | Khóa `bytes` dài đúng 8 byte |
| `aes.py` | AES-128 tự viết bằng ma trận 4×4, đủ 10 vòng | Khóa `bytes` dài đúng 16 byte |
| `rsa.py` | RSA cơ bản, tự tính khóa | Hai số nguyên tố khác nhau `p`, `q` và số mũ `e` |
| `md5.py` | MD5 tự viết, các từ là mảng 32 phần tử | Không có khóa |
| `sha.py` | SHA-1/256/512 tự viết, các từ là mảng 32/64 phần tử | Không có khóa |

Với Caesar, thay thế, Affine và Vigenere: chỉ đổi chữ ASCII `A–Z`, `a–z`;
giữ nguyên hoa/thường, số, khoảng trắng và các ký tự khác. Vigenere chỉ tiến
vị trí khóa khi gặp một chữ ASCII. Muốn mã hóa toàn bộ câu tiếng Việt theo
các mã này, hãy tự nhập câu không dấu.

Hill chỉ nhận A–Z viết hoa (không dấu, không khoảng trắng), chia thành cặp số. Hoán vị làm việc với
các ký tự bất kỳ, kể cả khoảng trắng và tiếng Việt. DES, AES, RSA chuyển
văn bản thành byte UTF-8 nên xử lý được tiếng Việt có dấu.

## Cách đọc công thức

Quy đổi `A = 0`, `B = 1`, ..., `Z = 25`. `% 26` lấy phần dư để kết quả
luôn nằm từ 0 đến 25.

- Dịch vòng: `y = (x + k) % 26`; giải mã bằng cách trừ `k`.
- Thay thế: chữ ở vị trí `x` được đổi thành chữ ở vị trí `x` trong khóa.
- Affine: `y = (a*x + b) % 26`; giải mã là `x = a_nghich_dao*(y-b) % 26`.
- Vigenere: dịch mỗi chữ theo chữ khóa tương ứng, lặp lại khóa khi hết.
- Hill: `C = K * P (mod 26)`, với `P` là vector cột gồm hai số. Giải mã
  dùng ma trận nghịch đảo của `K` theo modulo 26.
- Hoán vị `[3, 1, 4, 2]`: khối `ABCD` thành `CADB`; các chữ được đổi vị trí.
- RSA: `n = p*q`, `phi = (p-1)*(q-1)`.
  `d = nghich_dao_modulo(e, phi)` dùng Euclid mở rộng.
  Mã hóa `c = luy_thua_modulo(m, e, n)` và giải mã
  `m = luy_thua_modulo(c, d, n)` bằng bình phương và nhân.

Nghịch đảo modulo của `a` là số nhân với `a` cho phần dư 1 khi chia cho
`m`. Nó khác phép chia số thực `1/a`. Hàm `uoc_chung_lon_nhat` tự tính
Euclid bằng cách liên tục thay `(a, b)` bằng `(b, a % b)`.

## Cách đọc mảng và ma trận

DES lưu một bit bằng một số `0` hoặc `1`. Khối là mảng 64 phần tử;
hai nửa L/R là mảng 32 phần tử; toàn bộ khóa con là ma trận 16×48.
Các bảng hoán vị đếm từ 1, còn chỉ số danh sách Python đếm từ 0:

```python
khoi = [1, 0, 1, 1]
bang = [3, 1, 4, 2]
ket_qua = []
for vi_tri in bang:
    ket_qua.append(khoi[vi_tri - 1])  # [1, 1, 1, 0]

trai = khoi[:2]                    # [1, 0]
phai = khoi[2:]                    # [1, 1]
dich_vong = khoi[1:] + khoi[:1]     # [0, 1, 1, 1]
xor = [(a + b) % 2 for a, b in zip(trai, phai)]  # [0, 1]
```

AES lưu trạng thái bằng `trang_thai[hang][cot]`: ma trận 4×4 byte.
16 byte đầu vào được xếp theo cột, ví dụ `bytes(range(16))` thành:

```text
 0   4   8  12
 1   5   9  13
 2   6  10  14
 3   7  11  15
```

SubBytes tra từng ô; ShiftRows cắt và nối từng hàng; MixColumns nhân
với ma trận hệ số trong GF(2⁸). Phép nhân GF được viết bằng nhân các
mảng hệ số đa thức rồi chia dư cho đa thức AES, không phải nhân số
nguyên rồi `% 256`. AddRoundKey tự XOR từng cặp byte.

MD5, SHA-1 và SHA-256 biểu diễn mỗi từ bằng mảng 32 phần tử; SHA-512
dùng 64 phần tử. Các hàm `cong`, `xor`, `chon`, `da_so`, `xoay_trai`,
`xoay_phai` và `dich_phai` thực hiện bằng vòng lặp, lát cắt và số học.
Hàm `cong` cộng từ cuối mảng về đầu, giữ phần nhớ như phép cộng viết tay;
phần nhớ tràn bị bỏ để giữ đúng độ dài từ. Sau đệm, mỗi khối thông điệp
được chia thành ma trận các từ, mở rộng lịch từ rồi chạy các vòng nén.

Các bản mảng ưu tiên dễ quan sát nên chậm và dùng nhiều bộ nhớ hơn bản
xử lý bằng số nguyên. Mỗi file vẫn chạy độc lập, giữ cách gọi các hàm
mã hóa, giải mã và băm như trước.

Trang [des_visualizer.html](des_visualizer.html) dùng cùng cách xử lý mảng;
mở trực tiếp bằng trình duyệt để xem từng vòng và mã Python tương ứng.
Các giá trị hex trong trang chỉ là cách hiển thị ngắn gọn của mảng bit.

## Phần đệm và dữ liệu trả về

Hill thêm `X` nếu thiếu một chữ để đủ cặp. Hoán vị thêm khoảng trắng nếu
thiếu ký tự để đủ khối. Hai hàm `ma_hoa` này trả về **hai giá trị**: bản mã
và số ký tự đệm. Truyền lại số đệm cho `giai_ma` để chỉ xóa đúng phần thêm:

```python
from hoan_vi import ma_hoa, giai_ma

khoa = [3, 1, 4, 2]
ban_ma, so_ky_tu_dem = ma_hoa("HELLO", khoa)
ban_giai_ma = giai_ma(ban_ma, khoa, so_ky_tu_dem)
print(ban_ma)
print(ban_giai_ma)
```

Ví dụ import trên dùng trong file đặt cùng thư mục với `hoan_vi.py`.
Không tự dùng `rstrip("X")` hoặc `strip()` vì sẽ làm mất chữ `X` hay
khoảng trắng thật của bản gốc.

DES và AES dùng đệm PKCS#7 để đủ khối 8 và 16 byte. Hàm `ma_hoa` trả về
chuỗi hex; `giai_ma` nhận chuỗi hex và trả lại văn bản. Hàm `ma_hoa_khoi`
và `giai_ma_khoi` nhận/trả `bytes`, xử lý đúng một khối và không thêm đệm,
phù hợp đối chiếu bài tính tay hoặc mẫu kiểm thử.

Trong Python, `b"12345678"` là byte còn `"12345678"` là chuỗi văn bản.
Độ dài khóa tính theo **byte**, không theo số chữ hiển thị; `"á"` khi
mã hóa UTF-8 chiếm nhiều hơn một byte.

RSA trong bộ này mã hóa riêng từng byte UTF-8, trả về danh sách số nguyên.
Khóa công khai là `(e, n)`, khóa bí mật là `(d, n)`. Chọn `n > 255` để mọi
giá trị byte từ 0 đến 255 đều nhỏ hơn `n`.

MD5 và SHA trả về chuỗi hex của giá trị băm. Đây là hàm băm một chiều,
không có hàm giải mã; thay đổi nhỏ ở đầu vào thường tạo kết quả băm khác hẳn.

## Kiểm tra

```powershell
python -X utf8 .\review_gk\kiem_tra.py
```

Lệnh kiểm tra cả hai bộ mã: kết quả mẫu, mã hóa rồi giải mã, trường hợp
đầu vào sai và việc hai phiên bản có cùng mã thực thi.
`hashlib` chỉ được dùng trong file kiểm tra để đối chiếu kết quả băm,
không dùng trong các file triển khai thuật toán.

Kiểm tra riêng trang HTML (cần Node.js đã có trên máy):

```powershell
python -X utf8 .\review_gk\test_des_visualizer.py
```

## Phạm vi học tập

Đây là mã phục vụ ôn tập. DES/AES ở đây dùng ECB để nhìn rõ từng khối;
RSA dùng số nguyên tố nhỏ và chưa có padding. Các ví dụ này không phù hợp
để bảo vệ dữ liệu thật. MD5 và SHA-1 chỉ được đưa vào để học, không dùng
cho yêu cầu chống va chạm hoặc tự băm mật khẩu.

Tài liệu đối chiếu: [DES FIPS 46-3](https://csrc.nist.gov/pubs/fips/46-3/final),
[AES FIPS 197](https://csrc.nist.gov/pubs/fips/197/final),
[hashlib của Python](https://docs.python.org/3/library/hashlib.html).
