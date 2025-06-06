# client.py

"""QUIC Chat Client
Connects to the QUIC-like server using asyncio.
Implements the client-side state transitions and sends a sequence of protocol messages:
INIT → AUTH → JOIN → CHAT → CLOSE.
"""
import asyncio
import struct
import argparse
from protocol import *

async def run_client(ip, port):

    """
    Main Client coroutine. Connects to the server, performs authentication, joins a room, sends a message, and closes.
    """
    print(f"[Client] Connecting to server at {ip}:{port}...")  # 👈 Added print line

    reader, writer = await asyncio.open_connection(ip, port)
    session_id = 1234
    version = 1

    # Send INIT Message
    print("[Client] Sending INIT...")
    init_header = pack_header(version, MSG_INIT, 0, 0, session_id, 0)
    writer.write(init_header)
    await writer.drain()

    # Prepare AUTH Message with username and password
    username = b'sadia' + b'\x00' * (32 - len('sadia'))
    password = b'admin' + b'\x00' * (32 - len('admin'))
    auth_payload = username + password
    print("[Client] Sending AUTH...")
    auth_header = pack_header(version, MSG_AUTH, 0, 0, session_id, len(auth_payload))
    writer.write(auth_header + auth_payload)
    await writer.drain()

    # Wait for AUTH_ACK from server
    print("[Client] Waiting for AUTH_ACK...")
    ack_header = await reader.readexactly(12)
    _, msg_type, *_ = unpack_header(ack_header)
    if msg_type == MSG_AUTH_ACK:
        print("[Client] Authentication successful.")

        # Send JOIN message to join a chat room
        room_type = 1  # room-based
        room_name = b'room1' + b'\x00' * (32 - len('room1'))
        join_payload = struct.pack("!B32s", room_type, room_name)
        print("[Client] Sending JOIN...")
        join_header = pack_header(version, MSG_JOIN, 0, 0, session_id, len(join_payload))
        writer.write(join_header + join_payload)
        await writer.drain()

        # Send a CHAT message
        chat_msg = b"Hello QUIC Server!" + b'\x00' * (256 - len('Hello QUIC Server!'))
        print("[Client] Sending CHAT...")
        chat_header = pack_header(version, MSG_CHAT, 0, 0, session_id, len(chat_msg))
        writer.write(chat_header + chat_msg)
        await writer.drain()

        # Close the connection
        print("[Client] Sending CLOSE...")
        close_header = pack_header(version, MSG_CLOSE, 0, 0, session_id, 0)
        writer.write(close_header)
        await writer.drain()

    else:
        print("[Client] Authentication failed or invalid response.")

    writer.close()
    await writer.wait_closed()
    print("[Client] Connection closed.")

if __name__ == "__main__":
    # Parse command-line arguments for IP and port
    parser = argparse.ArgumentParser(description="QUIC Chat Client")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Server IP address")
    parser.add_argument("--port", type=int, default=8888, help="Server port")
    args = parser.parse_args()

    asyncio.run(run_client(args.ip, args.port))
