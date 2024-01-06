# pylint:disable=invalid-name
"""
    Contain utils function for IDEA
"""
import binascii

TWO_SIXTEEN = pow(2, 16)
TWO_SIXTEEN_PLUS_1 = TWO_SIXTEEN + 1


def XOR(a, b):
    """Bitwise XOR

    Returns:
        str: value of XOR a and b
    """
    if len(a) != len(b):
        raise ValueError(
            f'XOR operator unequal sizes between inputs a={len(a)} b={len(b)}')

    result = ""
    for i, val in enumerate(a):
        result += '1' if val != b[i] else '0'

    return result


def circular_left_shift(binString, k):
    """Shift left k bit

    Args:
        binString (str): input binary string
        k (int): number of bits to shift left

    Returns:
        str: value after shift left
    """
    res = binString
    for _ in range(k):
        tmp = res[0]
        res = res[1:] + tmp
    return res


def generate_subkeys(data):
    """Generate subkeys

    Args:
        data (str): input key

    Raises:
        Exception: if length of keys != 128

    Returns:
        list: a list 52 subkeys generated from original key
    """
    if len(data) != 128:
        raise ValueError(
            f'generate keys function requires an input of 128 bits, but received {len(data)}')

    keys = []
    for _ in range(7):
        subkeys = split_into_x_parts_of_y(data, 8, 16)
        keys += subkeys
        data = circular_left_shift(data, 25)

    return keys[:-4]


def split_into_x_parts_of_y(data, x, y):
    """Split data into x parts, each part has y bit

    Args:
        data: input data
        x: number of parts
        y: number of bits of each part

    Returns:
        list: data splitted
    """
    res = []
    for i in range(x):
        multiplier = y * i
        start = 0 + multiplier
        stop = y + multiplier
        res.append(data[start:stop])
    return res


def generate_decrypt_keys(keys):
    """Generate subkeys for decryption

    Args:
        keys (list): keys for encryption

    Returns:
        list: list of keys using for decryption
    """
    decrypt_keys = []
    for i in range(8):
        step = i * 6
        lower_index = 46 - step

        decrypt_keys.append(
            m_mul_inv(keys[lower_index + 2], TWO_SIXTEEN_PLUS_1))

        tmp1 = 4
        tmp2 = 3
        if i == 0:
            tmp1 = 3
            tmp2 = 4

        decrypt_keys.append(m_sum_inv(keys[lower_index + tmp1], TWO_SIXTEEN))
        decrypt_keys.append(m_sum_inv(keys[lower_index + tmp2], TWO_SIXTEEN))

        decrypt_keys.append(
            m_mul_inv(keys[lower_index + 5], TWO_SIXTEEN_PLUS_1))
        decrypt_keys.append(keys[lower_index])
        decrypt_keys.append(keys[lower_index + 1])

    decrypt_keys.append(m_mul_inv(keys[0], TWO_SIXTEEN_PLUS_1))
    decrypt_keys.append(m_sum_inv(keys[1], TWO_SIXTEEN))
    decrypt_keys.append(m_sum_inv(keys[2], TWO_SIXTEEN))
    decrypt_keys.append(m_mul_inv(keys[3], TWO_SIXTEEN_PLUS_1))

    return decrypt_keys


def m_mul_inv(a, m):
    """Inverse modular multiplication

    Args:
        a (str): input data
        m (int): modulo with 2^16 + 1

    Returns:
        str: output value after Inverse modular multiplication
    """
    m0 = m
    y = 0
    x = 1
    a = int(a, 2)
    if m == 1:
        return 0

    while a > 1:

        # q is quotient
        q = a // m
        t = m

        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if x < 0:
        x = x + m0

    bits = bin(x)[2:]
    return bits.zfill(16)


def m_sum_inv(a, m):
    """Inverse modular addition

    Args:
        a (str): input data
        m (int): modulo with 2^16

    Returns:
        str: value after Inverse modular addition
    """
    res = m - int(a, 2)
    bits = bin(res)[2:]
    return bits.zfill(16)


def m_mul(a, b):
    """Modular mutiplication

    Returns:
        str: value after mutiply modulo
    """
    a = int(a, 2)
    b = int(b, 2)
    res = (a * b) % TWO_SIXTEEN_PLUS_1
    bits = bin(res)[2:]
    return bits.zfill(16)


def m_sum(a, b):
    """Modular addition

    Returns:
        str: value after add modulo
    """
    a = int(a, 2)
    b = int(b, 2)
    res = (a + b) % TWO_SIXTEEN
    bits = bin(res)[2:]
    return bits.zfill(16)


def int2bits(val):
    """Convert int to bits

    Args:
        val (int): input value

    Returns:
        str: binary string
    """
    bits = bin(val)[2:]
    return bits.zfill(128)


def decode_binary_string(s):
    """Convert binary to string

    Args:
        s (str): input binary

    Returns:
        str: string
    """
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(len(s)//8))


def str_to_bits(text, size=64, encoding='utf-8', errors='surrogatepass'):
    """Convert string to bits

    Args:
        text (str): input text
        size (int, optional): input size to convert. Defaults to 64.
        encoding (str, optional): _description_. Defaults to 'utf-8'.
        errors (str, optional): _description_. Defaults to 'surrogatepass'.

    Returns:
        str: bits
    """
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    if len(bits) < size:
        num = size - len(bits)
        bits = ''.zfill(num) + bits
    # return bits.zfill(8 * ((len(bits) + 7) // 8))
    return bits
