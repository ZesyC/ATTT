from math import gcd


def caesar_encrypt(text: str, key: int, alphabet: str) -> str:
    result = []
    m = len(alphabet)

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = alphabet.index(c)
        en_pos = (pos + key) % m
        en_c = alphabet[en_pos]

        if i.isupper():
            en_c = en_c.upper()

        result.append(en_c)

    return "".join(result)


def caesar_decrypt(text: str, key: int, alphabet: str) -> str:
    result = []
    m = len(alphabet)

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = alphabet.index(c)
        de_pos = (pos - key) % m
        de_c = alphabet[de_pos]

        if i.isupper():
            de_c = de_c.upper()

        result.append(de_c)

    return "".join(result)


def _validate_substitution_key(key: str, alphabet: str) -> str:
    key = key.lower().strip()
    if len(key) != len(alphabet) or set(key) != set(alphabet):
        raise ValueError(
            f"Khóa thay thế phải chứa đủ {len(alphabet)} ký tự khác nhau."
        )
    return key


def substitution_encrypt(text: str, key: str, alphabet: str) -> str:
    result = []
    key = _validate_substitution_key(key, alphabet)

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = alphabet.index(c)
        en_c = key[pos]

        if i.isupper():
            en_c = en_c.upper()

        result.append(en_c)

    return "".join(result)


def substitution_decrypt(text: str, key: str, alphabet: str) -> str:
    result = []
    key = _validate_substitution_key(key, alphabet)

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = key.index(c)
        de_c = alphabet[pos]

        if i.isupper():
            de_c = de_c.upper()

        result.append(de_c)

    return "".join(result)


def _vigenere_key_positions(key: str, alphabet: str) -> list[int]:
    key = key.lower().strip()
    if not key or any(c not in alphabet for c in key):
        raise ValueError("Từ khóa Vigenere không hợp lệ với hệ chữ cái đã chọn.")
    return [alphabet.index(c) for c in key]


def vigenere_encrypt(text: str, key: str, alphabet: str) -> str:
    result = []
    m = len(alphabet)
    key_positions = _vigenere_key_positions(key, alphabet)
    j = 0

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = alphabet.index(c)
        en_pos = (pos + key_positions[j % len(key_positions)]) % m
        en_c = alphabet[en_pos]
        j += 1

        if i.isupper():
            en_c = en_c.upper()

        result.append(en_c)

    return "".join(result)


def vigenere_decrypt(text: str, key: str, alphabet: str) -> str:
    result = []
    m = len(alphabet)
    key_positions = _vigenere_key_positions(key, alphabet)
    j = 0

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = alphabet.index(c)
        de_pos = (pos - key_positions[j % len(key_positions)]) % m
        de_c = alphabet[de_pos]
        j += 1

        if i.isupper():
            de_c = de_c.upper()

        result.append(de_c)

    return "".join(result)


def _validate_affine_key(a: int, alphabet: str) -> None:
    if gcd(a, len(alphabet)) != 1:
        raise ValueError(f"Khóa a phải nguyên tố cùng nhau với {len(alphabet)}.")


def affine_encrypt(text: str, a: int, b: int, alphabet: str) -> str:
    _validate_affine_key(a, alphabet)
    result = []
    m = len(alphabet)

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = alphabet.index(c)
        en_pos = (a * pos + b) % m
        en_c = alphabet[en_pos]

        if i.isupper():
            en_c = en_c.upper()

        result.append(en_c)

    return "".join(result)


def affine_decrypt(text: str, a: int, b: int, alphabet: str) -> str:
    _validate_affine_key(a, alphabet)
    result = []
    m = len(alphabet)
    a_inverse = pow(a, -1, m)

    for i in text:
        c = i.lower()
        if c not in alphabet:
            result.append(i)
            continue

        pos = alphabet.index(c)
        de_pos = (a_inverse * (pos - b)) % m
        de_c = alphabet[de_pos]

        if i.isupper():
            de_c = de_c.upper()

        result.append(de_c)

    return "".join(result)


def _determinant(matrix: list[list[int]]) -> int:
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    result = 0
    for column, value in enumerate(matrix[0]):
        minor = [row[:column] + row[column + 1 :] for row in matrix[1:]]
        result += (-1) ** column * value * _determinant(minor)
    return result


def _validate_hill_matrix(matrix: list[list[int]], modulus: int) -> int:
    size = len(matrix)
    if size not in (2, 3) or any(len(row) != size for row in matrix):
        raise ValueError("Ma trận Hill phải có kích thước 2x2 hoặc 3x3.")

    determinant = _determinant(matrix)
    if gcd(determinant, modulus) != 1:
        raise ValueError(f"Ma trận Hill không khả nghịch trên Z{modulus}.")
    return size


def _inverse_matrix_mod(matrix: list[list[int]], modulus: int) -> list[list[int]]:
    size = _validate_hill_matrix(matrix, modulus)
    determinant_inverse = pow(_determinant(matrix) % modulus, -1, modulus)
    inverse = []

    for row in range(size):
        inverse_row = []
        for column in range(size):
            minor = [
                values[:row] + values[row + 1 :]
                for index, values in enumerate(matrix)
                if index != column
            ]
            cofactor = (-1) ** (row + column) * _determinant(minor)
            inverse_row.append((determinant_inverse * cofactor) % modulus)
        inverse.append(inverse_row)

    return inverse


def _hill_transform(
    text: str,
    matrix: list[list[int]],
    alphabet: str,
    remove_padding: bool = False,
) -> str:
    modulus = len(alphabet)
    size = _validate_hill_matrix(matrix, modulus)
    letters = [i for i in text if i.lower() in alphabet]
    padding_count = (-len(letters)) % size
    letters.extend("x" for _ in range(padding_count))
    transformed_letters = []

    for start in range(0, len(letters), size):
        block = [alphabet.index(i.lower()) for i in letters[start : start + size]]

        for row in matrix:
            position = sum(row[column] * block[column] for column in range(size))
            transformed = alphabet[position % modulus]
            source_index = start + len(transformed_letters) % size

            if source_index < len(letters) - padding_count and letters[source_index].isupper():
                transformed = transformed.upper()

            transformed_letters.append(transformed)

    result = []
    letter_index = 0
    for i in text:
        if i.lower() in alphabet:
            result.append(transformed_letters[letter_index])
            letter_index += 1
        else:
            result.append(i)

    result.extend(transformed_letters[letter_index:])
    output = "".join(result)

    if remove_padding:
        for _ in range(size - 1):
            if output.endswith(("x", "X")):
                output = output[:-1]
            else:
                break

    return output


def hill_encrypt(text: str, matrix: list[list[int]], alphabet: str) -> str:
    return _hill_transform(text, matrix, alphabet)


def hill_decrypt(text: str, matrix: list[list[int]], alphabet: str) -> str:
    inverse_matrix = _inverse_matrix_mod(matrix, len(alphabet))
    return _hill_transform(text, inverse_matrix, alphabet, remove_padding=True)


_DES_IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
]

_DES_IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25,
]

_DES_PC1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4,
]

_DES_PC2 = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]

_DES_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

_DES_E = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1,
]

_DES_P = [
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25,
]

_DES_S = [
    [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],
    ],
    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],
    ],
    [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12],
    ],
    [
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],
    ],
    [
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
        [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
        [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
        [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],
    ],
    [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
        [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
        [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
        [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],
    ],
    [
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
        [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
        [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],
    ],
    [
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
        [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
        [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11],
    ],
]


def _des_permute(block: int, table: list[int], block_size: int) -> int:
    result = 0
    for bit_pos in table:
        result = (result << 1) | ((block >> (block_size - bit_pos)) & 1)
    return result


def _des_generate_subkeys(key_bytes: bytes) -> list[int]:
    key_int = int.from_bytes(key_bytes, "big")
    key56 = _des_permute(key_int, _DES_PC1, 64)

    c = key56 >> 28
    d = key56 & 0x0FFF_FFFF

    subkeys = []
    for shift in _DES_SHIFTS:
        c = ((c << shift) | (c >> (28 - shift))) & 0x0FFF_FFFF
        d = ((d << shift) | (d >> (28 - shift))) & 0x0FFF_FFFF
        cd = (c << 28) | d
        subkeys.append(_des_permute(cd, _DES_PC2, 56))

    return subkeys


def _des_f(right: int, subkey: int) -> int:
    expanded = _des_permute(right, _DES_E, 32)
    xored = expanded ^ subkey

    sbox_output = 0
    for i in range(8):
        chunk = (xored >> (42 - 6 * i)) & 0x3F
        row = ((chunk & 0x20) >> 4) | (chunk & 1)
        col = (chunk >> 1) & 0x0F
        sbox_output = (sbox_output << 4) | _DES_S[i][row][col]

    return _des_permute(sbox_output, _DES_P, 32)


def _des_encrypt_block(block_bytes: bytes, subkeys: list[int]) -> bytes:
    block = int.from_bytes(block_bytes, "big")
    permuted = _des_permute(block, _DES_IP, 64)
    left = permuted >> 32
    right = permuted & 0xFFFF_FFFF

    for subkey in subkeys:
        left, right = right, left ^ _des_f(right, subkey)

    combined = (right << 32) | left
    result = _des_permute(combined, _DES_IP_INV, 64)
    return result.to_bytes(8, "big")


def _des_decrypt_block(block_bytes: bytes, subkeys: list[int]) -> bytes:
    return _des_encrypt_block(block_bytes, list(reversed(subkeys)))


def _pkcs7_pad(data: bytes, block_size: int = 8) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def _pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("Dữ liệu rỗng, không thể bỏ padding.")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Padding không hợp lệ (PKCS#7).")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Padding không hợp lệ (PKCS#7).")
    return data[:-pad_len]


def _is_pure_hex(s: str) -> bool:
    return len(s) > 0 and all(c in "0123456789abcdefABCDEF" for c in s)


def _des_parse_key(key: str) -> bytes:
    key = key.strip()
    hex_part = key[2:] if key.lower().startswith("0x") else key
    if _is_pure_hex(hex_part) and len(hex_part) == 16:
        try:
            return bytes.fromhex(hex_part)
        except ValueError as error:
            raise ValueError("Khóa DES hex không hợp lệ.") from error
    key_bytes = key.encode("ascii", errors="replace")
    if len(key_bytes) != 8:
        raise ValueError("Khóa DES phải có đúng 8 ký tự ASCII, hoặc hex 16 ký tự (8 bytes).")
    return key_bytes


def des_encrypt(plaintext: str, key: str) -> str:
    key_bytes = _des_parse_key(key)
    subkeys = _des_generate_subkeys(key_bytes)

    plaintext = plaintext.strip()
    hex_part = plaintext[2:] if plaintext.lower().startswith("0x") else plaintext
    if _is_pure_hex(hex_part) and len(hex_part) == 16:
        try:
            data = bytes.fromhex(hex_part)
        except ValueError as error:
            raise ValueError("Plaintext hex không hợp lệ.") from error
        return _des_encrypt_block(data, subkeys).hex().upper()

    data = _pkcs7_pad(plaintext.encode("utf-8"))
    ciphertext = b""
    for i in range(0, len(data), 8):
        ciphertext += _des_encrypt_block(data[i:i + 8], subkeys)
    return ciphertext.hex().upper()


def des_decrypt(ciphertext_hex: str, key: str) -> str:
    key_bytes = _des_parse_key(key)
    subkeys = _des_generate_subkeys(key_bytes)

    ciphertext_hex = ciphertext_hex.strip().replace(" ", "")
    try:
        data = bytes.fromhex(ciphertext_hex)
    except ValueError as error:
        raise ValueError("Bản mã DES phải là chuỗi hex hợp lệ.") from error

    if len(data) % 8 != 0:
        raise ValueError("Độ dài bản mã DES phải là bội số của 8 bytes.")

    plaintext_bytes = b""
    for i in range(0, len(data), 8):
        plaintext_bytes += _des_decrypt_block(data[i:i + 8], subkeys)

    try:
        unpadded = _pkcs7_unpad(plaintext_bytes)
        return unpadded.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return "0x" + plaintext_bytes.hex().upper()


def _self_check() -> None:
    z26 = "abcdefghijklmnopqrstuvwxyz"
    z29 = "aăâbcdđeêghiklmnoôơpqrstuưvxy"
    substitution_key = z26[::-1]
    hill_key = [[3, 3], [2, 5]]

    assert caesar_decrypt(caesar_encrypt("Hello, World!", 3, z26), 3, z26) == "Hello, World!"
    assert caesar_decrypt(caesar_encrypt("Ăn Cơm!", 7, z29), 7, z29) == "Ăn Cơm!"
    assert substitution_decrypt(substitution_encrypt("Bao mat!", substitution_key, z26), substitution_key, z26) == "Bao mat!"
    assert vigenere_decrypt(vigenere_encrypt("Attack at dawn!", "lemon", z26), "lemon", z26) == "Attack at dawn!"
    assert affine_decrypt(affine_encrypt("Affine Cipher!", 5, 8, z26), 5, 8, z26) == "Affine Cipher!"
    assert hill_decrypt(hill_encrypt("Hello!", hill_key, z26), hill_key, z26) == "Hello!"
    des_key = "ATTT2024"
    assert des_decrypt(des_encrypt("Hello, DES!", des_key), des_key) == "Hello, DES!"
    assert des_decrypt(des_encrypt("", des_key), des_key) == ""
    assert des_decrypt(des_encrypt("Test 123 !@#", des_key), des_key) == "Test 123 !@#"
    assert des_encrypt("123456ABCD132536", "AABB09182736CCDD") == "C0B7A8D05F3A829C"
    assert des_encrypt("0x123456ABCD132536", "0xAABB09182736CCDD") == "C0B7A8D05F3A829C"


if __name__ == "__main__":
    _self_check()
    print("Tất cả kiểm tra thuật toán đều đạt.")
