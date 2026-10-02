from math import gcd


def _left_rotate(value: int, amount: int, bits: int = 32) -> int:
    value &= (1 << bits) - 1
    return ((value << amount) | (value >> (bits - amount))) & ((1 << bits) - 1)


_MD5_SHIFT = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
_MD5_K = [
    0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE, 0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
    0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE, 0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
    0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA, 0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED, 0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
    0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C, 0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
    0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05, 0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
    0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039, 0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
    0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1, 0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391,
]


def md5_text(text: str) -> str:
    data = bytearray(text.encode("utf-8"))
    bit_length = len(data) * 8
    data.append(0x80)
    data.extend(b"\x00" * ((56 - len(data) % 64) % 64))
    data.extend(bit_length.to_bytes(8, "little"))
    a, b, c, d = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
    for offset in range(0, len(data), 64):
        words = [int.from_bytes(data[offset + i:offset + i + 4], "little") for i in range(0, 64, 4)]
        aa, bb, cc, dd = a, b, c, d
        for index in range(64):
            if index < 16:
                function, word_index = (b & c) | (~b & d), index
            elif index < 32:
                function, word_index = (d & b) | (~d & c), (5 * index + 1) % 16
            elif index < 48:
                function, word_index = b ^ c ^ d, (3 * index + 5) % 16
            else:
                function, word_index = c ^ (b | ~d), (7 * index) % 16
            value = (a + function + _MD5_K[index] + words[word_index]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + _left_rotate(value, _MD5_SHIFT[index])) & 0xFFFFFFFF
        a, b, c, d = (a + aa) & 0xFFFFFFFF, (b + bb) & 0xFFFFFFFF, (c + cc) & 0xFFFFFFFF, (d + dd) & 0xFFFFFFFF
    return b"".join(value.to_bytes(4, "little") for value in (a, b, c, d)).hex().upper()


_SHA256_K = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]


def sha256_text(text: str) -> str:
    data = bytearray(text.encode("utf-8"))
    bit_length = len(data) * 8
    data.append(0x80)
    data.extend(b"\x00" * ((56 - len(data) % 64) % 64))
    data.extend(bit_length.to_bytes(8, "big"))
    state = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
    for offset in range(0, len(data), 64):
        words = [int.from_bytes(data[offset + i:offset + i + 4], "big") for i in range(0, 64, 4)]
        for index in range(16, 64):
            first = _left_rotate(words[index - 15], 25) ^ _left_rotate(words[index - 15], 14) ^ (words[index - 15] >> 3)
            second = _left_rotate(words[index - 2], 15) ^ _left_rotate(words[index - 2], 13) ^ (words[index - 2] >> 10)
            words.append((words[index - 16] + first + words[index - 7] + second) & 0xFFFFFFFF)
        working = state[:]
        for index in range(64):
            a, b, c, d, e, f, g, h = working
            sigma_one = _left_rotate(e, 26) ^ _left_rotate(e, 21) ^ _left_rotate(e, 7)
            choose = (e & f) ^ (~e & g)
            temp_one = (h + sigma_one + choose + _SHA256_K[index] + words[index]) & 0xFFFFFFFF
            sigma_zero = _left_rotate(a, 30) ^ _left_rotate(a, 19) ^ _left_rotate(a, 10)
            majority = (a & b) ^ (a & c) ^ (b & c)
            temp_two = (sigma_zero + majority) & 0xFFFFFFFF
            working = [(temp_one + temp_two) & 0xFFFFFFFF, a, b, c, (d + temp_one) & 0xFFFFFFFF, e, f, g]
        state = [(left + right) & 0xFFFFFFFF for left, right in zip(state, working)]
    return b"".join(value.to_bytes(4, "big") for value in state).hex().upper()


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


def _aes_gf_mul(left: int, right: int) -> int:
    result = 0
    for _ in range(8):
        if right & 1:
            result ^= left
        left = ((left << 1) ^ (0x11B if left & 0x80 else 0)) & 0xFF
        right >>= 1
    return result


def _aes_sbox_value(value: int) -> int:
    inverse = 0 if value == 0 else next(
        candidate for candidate in range(1, 256) if _aes_gf_mul(value, candidate) == 1
    )
    rotated = inverse
    for shift in (1, 2, 3, 4):
        rotated ^= ((inverse << shift) | (inverse >> (8 - shift))) & 0xFF
    return rotated ^ 0x63


_AES_SBOX = [_aes_sbox_value(value) for value in range(256)]
_AES_INV_SBOX = [0] * 256
for _value, _substituted in enumerate(_AES_SBOX):
    _AES_INV_SBOX[_substituted] = _value


def _aes_key_bytes(key: str) -> bytes:
    key = key.strip()
    hex_part = key[2:] if key.lower().startswith("0x") else key
    if len(hex_part) == 32 and _is_pure_hex(hex_part):
        return bytes.fromhex(hex_part)
    key_bytes = key.encode("utf-8")
    if len(key_bytes) != 16:
        raise ValueError("Khóa AES-128 phải có đúng 16 ký tự UTF-8 hoặc 32 ký tự hex.")
    return key_bytes


def _aes_round_keys(key: bytes) -> list[list[int]]:
    words = [list(key[index:index + 4]) for index in range(0, 16, 4)]
    rcon = 1
    while len(words) < 44:
        word = words[-1][:]
        if len(words) % 4 == 0:
            word = word[1:] + word[:1]
            word = [_AES_SBOX[value] for value in word]
            word[0] ^= rcon
            rcon = _aes_gf_mul(rcon, 2)
        words.append([left ^ right for left, right in zip(words[-4], word)])
    return [sum(words[index:index + 4], []) for index in range(0, 44, 4)]


def _aes_add_round_key(state: list[int], round_key: list[int]) -> None:
    for index in range(16):
        state[index] ^= round_key[index]


def _aes_sub_bytes(state: list[int], inverse: bool = False) -> None:
    box = _AES_INV_SBOX if inverse else _AES_SBOX
    for index in range(16):
        state[index] = box[state[index]]


def _aes_shift_rows(state: list[int], inverse: bool = False) -> None:
    original = state[:]
    for row in range(4):
        for column in range(4):
            source_column = (column - row if inverse else column + row) % 4
            state[4 * column + row] = original[4 * source_column + row]


def _aes_mix_columns(state: list[int], inverse: bool = False) -> None:
    coefficients = (14, 11, 13, 9) if inverse else (2, 3, 1, 1)
    for column in range(4):
        offset = column * 4
        values = state[offset:offset + 4]
        state[offset] = (
            _aes_gf_mul(values[0], coefficients[0])
            ^ _aes_gf_mul(values[1], coefficients[1])
            ^ _aes_gf_mul(values[2], coefficients[2])
            ^ _aes_gf_mul(values[3], coefficients[3])
        )
        state[offset + 1] = (
            _aes_gf_mul(values[0], coefficients[3])
            ^ _aes_gf_mul(values[1], coefficients[0])
            ^ _aes_gf_mul(values[2], coefficients[1])
            ^ _aes_gf_mul(values[3], coefficients[2])
        )
        state[offset + 2] = (
            _aes_gf_mul(values[0], coefficients[2])
            ^ _aes_gf_mul(values[1], coefficients[3])
            ^ _aes_gf_mul(values[2], coefficients[0])
            ^ _aes_gf_mul(values[3], coefficients[1])
        )
        state[offset + 3] = (
            _aes_gf_mul(values[0], coefficients[1])
            ^ _aes_gf_mul(values[1], coefficients[2])
            ^ _aes_gf_mul(values[2], coefficients[3])
            ^ _aes_gf_mul(values[3], coefficients[0])
        )


def _aes_transform_block(block: bytes, round_keys: list[list[int]], decrypt: bool) -> bytes:
    state = list(block)
    if decrypt:
        _aes_add_round_key(state, round_keys[10])
        for round_key in reversed(round_keys[1:10]):
            _aes_shift_rows(state, inverse=True)
            _aes_sub_bytes(state, inverse=True)
            _aes_add_round_key(state, round_key)
            _aes_mix_columns(state, inverse=True)
        _aes_shift_rows(state, inverse=True)
        _aes_sub_bytes(state, inverse=True)
        _aes_add_round_key(state, round_keys[0])
    else:
        _aes_add_round_key(state, round_keys[0])
        for round_key in round_keys[1:10]:
            _aes_sub_bytes(state)
            _aes_shift_rows(state)
            _aes_mix_columns(state)
            _aes_add_round_key(state, round_key)
        _aes_sub_bytes(state)
        _aes_shift_rows(state)
        _aes_add_round_key(state, round_keys[10])
    return bytes(state)


def _aes_pad(data: bytes) -> bytes:
    padding = 16 - len(data) % 16
    return data + bytes([padding] * padding)


def aes_encrypt(plaintext: str, key: str) -> str:
    round_keys = _aes_round_keys(_aes_key_bytes(key))
    data = _aes_pad(plaintext.encode("utf-8"))
    return b"".join(
        _aes_transform_block(data[index:index + 16], round_keys, False)
        for index in range(0, len(data), 16)
    ).hex().upper()


def aes_decrypt(ciphertext_hex: str, key: str) -> str:
    try:
        data = bytes.fromhex(ciphertext_hex.strip().replace(" ", ""))
    except ValueError as error:
        raise ValueError("Bản mã AES phải là chuỗi hex hợp lệ.") from error
    if not data or len(data) % 16:
        raise ValueError("Độ dài bản mã AES phải là bội số của 16 bytes.")
    round_keys = _aes_round_keys(_aes_key_bytes(key))
    plaintext = b"".join(
        _aes_transform_block(data[index:index + 16], round_keys, True)
        for index in range(0, len(data), 16)
    )
    padding = plaintext[-1]
    if padding < 1 or padding > 16 or plaintext[-padding:] != bytes([padding] * padding):
        raise ValueError("Padding AES không hợp lệ, có thể sai khóa.")
    try:
        return plaintext[:-padding].decode("utf-8")
    except UnicodeDecodeError:
        return "0x" + plaintext[:-padding].hex().upper()


def rsa_encrypt(plaintext: str, p: int, q: int, e: int) -> str:
    modulus = p * q
    if p < 2 or q < 2 or p == q or gcd(e, (p - 1) * (q - 1)) != 1:
        raise ValueError("RSA cần p, q khác nhau và e nguyên tố cùng nhau với phi(n).")
    return " ".join(str(pow(byte, e, modulus)) for byte in plaintext.encode("utf-8"))


def rsa_decrypt(ciphertext: str, p: int, q: int, e: int) -> str:
    modulus = p * q
    phi = (p - 1) * (q - 1)
    if p < 2 or q < 2 or p == q or gcd(e, phi) != 1:
        raise ValueError("RSA cần p, q khác nhau và e nguyên tố cùng nhau với phi(n).")
    private_exponent = pow(e, -1, phi)
    try:
        data = bytes(pow(int(value), private_exponent, modulus) for value in ciphertext.split())
        return data.decode("utf-8")
    except (ValueError, OverflowError, UnicodeDecodeError) as error:
        raise ValueError("Bản mã RSA phải là các số nguyên hợp lệ với đúng khóa.") from error


def hash_text(text: str, algorithm: str) -> str:
    if algorithm == "md5":
        return md5_text(text)
    if algorithm == "sha256":
        return sha256_text(text)
    raise ValueError("Thuật toán băm không được hỗ trợ.")


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
    aes_key = "ThucHanhAES20260"
    assert aes_decrypt(aes_encrypt("Xin chao AES!", aes_key), aes_key) == "Xin chao AES!"
    assert rsa_decrypt(rsa_encrypt("RSA", 61, 53, 17), 61, 53, 17) == "RSA"
    assert hash_text("abc", "md5") == "900150983CD24FB0D6963F7D28E17F72"
    assert hash_text("abc", "sha256") == "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD"


if __name__ == "__main__":
    _self_check()
    print("Tất cả kiểm tra thuật toán đều đạt.")
