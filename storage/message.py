"""The module defines the Message data model
for the gRPC Chat application.

The Message class in this module represents the data structure
for message information within the chat system.
This class is designed to facilitate easy conversion between Python
dataclass objects and protobuf message objects, enabling seamless
serialization and deserialization of chat messages.
"""

from dataclasses import dataclass, asdict
from datetime import datetime as dt

from build import chat_pb2


@dataclass
class Message:
    """A dataclass representing a message in the chat system."""
    from_user: str
    to_user: str
    body: str
    timestamp: dt

    def to_dict(self) -> dict:
        """Convert Message to dictionary."""
        data = asdict(self)
        data["timestamp"] = str(self.timestamp)
        return data

    def get_unique_key(self) -> str:
        """Get unique key for the message."""
        return f"message.{self.to_user}.{self.timestamp}"

    def to_pb(self):
        """Convert the message object to a protobuf message."""
        return chat_pb2.Message(
            from_user=self.from_user,
            to_user=self.to_user,
            body=self.body,
            timestamp=self.timestamp
        )

    @classmethod
    def from_pb(cls, pb_message):
        """Convert a protobuf message to a Message object."""
        return cls(
            from_user=pb_message.from_user,
            to_user=pb_message.to_user,
            body=pb_message.body,
            timestamp=pb_message.timestamp
        )
