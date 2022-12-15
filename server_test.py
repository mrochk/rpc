import xdr
import rpcnet

HOST = "localhost"
PORT = 7777
TEST_PROG = 0x20000001
TEST_VERS = 1
XID = 1000

PROC_NULL = 0
PROC_PI = 1
PROC_INC = 2
PROC_ADD = 3
PROC_ECHO = 4

result = rpcnet.call(HOST, PORT, XID, TEST_PROG, TEST_VERS, PROC_NULL, b'')
print("result procedure null =", "null" if len(result) == 0 else "error")

result = rpcnet.call(HOST, PORT, XID, TEST_PROG, TEST_VERS, PROC_PI, b'')
print("result procedure pi =", xdr.decode_double(result))

args = xdr.encode_int(10)
result = rpcnet.call(HOST, PORT, XID, TEST_PROG, TEST_VERS, PROC_INC, args)
print("result procedure inc = ", xdr.decode_int(result))

args = xdr.encode_two_int(10, 100)
result = rpcnet.call(HOST, PORT, XID, TEST_PROG, TEST_VERS, PROC_ADD, args)
print("result procedure add =", xdr.decode_int(result))

args = xdr.encode_string("Hello World!")
result = rpcnet.call(HOST, PORT, XID, TEST_PROG, TEST_VERS, PROC_ECHO, args)
print("result procedure echo =", xdr.decode_string(result))