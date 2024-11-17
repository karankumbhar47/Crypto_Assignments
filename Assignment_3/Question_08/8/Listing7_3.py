def cmp_const(a: bytes, b: bytes, size: int) -> int:
    result = 0
    a, b = bytearray(a), bytearray(b)
    for i in range(size):
        result |= a[i] ^ b[i]
    return result
