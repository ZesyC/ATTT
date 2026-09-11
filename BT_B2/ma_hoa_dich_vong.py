ad = {char: i for i, char in enumerate("abcdefghijklmnopqrstuvwxyz")}
ad_reverse = {i: char for char, i in ad.items()}
ad_upper = {char: i for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
ad_upper_reverse = {i: char for char, i in ad_upper.items()}

def encode(text, k):
    a = []
    for c in text:
        if 'a' <= c <= 'z':
            a.append(ad_reverse[(ad[c] + k) % 26])
        elif 'A' <= c <= 'Z':
            a.append(ad_upper_reverse[(ad_upper[c] + k) % 26])
        else:
            a.append(c)
    result = ''.join(a)
    return result

def decode(text, k):
    a = []
    for c in text:
        if 'a' <= c <= 'z':
            a.append(ad_reverse[(ad[c] - k) % 26])
        elif 'A' <= c <= 'Z':
            a.append(ad_upper_reverse[(ad_upper[c] - k) % 26])
        else:
            a.append(c)
    start = ''.join(a)
    return start

def main():
    text = input("Nhập văn bản cần mã hóa: ")
    while True:
        try:
            k = int(input("Nhập key (0 <= k <= 25): "))
            if 0 <= k <= 25:
                break
            print("Key phải nằm trong khoảng từ 0 đến 25.")
        except ValueError:
            print("Key phải là một số nguyên.")
    enc = encode(text, k)
    print(f"Chuỗi sau mã hóa: {enc}")
    dec = decode(enc, k)
    print(f"Chuỗi ban đầu: {dec}")

main()