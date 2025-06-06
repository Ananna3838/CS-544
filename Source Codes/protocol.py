# protocol.py

"""
Defines a message type constants and helper functions to pack/unpack the 12-byte protocol header
"""

import struct

# Message Type constants
MSG_INIT     = 0x01
MSG_AUTH     = 0x02
MSG_AUTH_ACK = 0x03
MSG_JOIN     = 0x04
MSG_CHAT     = 0x05
MSG_CHAT_ACK = 0x06
MSG_TYPING   = 0x07
MSG_LEAVE    = 0x08
MSG_ERROR    = 0x09
MSG_CLOSE    = 0x0A

# Header Format: version(1), msg_type(1), flags(1), reserved(1), session_id(4), payload_len(4)
HEADER_FORMAT = "!BBBBII"  # Total: 12 bytes
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def pack_header(version, msg_type, flags, reserved, session_id, payload_len):
    """Packs the protocol header into binary format."""
    return struct.pack(HEADER_FORMAT, version, msg_type, flags, reserved, session_id, payload_len)

def unpack_header(data):
    """Unpacks a 12-byte binary header into its components"""
    return struct.unpack(HEADER_FORMAT, data)
