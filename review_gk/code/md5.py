"""MD5 là hàm băm một chiều; không có thao tác giải mã, không dùng cho bảo mật mới."""

import hashlib


def bam_md5(van_ban: str) -> str:
    if not isinstance(van_ban, str):
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")
    du_lieu = van_ban.encode("utf-8")
    ket_qua = hashlib.md5(du_lieu, usedforsecurity=False)
    return ket_qua.hexdigest()


if __name__ == "__main__":
    van_ban = "Xin chào Python!"
    assert bam_md5("abc") == "900150983cd24fb0d6963f7d28e17f72"
    print("Văn bản:", van_ban)
    print("MD5 (128 bit, 32 ký tự hex):", bam_md5(van_ban))
    print("Băm là một chiều: không có hàm giải mã.")
