import socket
import ssl
import time

HOST = "127.0.0.1"
PORT = 5000

def test_performance(requests=10):

    context = ssl._create_unverified_context()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_hostname=HOST)

    secure_sock.connect((HOST, PORT))

    total_time = 0
    success = 0

    for i in range(requests):
        start = time.time()

        secure_sock.send(b"PING google.com")
        data = secure_sock.recv(4096)

        end = time.time()

        response_time = (end - start) * 1000
        total_time += response_time

        if b"Packets Received" in data:
            success += 1

        print(f"Request {i+1}: {response_time:.2f} ms")

    avg_time = total_time / requests

    print("\n===== PERFORMANCE REPORT =====")
    print(f"Total Requests: {requests}")
    print(f"Successful: {success}")
    print(f"Average Response Time: {avg_time:.2f} ms")

    secure_sock.close()


test_performance()
