"""Kiểm tra hai bộ thuật toán. Chạy: python -X utf8 review_gk/kiem_tra.py.

hashlib chỉ là kết quả đối chiếu trong kiểm thử, không tham gia triển khai.
Không cần cài thêm thư viện.
"""

import ast
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
from pathlib import Path
import random
import runpy
import sys


ROOT = Path(__file__).resolve().parent


def nap_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def phai_bao_loi(ham, *args):
    try:
        ham(*args)
    except ValueError:
        return
    raise AssertionError(f"{ham.__name__} không từ chối đầu vào sai: {args!r}")


def kiem_tra_cau_truc():
    ten_file = sorted(path.name for path in (ROOT / "code").glob("*.py"))
    assert len(ten_file) == 11
    toan_tu_bit = (ast.LShift, ast.RShift, ast.BitAnd, ast.BitOr, ast.BitXor, ast.Invert)
    for ten in ten_file:
        gon = ast.parse((ROOT / "code" / ten).read_text(encoding="utf-8"))
        chu_thich = ast.parse((ROOT / "code_co_chu_thich" / ten).read_text(encoding="utf-8"))
        assert ast.dump(gon) == ast.dump(chu_thich), f"Hai bản {ten} khác mã thực thi."
        for node in ast.walk(gon):
            assert not isinstance(node, toan_tu_bit), f"Còn toán tử bit trong {ten}."
            assert not isinstance(node, (ast.Import, ast.ImportFrom)), f"Còn import trong {ten}."
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != "pow", f"Còn gọi pow trong {ten}."
    return ten_file


def kiem_tra_ma_khoi(module, kich_thuoc, vectors, rng):
    for khoa_hex, ro_hex, ma_hex in vectors:
        khoa, ro, ma = map(bytes.fromhex, (khoa_hex, ro_hex, ma_hex))
        assert module.ma_hoa_khoi(ro, khoa) == ma
        assert module.giai_ma_khoi(ma, khoa) == ro
    khoa = bytes(range(kich_thuoc))
    for _ in range(8):
        ro = rng.randbytes(kich_thuoc)
        assert module.giai_ma_khoi(module.ma_hoa_khoi(ro, khoa), khoa) == ro
    for ro in ("", "a", "A" * (kich_thuoc - 1), "A" * kich_thuoc,
               "A" * (kich_thuoc + 1), "Xin chào, Việt Nam!", "\ufeffabc\0"):
        ma = module.ma_hoa(ro, khoa)
        assert module.giai_ma(ma, khoa) == ro
        assert len(ma) % (kich_thuoc * 2) == 0
    phai_bao_loi(module.ma_hoa_khoi, bytes(kich_thuoc - 1), khoa)
    phai_bao_loi(module.ma_hoa_khoi, bytes(kich_thuoc), bytes(kich_thuoc + 1))
    phai_bao_loi(module.ma_hoa_khoi, bytes(kich_thuoc), "A" * kich_thuoc)
    for ban_ma in ("", "00", "GG" * kich_thuoc):
        phai_bao_loi(module.giai_ma, ban_ma, khoa)
    # Bản rõ toàn 0 có byte cuối 0, không phải đệm PKCS#7 hợp lệ.
    ma_sai_dem = module.ma_hoa_khoi(bytes(kich_thuoc), khoa).hex()
    phai_bao_loi(module.giai_ma, ma_sai_dem, khoa)
    # Byte cuối cho số đệm hợp lệ, nhưng các byte còn lại không giống nhau.
    ro_sai_dem = bytes(kich_thuoc - 2) + bytes([3, 2])
    phai_bao_loi(module.giai_ma, module.ma_hoa_khoi(ro_sai_dem, khoa).hex(), khoa)


def main():
    sys.dont_write_bytecode = True
    ten_file = kiem_tra_cau_truc()
    rng = random.Random(20261015)
    vectors_des = [
        ("133457799BBCDFF1", "0123456789ABCDEF", "85E813540F0AB405"),
        ("0000000000000000", "0000000000000000", "8CA64DE9C1B123A7"),
    ]
    vectors_aes = [
        ("000102030405060708090A0B0C0D0E0F", "00112233445566778899AABBCCDDEEFF", "69C4E0D86A7B0430D8CDB78070B4C55A"),
        ("00000000000000000000000000000000", "00000000000000000000000000000000", "66E94BD4EF8A2C3B884CFA59CA342B2E"),
        ("2B7E151628AED2A6ABF7158809CF4F3C", "6BC1BEE22E409F96E93D7E117393172A", "3AD77BB40D7A3660A89ECAF32466EF97"),
    ]
    do_dai_dem = (0, 1, 55, 56, 63, 64, 65, 111, 112, 127, 128, 129, 255)
    van_ban_bam = ["a" * n for n in do_dai_dem] + ["abc", "Xin chào Việt Nam!", "\ufeffabc\0", "🙂"]
    for thu_muc in ("code", "code_co_chu_thich"):
        modules = {Path(ten).stem: nap_module(ROOT / thu_muc / ten) for ten in ten_file}
        des, aes, rsa = modules["des"], modules["aes"], modules["rsa"]
        kiem_tra_ma_khoi(des, 8, vectors_des, rng)
        kiem_tra_ma_khoi(aes, 16, vectors_aes, rng)
        khoa_des = des._tao_khoa_con(bytes(8))
        assert len(khoa_des) == 16 and all(len(hang) == 48 for hang in khoa_des)
        assert des._hoan_vi([1, 0, 1, 1], [3, 1, 4, 2]) == [1, 1, 1, 0]
        assert des._xor([1, 0, 1, 1], [1, 1, 0, 1]) == [0, 1, 1, 0]
        assert aes._tao_ma_tran(bytes(range(16))) == [
            [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],
        ]
        assert aes._nhan_gf(0x57, 0x13) == 0xFE
        bam = ((modules["md5"].bam_md5, "md5"), (modules["sha"].bam_sha1, "sha1"),
               (modules["sha"].bam_sha256, "sha256"), (modules["sha"].bam_sha512, "sha512"))
        for ham, ten in bam:
            for text in van_ban_bam:
                expected = hashlib.new(ten, text.encode("utf-8"), usedforsecurity=False).hexdigest()
                assert ham(text) == expected, (thu_muc, ten, len(text.encode("utf-8")))
            phai_bao_loi(ham, b"abc")
            phai_bao_loi(ham, None)
        cong_khai, bi_mat = rsa.tao_khoa(61, 53, 17)
        assert cong_khai == (17, 3233) and bi_mat == (2753, 3233)
        assert rsa.luy_thua_modulo(65, 17, 3233) == 2790
        assert rsa.luy_thua_modulo(2790, 2753, 3233) == 65
        for byte in range(256):
            so = rsa.luy_thua_modulo(byte, cong_khai[0], cong_khai[1])
            assert rsa.luy_thua_modulo(so, bi_mat[0], bi_mat[1]) == byte
        assert rsa.giai_ma(rsa.ma_hoa("Xin chào RSA!", cong_khai), bi_mat) == "Xin chào RSA!"
        phai_bao_loi(rsa.tao_khoa, 61, 61)
        phai_bao_loi(rsa.tao_khoa, 15, 53)
        phai_bao_loi(rsa.tao_khoa, 61, 53, 12)
        phai_bao_loi(rsa.giai_ma, [-1], bi_mat)
        phai_bao_loi(rsa.giai_ma, [3233], bi_mat)
        # Mỗi demo chứa các kiểm tra mẫu của cả sáu mã cổ điển và năm file còn lại.
        for ten in ten_file:
            with redirect_stdout(io.StringIO()):
                runpy.run_path(str(ROOT / thu_muc / ten), run_name="__main__")
        print(f"PASS {thu_muc}: 11 demos; DES/AES vectors, padding and round-trips; "
              f"4 hashes x {len(van_ban_bam)} cases; RSA 256 bytes.")
    print("PASS: both versions have identical executable AST; no bitwise operators, imports or pow in algorithms.")


if __name__ == "__main__":
    main()
