import socket
import rpcmsg

MAXMSG = 1500

def call(host, port, xid, prog, vers, proc, args) -> bytes:
    # Creating socket to send call to RPC Server
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Encoding the msg in XDR format
    msg=rpcmsg.encode_call(xid, prog, vers, proc, args)
    # Sending the msg to the server
    sock.sendto(msg, (host, port))
    # Waiting for the server reply and storing it
    response, _=sock.recvfrom(MAXMSG)
    # Decoding the server reply from XDR format
    _, response=rpcmsg.decode_reply(response)
    return response

def reply(sserver, handle):
    # Waiting from client request.
    call, clientaddr = sserver.recvfrom(MAXMSG)
    # Decoding the XDR formated request.
    xid, prog, vers, proc, args = rpcmsg.decode_call(call)
    # Calling handle function (returns bytes in XDR format).
    reply = handle(xid, prog, vers, proc, args)
    # Encoding the reply in XDR format
    reply = rpcmsg.encode_reply(xid, reply)
    # Sending the result to the client.
    sserver.sendto(reply, clientaddr)