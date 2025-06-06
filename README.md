# CS-544-Final Project- QUIC Chat Protocol
This project implements a **stateful application-layer protocol** over QUIC-like behavior using Python and asyncio. The client and server communicate using a custom-designed **Finite State Machine (FSM)** and structured **Protocol Data Units (PDUs)**.

## Features
- **Custom Stateful Protocol** with defined DFA transitions.
- **Structured PDU Message Format** using `struct.pack/unpack`.
- **Client-Server Chat Simulation** with INIT, AUTH, JOIN, CHAT, and CLOSE phases.
- **Command-line Configuration** (IP and Port) for flexibility.
- **Minimal Dependency**: Uses only Python Standard Library (compliant with no 3rd-party kernel use).

## Protocol Overview

### Message Types
| Name         | Code |
|--------------|------|
| INIT         | 0x01 |
| AUTH         | 0x02 |
| AUTH_ACK     | 0x03 |
| JOIN         | 0x04 |
| CHAT         | 0x05 |
| CHAT_ACK     | 0x06 |
| TYPING       | 0x07 |
| LEAVE        | 0x08 |
| ERROR        | 0x09 |
| CLOSE        | 0x0A |

### Header Format
Each message header is 12 bytes, with the structure:

| version | msg_type | flags | reserved | session_id (4B) | payload_len (4B) |
Structured using `!BBBBII` (network byte order, 12 bytes total).

### Finite State Machine (FSM)
The server implements a strict FSM:
- `INIT_WAIT` → `AUTH_WAIT` → `CHAT_READY` → `IN_CHAT` → `CLOSING` → `CLOSED`
Only valid transitions are allowed. Invalid messages in any state lead to session termination.

## Usage Instructions
### 1. Clone the repository
```bash
git clone https://github.com/yourusername/quic_chat.git
cd quic_chat

### 2. Prerequisites
Ensure Python 3.8 or higher is installed:
```bash
python3 --version

This project is implemented in Python 3.8+ and uses asyncio and standard libraries only. A Makefile is provided for automation on Linux-based systems.
