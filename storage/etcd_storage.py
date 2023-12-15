"""This script defines classes for User, Message and EtcdStorage,
providing serialization, deserialization and storage functionality
using etcd for User and Message objects.
"""

from abc import ABC, abstractmethod

import etcd3

from user import User
from message import Message
from build import chat_pb2


class AbstractStorage(ABC):
    """An abstract base class for storage mechanisms
    in the gRPC Chat application.
    """

    @abstractmethod
    def save_user(self, user: User) -> None:
        """Abstract method to save a User object to the storage."""
        pass

    @abstractmethod
    def get_user(self, login: str) -> User:
        """Abstract method to retrieve a User object
        from the storage by login.
        """
        pass

    @abstractmethod
    def save_message(self, message: Message) -> None:
        """Abstract method to save a Message object to the storage."""
        pass

    @abstractmethod
    def get_messages(self, to_user: str, since_timestamp: int) -> list:
        """Abstract method to retrieve a list
        of Message objects from the storage.
        """
        pass


class EtcdStorage(AbstractStorage):
    """Provides storage functionality using etcd
    for User and Message objects.
    """

    def __init__(self, host: str = "localhost", port: int = 2379):
        """Initializes the EtcdStorage with
        a connection to an etcd server.
        """
        self.etcd = etcd3.client(host, port)

    def create_users(self, users: list[User]) -> None:
        """Save multiple User objects to etcd."""
        for user in users:
            self.save_user(user)

    def save_user(self, user: User) -> None:
        """Save a User object to etcd."""
        user_key = f"user.{user.get_unique_key()}"
        self.etcd.put(user_key.encode(), user.to_pb().SerializeToString())

    def get_user(self, login: str) -> list | None:
        """Retrieve a User object from etcd based on the login."""
        user_key = f"user.{login}"
        user_data, _ = self.etcd.get(user_key.encode())
        return User(**user_data.decode()) if user_data else None

    def save_message(self, pb_message) -> None:
        """Saves a Message object to etcd."""
        message = Message.from_pb(pb_message)
        message_key = message.get_unique_key()
        serialized_message = message.to_pb().SerializeToString()
        self.etcd.put(message_key.encode(), serialized_message)

    def get_messages(self, to_user: str, since_timestamp: int = 0) -> list:
        """Retrieve Message objects from etcd based
        on recipient and optional timestamp.
        """
        messages = []
        for value, _ in self.etcd.get_prefix(f"message.{to_user}."):
            pb_message = chat_pb2.Message().FromString(value)
            message_data = Message.from_pb(pb_message)
            if message_data.timestamp > since_timestamp:
                messages.append(message_data)
        return messages

    def get_all_users(self):
        """Retrieve all users from etcd."""
        users = []
        for value, _ in self.etcd.get_prefix("user."):
            user_pb = chat_pb2.User().FromString(value)
            users.append(User.from_pb(user_pb))
        return users
