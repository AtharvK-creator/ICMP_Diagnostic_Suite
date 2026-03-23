import socket
import ssl
import threading
from icmp_ping import ping_host
from traceroute import traceroute

HOST = "0.0.0.0"
PORT = 5000


def handle_client(conn, addr):
    print("Client connected:", addr)

    while True:
        try:
            data = conn.recv(1024).decode()

            if not data:
                break

            command = data.split()

            # ✅ Input validation
            if len(command) < 2:
                conn.send("Invalid input. Use: PING <host> or TRACE <host>".encode())
                continue   # ✅ inside try block

            if command[0].upper() == "PING":
                result = ping_host(command[1])

            elif command[0].upper() == "TRACE":
                result = traceroute(command[1])

            else:
                result = "Invalid command"

            conn.send(result.encode())

        except Exception as e:
            print("Error:", e)
            break   # ✅ properly inside except

    conn.close()
    print("Client disconnected:", addr)


def start_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")

    secure_sock = context.wrap_socket(sock, server_side=True)

    print("Secure ICMP Diagnostic Server Running...")

    while True:
        conn, addr = secure_sock.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start_server()
