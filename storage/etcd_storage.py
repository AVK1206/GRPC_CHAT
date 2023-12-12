"""This script defines classes for User, Message and EtcdStorage,
providing serialization, deserialization and storage functionality
using etcd for User and Message objects.
"""

from datetime import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
import json
import random

from langdetect import detect, lang_detect_exception
import emoji
import etcd3


class Serializable(ABC):
    """Abstract base class for objects that can be serialized to
    and deserialized from JSON.
    """

    @abstractmethod
    def to_json(self) -> json:
        """Convert the object to a JSON-formatted string."""
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, json_str: json):
        """Create an instance of the class from
        a JSON-formatted string.
        """
        pass


@dataclass
class User(Serializable):
    """Represents a user with login and full name, providing methods
    for serialization, deserialization, nickname generation
    and initials extraction.
    """
    login: str
    full_name: str

    def to_json(self) -> json:
        """Convert the user object to a JSON-formatted string."""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: json) -> "User":
        """Create a User instance from a JSON-formatted string."""
        return cls(**json.loads(json_str))

    def get_initials(self) -> str:
        """Get the initials of the user's full name."""
        return "".join(
            f"{word[0].upper()}." for word in self.full_name.split())

    def generate_nickname(self, length: int = 3) -> str:
        """Generate a nickname based on the user's full name."""
        return "".join(f"{word[:length]}" for word in self.full_name.split())

    def generate_nickname_with_emoji(self, length: int = 3) -> str:
        """Generate a nickname with a random emoji from emoji_keys
        based on the user's full name.
        """
        nickname = self.generate_nickname(length)

        emoji_keys = ["clapping_hands", "crown", "fire", "glowing_star",
                      "ninja", "rocket", "star", "thumbs_up", ]

        random_emoji = emoji.emojize(f":{random.choice(emoji_keys)}:")
        return f"{nickname}{random_emoji}"


@dataclass
class Message(Serializable):
    """Represents a message with sender, recipient, body and timestamp
    providing methods for serialization, deserialization,
    message length, language detection and filtering.
    """
    from_user: str
    to_user: str
    body: str
    timestamp: dt

    def to_json(self) -> json:
        """Convert the message object to a JSON-formatted string."""
        data = asdict(self)
        data["timestamp"] = str(self.timestamp)
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        """Create a Message instance from a JSON-formatted string."""
        data = json.loads(json_str)
        return cls(**data)

    def message_length(self) -> int:
        """Return the length of the message body."""
        return len(self.body)

    @classmethod
    def filter_messages(cls, messages, keyword: str) -> list["Message"]:
        """Filter a list of messages based on a keyword
        in the message body.
        """
        return [message for message in messages if keyword in message.body]

    def detect_language(self) -> str:
        """Detect the language of the message."""
        try:
            language = detect(self.body)
            return language
        except lang_detect_exception.LangDetectException as error:
            return f"Unknown language {error}"


@dataclass
class EtcdStorage:
    """Provides storage functionality using etcd
    for User and Message objects.
    """
    host: str = "localhost"
    port: int = 2379
    etcd: etcd3.client = etcd3.client(host=host, port=port)

    def save_user(self, user: User) -> None:
        """Save a User object to etcd."""
        key = f"users.{user.login}"
        value = user.to_json()
        self.etcd.put(key.encode(), value.encode())

    def get_user(self, login: str) -> User | None:
        """Retrieve a User object from etcd based on the login."""
        key = f"users.{login}"
        data, _ = self.etcd.get(key.encode())
        return User.from_json(data.decode()) if data else None

    def save_message(self, message: Message) -> None:
        """Save a Message object to etcd."""
        key = f"messages.{message.from_user}.{message.to_user}"
        value = message.to_json()
        self.etcd.put(key.encode(), value.encode())

    def get_message(self, from_user: str, to_user: str) -> Message | None:
        """Retrieve a Message object from etcd
        based on sender and recipient.
        """
        key = f"messages.{from_user}.{to_user}"
        data, _ = self.etcd.get(key.encode())
        return Message.from_json(data.decode()) if data else None
