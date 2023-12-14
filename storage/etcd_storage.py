"""This script defines classes for User, Message and EtcdStorage,
providing serialization, deserialization and storage functionality
using etcd for User and Message objects.
"""

from abc import ABC, abstractmethod

import etcd3

from user import User
from message import Message


class AbstractStorage(ABC):

    @abstractmethod
    def save_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user(self, login: str) -> User:
        pass

    @abstractmethod
    def save_message(self, message: Message) -> None:
        pass

    @abstractmethod
    def get_message(self, unique_key: str) -> Message:
        pass


class EtcdStorage(AbstractStorage):
    """Provides storage functionality using etcd
    for User and Message objects.
    """

    def __init__(self, host: str = "localhost", port: int = 2379):
        self.etcd = etcd3.client(host, port)

    def save_user(self, user: User) -> None:
        """Save a User object to etcd."""
        user_key = f"user.{user.get_unique_key()}"
        self.etcd.put(user_key.encode(), user.to_dict().encode())

    def get_user(self, login: str) -> User | None:
        """Retrieve a User object from etcd based on the login."""
        user_key = f"user.{login}"
        user_data, _ = self.etcd.get(user_key.encode())
        return User(**user_data.decode()) if user_data else None

    def save_message(self, message: Message) -> None:
        """Save a Message object to etcd."""
        message_key = f"message.{message.get_unique_key()}"
        self.etcd.put(message_key.encode(), message.to_dict().encode())

    def get_message(self, unique_key: str) -> Message | None:
        """Retrieve a Message object from etcd
        based on sender and recipient.
        """
        message_key = f"message.{unique_key}"
        message_data, _ = self.etcd.get(message_key.encode())
        return Message(**message_data.decode()) if message_data else None
