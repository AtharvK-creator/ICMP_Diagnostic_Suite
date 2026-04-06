# ICMP-Based Network Diagnostic Suite

## Problem Statement
This project implements a secure network diagnostic tool that allows users to perform Ping, Traceroute, and Performance analysis using ICMP. The system follows a client-server architecture with secure communication over SSL/TLS.

---

## Architecture

Client -> TCP Socket -> SSL Layer -> Server -> ICMP Engine -> Target Host

1. Client sends commands (PING / TRACE / PERF)
2. Communication happens over TCP sockets secured using SSL
3. Server processes requests using ICMP (raw sockets)
4. Target host responds with ICMP packets
5. Server sends results back to the client

---

## Features

- ICMP Ping (Echo Request/Reply)
- Traceroute using TTL manipulation
- Performance analysis (PERF command)
- TCP Socket Programming
- SSL/TLS Secure Communication
- Multi-client support using threading
- Error handling (invalid host, SSL errors, timeouts)

---

## Technologies Used

- Python
- Socket Programming (TCP and Raw Sockets)
- SSL/TLS Security
- ICMP Protocol

---

## ICMP Error Handling

The system demonstrates ICMP-based error detection:

- Type 0: Echo Reply (Success)
- Type 3: Destination Unreachable
- Type 11: Time Exceeded

These messages help identify network failures and routing issues.

---

## Performance Metrics

- Round Trip Time (RTT)
- Packet Loss Percentage
- Average Latency (via PERF command)
- Multiple request handling for consistency

---

## Example Commands

PING google.com  
TRACE 8.8.8.8  
PERF google.com  

---

## Sample Output

Reply from 142.250.xxx.xxx  
RTT = 32 ms  

Packets Sent: 4  
Packets Received: 4  
Packet Loss: 0%  

Invalid hostname or unreachable domain  

1   192.168.1.1  
2   10.23.xxx.xxx  
3   * * * Request timed out  
---

## Security Implementation

- SSL/TLS is used to encrypt communication between client and server
- Ensures secure and reliable data exchange over the network

---

## How to Run
IMP (This is structured for Linux)
### Start Server
python3 server.py (Run as administrator use sudo command)

### Start Client
python3 client.py

---

## Project Structure

ICMP_Mini_project/
- client.py
- server.py
- icmp_ping.py
- traceroute.py
- performance.py
- certs/
- README.md

---

## Notes

- Some routers or networks may block ICMP packets, resulting in "Request timed out"
- This is expected behavior due to firewall and security policies
- The application still correctly demonstrates traceroute and ICMP functionality

---

## Conclusion

This project demonstrates:
- Low-level socket programming
- ICMP protocol handling
- Secure communication using SSL/TLS
- Multi-client server architecture
- Network performance evaluation

---
