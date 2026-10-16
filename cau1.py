def giai_ma(ban_ma, khoa):
    ban_ro = ""
    for chu in ban_ma:
        vi_tri = ord(chu) - ord("a")
        vi_tri_moi = (vi_tri - khoa) % 26
        ban_ro += chr(vi_tri_moi + ord("a"))
    return ban_ro


def giai_ma_vigenere(ban_ma, khoa):
    if not khoa or any(chu < "a" or chu > "z" for chu in khoa):
        raise ValueError("Khóa Vigenere phải gồm các chữ thường a-z.")
    ban_ro = ""
    for i in range(len(ban_ma)):
        vi_tri = ord(ban_ma[i]) - ord("a")
        do_dich = ord(khoa[i % len(khoa)]) - ord("a")
        vi_tri_moi = (vi_tri - do_dich) % 26
        ban_ro += chr(vi_tri_moi + ord("a"))
    return ban_ro


def tham_ma_vigenere(ban_ma):
    with open("ket_qua_vigenere.txt", "w", encoding="utf-8") as tep:
        for do_dai in range(1, 4):
            for so in range(26 ** do_dai):
                khoa = ""
                for i in range(do_dai):
                    khoa = chr(so % 26 + ord("a")) + khoa
                    so //= 26
                ban_ro = giai_ma_vigenere(ban_ma, khoa)
                tep.write(f"Khóa: {khoa} | Bản rõ: {ban_ro}\n")


if __name__ == "__main__":
    ban_ma = "tyltsrekyreytfex"
    print("Thử 26 khóa dịch vòng:")
    for khoa in range(26):
        ban_ro = giai_ma(ban_ma, khoa)
        print(f"Khóa: {khoa:2} | Bản rõ: {ban_ro}")
    tham_ma_vigenere(ban_ma)
    print("Đã thử mọi khóa Vigenere dài 1 đến 3 chữ.")
    print("Xem các bản rõ ứng viên trong ket_qua_vigenere.txt.")
