# server.py

"""QUIC Chat Server
Implements a stateful chat server that accepts a single client at a time, 
validates messages in order using a finite state machine (FSA/DFA), and responds accordingly.
"""

import asyncio
import struct
import argparse
from protocol import *
from state import State  

async def handle_client(reader, writer):
    """
    Coroutine to handle a single client connection.
    Reads and processes messages in the expected stateful sequence:
    INIT → AUTH → JOIN → CHAT → CLOSE.
    """

    addr = writer.get_extra_info('peername')
    print(f"[Server] New client connected.")
    state = State.INIT_WAIT
    session_id = None

    try:
        while state != State.CLOSED:
            # Read and unpack 12-byte header
            header = await reader.readexactly(12)
            version, msg_type, flags, reserved, sid, payload_len = unpack_header(header)
            payload = await reader.readexactly(payload_len) if payload_len > 0 else b''

            # INIT -> AUTH_WAIT
            if state == State.INIT_WAIT and msg_type == MSG_INIT:
                print("[Server] INIT received.")
                session_id = sid
                state = State.AUTH_WAIT

            # AUTH_WAIT -> CHAT_READY
            elif state == State.AUTH_WAIT and msg_type == MSG_AUTH:
                username = payload[:32].rstrip(b'\x00').decode()
                password = payload[32:].rstrip(b'\x00').decode()
                print(f"[Server] AUTH: username={username}, password={password}")

                if username == "sadia" and password == "admin":
                    print("[Server] Auth OK.")
                    ack = pack_header(version, MSG_AUTH_ACK, 0, 0, session_id, 0)
                    writer.write(ack)
                    await writer.drain()
                    state = State.CHAT_READY
                else:
                    print("[Server] Auth failed.")
                    state = State.CLOSING

            # JOIN -> IN_CHAT
            elif state == State.CHAT_READY and msg_type == MSG_JOIN:
                room_type = payload[0]
                room_name = payload[1:].decode('utf-8').strip('\x00')
                print(f"[Server] Joined room: {room_name}")
                state = State.IN_CHAT
            
            # CHAT -> CLOSING
            elif state == State.IN_CHAT and msg_type == MSG_CHAT:
                msg = payload.decode('utf-8').strip('\x00')
                print(f"[Server] Chat message: {msg}")
                state = State.CLOSING  # Close after one message for demo

            #Handle CLOSE
            elif msg_type == MSG_CLOSE:
                print("[Server] Closing connection.")
                state = State.CLOSED

            else:
                print(f"[Server] Invalid message or out-of-order in state: {state}")
                state = State.CLOSED

    except asyncio.IncompleteReadError:
        print("[Server] Client disconnected unexpectedly.")
    except Exception as e:
        print(f"[Server] Error: {e}")

    print("[Server] Connection closed.")
    writer.close()
    await writer.wait_closed()

async def main():
    """
    Entry point: parse CLI port argument and starts the asyncio server.
    """

    parser = argparse.ArgumentParser(description="QUIC Chat Server")
    parser.add_argument('--port', type=int, default=8888, help="Port to bind the server")
    args = parser.parse_args()

    server = await asyncio.start_server(handle_client, '0.0.0.0', args.port)
    addr = server.sockets[0].getsockname()
    print(f"[Server] Server started on port {addr[1]}.")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
