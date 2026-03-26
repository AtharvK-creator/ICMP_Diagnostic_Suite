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

            command = data.strip().split()   # 🔥 minor fix (strip added)

            # ✅ Input validation (same logic, improved message)
            if len(command) < 2:
                conn.send("❌ Invalid input. Use: PING <host> or TRACE <host>".encode())
                continue

            cmd = command[0].upper()   # 🔥 avoid repeated .upper()
            host = command[1]

            # ✅ Host validation (NEW but safe, no logic change)
            try:
                socket.gethostbyname(host)
            except socket.gaierror:
                conn.send("❌ Invalid hostname or unreachable domain".encode())
                continue

            # 🔵 SAME LOGIC (unchanged)
            if cmd == "PING":
                result = ping_host(host)

            elif cmd == "TRACE":
                result = traceroute(host)

            else:
                result = "❌ Invalid command"

            conn.send(result.encode())

        except Exception as e:
            print("Error:", e)
            break

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

        # 🔥 only small improvement: daemon=True (no logic change)
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()


start_server()