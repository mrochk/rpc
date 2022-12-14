import xdrlib

CALL = 0
REPLY = 1
RPC_VERSION = 2
AUTH_NONE = 0
MSG_ACCEPTED = 0
MSG_DENIED = 1
SUCCESS = 0

def encode_call(xid, prog, vers, proc, data) -> bytes:
    """
    >>> encode_call(1, 1, 1, 1, b'ABCD').hex()
    '0000000100000000000000020000000100000001000000010000000000000000000000000000000041424344'
    """
    p = xdrlib.Packer()
    p.pack_uint(xid)         # MSG ID
    p.pack_uint(CALL)        # 0 FOR CALL
    p.pack_uint(RPC_VERSION) # 2
    p.pack_uint(prog)        # PROG NUMBER
    p.pack_uint(vers)        # PROG VERSION
    p.pack_uint(proc)        # PROG VERSION
    p.pack_farray(2, [AUTH_NONE, AUTH_NONE], p.pack_uint)
    p.pack_farray(2, [AUTH_NONE, AUTH_NONE], p.pack_uint)
    return p.get_buffer() + data

def encode_reply(xid, data) -> bytes:
    """
    >>> encode_reply(1, b'ABCD').hex()
    '00000001000000010000000000000000000000000000000041424344'
    """
    p = xdrlib.Packer()
    p.pack_uint(xid)
    p.pack_uint(REPLY)
    p.pack_uint(MSG_ACCEPTED)
    p.pack_uint(AUTH_NONE)
    p.pack_uint(0)
    p.pack_uint(SUCCESS)
    return p.get_buffer() + data

def decode_call(msg : bytes):
    """
    >>> msg = bytes.fromhex('0000000100000000000000020000000100000001000000010000000000000000000000000000000041424344')
    >>> decode_call(msg)
    (1, 1, 1, 1, b'ABCD')
    """
    xid = prog = vers = proc = 0
    u = xdrlib.Unpacker(msg)
    xid = u.unpack_uint()  # XID
    u.unpack_farray(2, u.unpack_uint)
    prog = u.unpack_uint() # PROC
    vers = u.unpack_uint() # PROC
    proc = u.unpack_uint() # PROC
    u.unpack_farray(4, u.unpack_uint)
    data = msg[u.get_position():]
    return (xid, prog, vers, proc, data)

def decode_reply(msg):
    """
    >>> msg = bytes.fromhex('00000001000000010000000000000000000000000000000041424344')
    >>> decode_reply(msg)
    (1, b'ABCD')
    """
    xid = 0
    data = b''
    u = xdrlib.Unpacker(msg)
    xid = u.unpack_uint()
    u.unpack_farray(5, u.unpack_uint)
    data = msg[u.get_position():]
    return (xid, data)

if __name__ == "__main__":
    import doctest
    doctest.testmod()