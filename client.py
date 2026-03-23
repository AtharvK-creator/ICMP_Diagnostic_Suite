import socket
import ssl
import time

HOST = "127.0.0.1"
PORT = 5000

context = ssl._create_unverified_context()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock, server_hostname=HOST)

secure_sock.connect((HOST, PORT))

print("Connected to diagnostic server")

while True:
    cmd = input("Enter command (PING/TRACE/PERF host): ")

    # ✅ Basic input validation
    parts = cmd.split()
    if len(parts) < 2:
        print("❌ Invalid command format. Use: PING/TRACE/PERF <host>")
        continue

    command = parts[0].upper()
    host = parts[1]

    # 🔥 PERF COMMAND
    if command == "PERF":
        requests = 5
        total_time = 0
        success = 0

        print(f"\nRunning performance test on {host}...\n")

        for i in range(requests):
            try:
                start = time.time()

                secure_sock.send(f"PING {host}".encode())
                data = secure_sock.recv(4096)

                end = time.time()
                response_time = (end - start) * 1000
                total_time += response_time

                if b"Packets Received" in data:
                    success += 1

                print(f"Request {i+1}: {response_time:.2f} ms")

            except ssl.SSLEOFError:
                print("❌ SSL Connection closed by server.")
                break
            except ssl.SSLError as e:
                print(f"❌ SSL Error: {e}")
                break
            except socket.gaierror:
                print("❌ Invalid hostname.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break

        if requests > 0:
            avg_time = total_time / requests

            print("\n===== PERFORMANCE REPORT =====")
            print(f"Total Requests: {requests}")
            print(f"Successful: {success}")
            print(f"Average Response Time: {avg_time:.2f} ms\n")

    # 🔵 NORMAL COMMANDS
    else:
        try:
            secure_sock.send(cmd.encode())
            data = secure_sock.recv(4096).decode()

            if not data:
                print("❌ No response from server.")
            else:
                print(data)

        except ssl.SSLEOFError:
            print("❌ Connection closed unexpectedly (SSL Error).")
            break

        except ssl.SSLError as e:
            print(f"❌ SSL Error: {e}")
            break

        except socket.gaierror:
            print("❌ Invalid hostname.")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")