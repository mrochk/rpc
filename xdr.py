import xdrlib

def encode_double(val) -> bytes:
    """
    >>> encode_double(1.2).hex()
    '3ff3333333333333'
    """
    p = xdrlib.Packer()
    p.pack_double(val)
    return p.get_buffer()

def encode_int(val) -> bytes:
    """
    >>> encode_int(-1).hex()
    'ffffffff'
    """
    p = xdrlib.Packer()
    p.pack_int(val)
    return p.get_buffer()

def encode_uint(val) -> bytes:
    """
    >>> encode_uint(10).hex()
    '0000000a'
    """
    p = xdrlib.Packer()
    p.pack_uint(val)
    return p.get_buffer()

def encode_bool(val : bool) -> bytes:
    """
    >>> encode_bool(True).hex()
    '00000001'
    """
    p = xdrlib.Packer()
    p.pack_bool(val)
    return p.get_buffer()

def encode_string(val: str) -> bytes:
    """
    >>> encode_string("hello").hex()
    '0000000568656c6c6f000000'
    """
    p = xdrlib.Packer()
    p.pack_string(val.encode())
    return p.get_buffer()

def encode_two_int(val1, val2) -> bytes:
    """
    >>> encode_two_int(-1,2).hex()
    'ffffffff00000002'
    """
    p = xdrlib.Packer()
    p.pack_int(val1)
    p.pack_int(val2)
    return p.get_buffer()

def decode_double(data : bytes):
    """
    >>> msg = bytes.fromhex('3ff3333333333333')
    >>> decode_double(msg)
    1.2
    """
    u = xdrlib.Unpacker(data)
    return u.unpack_double()

def decode_int(data : bytes):
    """
    >>> msg = bytes.fromhex('ffffffff')
    >>> decode_int(msg)
    -1
    """
    u = xdrlib.Unpacker(data)
    return u.unpack_int()

def decode_uint(data : bytes):
    """
    >>> msg = bytes.fromhex('00000001')
    >>> decode_uint(msg)
    1
    """
    u = xdrlib.Unpacker(data)
    return u.unpack_uint()

def decode_bool(data : bytes):
    """
    >>> msg = bytes.fromhex('00000001')
    >>> decode_bool(msg)
    True
    """
    u = xdrlib.Unpacker(data)
    return u.unpack_bool()

def decode_string(data : bytes) -> str:
    """
    >>> msg = bytes.fromhex('0000000568656c6c6f000000')
    >>> decode_string(msg)
    'hello'
    """
    u = xdrlib.Unpacker(data)
    return u.unpack_string().decode("utf-8")

def decode_two_int(data):
    """
    >>> msg = bytes.fromhex('ffffffff00000002')
    >>> decode_two_int(msg)
    (-1, 2)
    """
    u    = xdrlib.Unpacker(data)
    res1 = u.unpack_int()
    res2 = u.unpack_int()
    return res1, res2

if __name__ == "__main__":
    import doctest
    doctest.testmod()