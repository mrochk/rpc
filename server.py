import sys
import socket
import rpcnet   
import rpcbind 
import struct
import enum

TEST_PROG = 0x20000001
TEST_VERS = 1

class Procedure(enum.Enum):
	Null = 0
	Pi   = 1
	Inc  = 2
	Add  = 3
	Echo = 4

	def null() -> bytes:
		return b''

	def pi() -> bytes:
		return(struct.pack(">d", 3.1415926))

	def inc(args : bytes) -> bytes:
		arg = int.from_bytes(args, "big")
		return int.to_bytes(arg + 1, 4, "big")
		
	def add(args : bytes) -> bytes:
		arg1, arg2 = int.from_bytes(args[:4], "big"), int.from_bytes(args[4:], "big")
		return int.to_bytes(arg1 + arg2, 4, "big")

	def echo(args : bytes) -> bytes:
		return args

def handler(xid, prog, vers, proc, args):
	print("=> call Procedureedure", Procedure)
	match proc:
		case Procedure.Null:
			return Procedure.null()
		case Procedure.Pi:
			return Procedure.pi()
		case Procedure.Inc:
			return Procedure.inc(args)
		case Procedure.Add:
			return Procedure.add(args)
		case Procedure.Echo:
			return Procedure.echo(args)

if __name__ == '__main__':
    if (len(sys.argv) != 2) :
        print("Usage: server.py <port>")
        sys.exit(1)
    host = ''
    port = int(sys.argv[1])
    # Create server socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    # Register the program to rpcbind.
    rpcbind.register(1, TEST_PROG, TEST_VERS, port)
    print(f"Server listening on port {port}..")
    # Listen and serve requests.
    while True:
        rpcnet.reply(server_socket, handler)