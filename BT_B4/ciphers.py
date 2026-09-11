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

    # ponytail: dùng x làm ký tự đệm; cần lưu độ dài bản rõ nếu muốn giữ chữ x cuối.
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


if __name__ == "__main__":
    _self_check()
    print("Tất cả kiểm tra thuật toán đều đạt.")
