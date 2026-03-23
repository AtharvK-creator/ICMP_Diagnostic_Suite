import socket
import struct
import time

def traceroute(dest_name, max_hops=20):
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434

    result = f"Traceroute to {dest_name} ({dest_addr})\n\n"

    for ttl in range(1, max_hops + 1):

        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        recv_socket.bind(("", port))
        recv_socket.settimeout(5)

        send_socket.sendto(b'', (dest_name, port))

        curr_addr = None
        curr_name = None

        try:
            start = time.time()
            data, curr_addr = recv_socket.recvfrom(512)
            end = time.time()

            curr_addr = curr_addr[0]

            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except:
                curr_name = curr_addr

            rtt = (end - start) * 1000

            result += f"{ttl}. {curr_name} ({curr_addr}) {rtt:.2f} ms\n"

        except socket.timeout:
            result += f"{ttl}. * * * Request timed out\n"

        finally:
            send_socket.close()
            recv_socket.close()

        if curr_addr == dest_addr:
            break

    return result
