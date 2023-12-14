from dataclasses import dataclass, asdict
from datetime import datetime as dt
from build import chat_pb2


@dataclass
class Message:
    from_user: str
    to_user: str
    body: str
    timestamp: dt

    def to_pb(self):
        """Convert Message to protobuf object."""
        return chat_pb2.Message(from_user=self.from_user, to_user=self.to_user,
                                body=self.body, timestamp=str(self.timestamp))

    def to_dict(self) -> dict:
        """Convert Message to dictionary."""
        return asdict(self)

    def get_unique_key(self) -> str:
        """Get unique key for the message."""
        return f"{self.to_user}.{self.timestamp}"
