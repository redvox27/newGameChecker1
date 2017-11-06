from socket import *
from _thread import *

host = ""
port = 5555
s = socket(AF_INET, SOCK_STREAM) # initialize tcp socket

try:
    s.bind((host, port))

except error as e:
    print(str(e))

s.listen(5)
print("waiting for a connection")
def threaded_client(conn):
    conn.send(str.encode("welcome, type your info\n"))

    while True:
        data = conn.recv(2048)
        reply = "Server output: " + data.decode("utf-8")

        if not data:
            break

        conn.sendall(str.encode(reply))
    conn.close()


while True:
    conn, addr = s.accept()

    print("connected to: " + addr[0] + ":" + str(addr[1]))

    start_new_thread(threaded_client,(conn,))