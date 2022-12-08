#!/usr/bin/python3

# RPC Bind Module
# Author(s): Maxime Rochkoulets, Achille Harismendy

import xdr
import xdrlib
import rpcnet

RPCB_HOST = "localhost"
RPCB_PORT = 111
RPCB_PROG = 100000 # rpcbind / portmap
RPCB_VERS = 4

RPCBPROC_SET     = 1
RPCBPROC_UNSET   = 2
RPCBPROC_GETADDR = 3

NETID = "udp"
OWNER = ""

def make_rpcb_struct(prog, vers, uaddr):
    p = xdrlib.Packer()
    p.pack_uint(int(prog))
    p.pack_uint(vers)
    p.pack_string(NETID.encode())
    p.pack_string(uaddr.encode())
    p.pack_string(OWNER.encode())
    return p.get_buffer()

def getport(xid, prog, vers) -> int:
    uaddr = ""
    args = make_rpcb_struct(prog, vers, uaddr)
    res = rpcnet.call(RPCB_HOST, RPCB_PORT, xid, RPCB_PROG, 
        RPCB_VERS, RPCBPROC_GETADDR, args)
    u = xdrlib.Unpacker(res)
    rpcb_res = u.unpack_bytes()
    univ_addr = str(rpcb_res).replace("'", "").split('.')
    return int(univ_addr[-2]) * 256 + int(univ_addr[-1])

def register(xid, prog, vers, port) -> bool:
    uaddr = "127.0.0.1." + str(port - 256)
    args = make_rpcb_struct(prog, vers, uaddr)
    res = rpcnet.call(RPCB_HOST, RPCB_PORT, xid, 
        RPCB_PROG, RPCB_VERS, RPCBPROC_SET, args)
    u = xdrlib.Unpacker(res)
    rpcb_res = u.unpack_bool()
    return rpcb_res

def unregister(xid, prog, vers) -> bool:
    uaddr = ""
    args = make_rpcb_struct(prog, vers, uaddr)
    res = rpcnet.call(RPCB_HOST, RPCB_PORT, xid, 
        RPCB_PROG, RPCB_VERS, RPCBPROC_UNSET, args)
    u = xdrlib.Unpacker(res)
    rpcb_res = u.unpack_bool()
    return rpcb_res


# Tests :

# register prog 0x30000001 (version 1) with port 4001

ret1 = register(1, 0x30000001, 1, 4001)

# register prog 0x30000002 (version 1) with port 4002

ret2 = register(2, 0x30000002, 1, 4002)

# unregister prog 0x30000002 (version 1)

ret3 = unregister(3, 0x30000002, 1)

# get port of program 0x30000001 (version 1)

port = getport(4, 0x30000001, 1)

print(ret1, ret2, ret3)
print("port =", port)

# EOF