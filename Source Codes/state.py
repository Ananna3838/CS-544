# state.py

"""
Defines the client/server FSM states used to enforce protocol message order.
"""

from enum import Enum

class State(Enum):
    INIT_WAIT = 1  
    AUTH_WAIT = 2
    CHAT_READY = 3
    IN_CHAT = 4
    CLOSING = 5
    CLOSED = 6
