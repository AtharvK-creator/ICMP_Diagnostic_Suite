import socket
import struct
import time
import os

ICMP_ECHO_REQUEST = 8


def checksum(source):
    sum = 0
    countTo = (len(source) // 2) * 2

    count = 0
    while count < countTo:
        thisVal = source[count + 1] * 256 + source[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count += 2

    if countTo < len(source):
        sum += source[-1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def create_packet(pid):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, pid, 1)
    data = struct.pack("d", time.time())

    chksum = checksum(header + data)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0,
                         socket.htons(chksum), pid, 1)

    return header + data


def ping_host(host, count=4):
    dest = socket.gethostbyname(host)

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.settimeout(2)

    pid = os.getpid() & 0xFFFF

    sent = 0
    received = 0
    rtts = []
    icmp_messages = []   # ✅ NEW

    # ✅ ICMP TYPE-CODE MAPPING
    ICMP_DESCRIPTIONS = {
        (0, 0): "Echo Reply (Success)",
        (3, 0): "Destination Network Unreachable",
        (3, 1): "Destination Host Unreachable",
        (3, 2): "Destination Protocol Unreachable",
        (3, 3): "Destination Port Unreachable",
        (3, 6): "Destination Network Unknown",
        (3, 7): "Destination Host Unknown",
        (4, 0): "Source Quench (Congestion Control)",
        (8, 0): "Echo Request",
        (9, 0): "Router Advertisement",
        (10, 0): "Router Discovery",
        (11, 0): "TTL Expired (Time Exceeded)",
        (12, 0): "Bad IP Header"
    }

    for _ in range(count):
        packet = create_packet(pid)

        start = time.time()
        sock.sendto(packet, (dest, 1))
        sent += 1

        try:
            recv_packet, addr = sock.recvfrom(1024)
            end = time.time()

            ip_header_len = (recv_packet[0] & 0x0F) * 4
            icmp_header = recv_packet[ip_header_len:ip_header_len + 8]

            type, code, chksum, p_id, seq = struct.unpack("bbHHh", icmp_header)

            # ✅ Decode ICMP
            icmp_info = ICMP_DESCRIPTIONS.get(
                (type, code),
                f"Unknown ICMP Type {type}, Code {code}"
            )
            icmp_messages.append(icmp_info)

            if p_id == pid:
                rtt = (end - start) * 1000
                rtts.append(rtt)
                received += 1

        except socket.timeout:
            icmp_messages.append("No Reply (Timeout / ICMP Blocked)")

        time.sleep(1)

    loss = ((sent - received) / sent) * 100

    result = f"""
Ping statistics for {host}

Packets Sent: {sent}
Packets Received: {received}
Packet Loss: {loss:.1f} %
"""

    # ✅ Unreachable note
    if received == 0:
        result += "\nNote: Host may be unreachable or blocking ICMP requests.\n"

    if rtts:
        result += f"""
Min RTT: {min(rtts):.2f} ms
Avg RTT: {sum(rtts)/len(rtts):.2f} ms
Max RTT: {max(rtts):.2f} ms
"""

    # ✅ ADD ICMP ANALYSIS OUTPUT
    if icmp_messages:
        result += "\nICMP Analysis:\n"
        for msg in icmp_messages:
            result += f"- {msg}\n"

    return result