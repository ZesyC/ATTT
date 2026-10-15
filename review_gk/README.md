# Ôn tập mã hóa bằng Python

Hai thư mục có cùng 11 chương trình, chạy độc lập:

- `code/`: bản gọn để đọc và thực hành.
- `code_co_chu_thich/`: cùng mã nguồn, có chú thích tiếng Việt từng dòng.

Chỉ cần **Python 3.10 trở lên**, không cần cài thêm gói nào. Các chương trình
dùng hàm, vòng lặp và danh sách; không cần học class trước.

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
| `des.py` | DES, đủ 16 vòng | Khóa `bytes` dài đúng 8 byte |
| `aes.py` | AES-128, đủ 10 vòng | Khóa `bytes` dài đúng 16 byte |
| `rsa.py` | RSA cơ bản, tự tính khóa | Hai số nguyên tố khác nhau `p`, `q` và số mũ `e` |
| `md5.py` | Băm MD5 bằng `hashlib` | Không có khóa |
| `sha.py` | Băm SHA-1, SHA-256, SHA-512 bằng `hashlib` | Không có khóa |

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
- RSA: `n = p*q`, `phi = (p-1)*(q-1)`, `d = pow(e, -1, phi)`.
  Mã hóa `c = pow(m, e, n)`, giải mã `m = pow(c, d, n)`.

`pow(a, -1, m)` tính nghịch đảo modulo: số nhân với `a` cho phần dư 1
khi chia cho `m`. Nó khác phép chia số thực `1/a`.

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

## Phạm vi học tập

Đây là mã phục vụ ôn tập. DES/AES ở đây dùng ECB để nhìn rõ từng khối;
RSA dùng số nguyên tố nhỏ và chưa có padding. Các ví dụ này không phù hợp
để bảo vệ dữ liệu thật. MD5 và SHA-1 chỉ được đưa vào để học, không dùng
cho yêu cầu chống va chạm hoặc tự băm mật khẩu.

Tài liệu đối chiếu: [DES FIPS 46-3](https://csrc.nist.gov/pubs/fips/46-3/final),
[AES FIPS 197](https://csrc.nist.gov/pubs/fips/197/final),
[hashlib của Python](https://docs.python.org/3/library/hashlib.html).
