from dataclasses import dataclass, asdict

from build import chat_pb2


@dataclass
class User:
    login: str
    full_name: str

    def to_pb(self):
        """Convert User to protobuf object."""
        return chat_pb2.User(login=self.login, full_name=self.full_name)

    def to_dict(self) -> dict:
        """Convert User to dictionary"""
        return asdict(self)

    def get_unique_key(self) -> str:
        """Get unique key for the user."""
        return self.login
