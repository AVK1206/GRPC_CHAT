"""The module defines the User data model for the gRPC Chat application.

The User class in this module represents the data structure
for user information within the chat system. It includes
functionality for converting between the custom User dataclass
and the protobuf User object.
"""

from dataclasses import dataclass, asdict

from build import chat_pb2


@dataclass
class User:
    """A dataclass representing a user in the chat system."""
    login: str
    full_name: str

    def to_pb(self):
        """Convert User to protobuf object."""
        return chat_pb2.User(login=self.login, full_name=self.full_name)

    def to_dict(self) -> dict:
        """Convert the User instance into a dictionary"""
        return asdict(self)

    def get_unique_key(self) -> str:
        """Get unique key for the user."""
        return self.login

    @classmethod
    def from_pb(cls, pb_obj):
        """Create a User instance from a protobuf User object."""
        return cls(login=pb_obj.login, full_name=pb_obj.full_name)
