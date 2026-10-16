import os
from pathlib import Path
from tempfile import TemporaryDirectory

from cau1 import giai_ma, giai_ma_vigenere, tham_ma_vigenere


def test_cau1():
    ban_ma = "tyltsrekyreytfex"
    assert giai_ma(ban_ma, 17) == "chucbanthanhcong"
    assert giai_ma_vigenere("lxfopvefrnhr", "lemon") == "attackatdawn"
    for khoa in range(26):
        assert giai_ma_vigenere(ban_ma, chr(khoa + ord("a"))) == giai_ma(ban_ma, khoa)
    for khoa in ["", "A", "a1"]:
        try:
            giai_ma_vigenere(ban_ma, khoa)
        except ValueError:
            pass
        else:
            raise AssertionError("Phải từ chối khóa không hợp lệ.")

    thu_muc_cu = Path.cwd()
    with TemporaryDirectory() as thu_muc:
        try:
            os.chdir(thu_muc)
            tham_ma_vigenere(ban_ma)
            cac_dong = Path("ket_qua_vigenere.txt").read_text().splitlines()
        finally:
            os.chdir(thu_muc_cu)
    assert len(cac_dong) == 26 + 26 ** 2 + 26 ** 3
    cac_khoa = {dong.split(" | ")[0].split(": ")[1] for dong in cac_dong}
    assert len(cac_khoa) == len(cac_dong)
    assert all(1 <= len(khoa) <= 3 for khoa in cac_khoa)
    assert {"a", "z", "aa", "zz", "aaa", "zzz"} <= cac_khoa
    for khoa in ["r", "rr", "rrr"]:
        assert f"Khóa: {khoa} | Bản rõ: chucbanthanhcong" in cac_dong


if __name__ == "__main__":
    test_cau1()
    print("Đạt: giải mã Vigenere, khóa không hợp lệ và đủ 18.278 khóa không trùng.")
