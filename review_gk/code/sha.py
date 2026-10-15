"""SHA là họ hàm băm một chiều; SHA-1 chỉ dùng để học, ưu tiên SHA-256 hoặc SHA-512."""

import hashlib


def bam_sha1(van_ban: str) -> str:
    if not isinstance(van_ban, str):
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")
    du_lieu = van_ban.encode("utf-8")
    return hashlib.sha1(du_lieu, usedforsecurity=False).hexdigest()


def bam_sha256(van_ban: str) -> str:
    if not isinstance(van_ban, str):
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")
    du_lieu = van_ban.encode("utf-8")
    return hashlib.sha256(du_lieu).hexdigest()


def bam_sha512(van_ban: str) -> str:
    if not isinstance(van_ban, str):
        raise ValueError("Dữ liệu cần băm phải là chuỗi.")
    du_lieu = van_ban.encode("utf-8")
    return hashlib.sha512(du_lieu).hexdigest()


if __name__ == "__main__":
    van_ban = "Xin chào Python!"
    assert bam_sha256("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    print("Văn bản:", van_ban)
    print("SHA-1 (160 bit, 40 ký tự hex):", bam_sha1(van_ban))
    print("SHA-256 (256 bit, 64 ký tự hex):", bam_sha256(van_ban))
    print("SHA-512 (512 bit, 128 ký tự hex):", bam_sha512(van_ban))
    print("Băm là một chiều: không có hàm giải mã.")
