from dataclasses import dataclass, asdict
from datetime import datetime as dt
import etcd3


@dataclass
class User:
    login: str
    full_name: str


@dataclass
class Message:
    from_user: str
    to_user: str
    body: str
    timestamp: dt


@dataclass
class EtcdStorage:
    host: str = "localhost"
    port: int = 2379
    etcd: etcd3.client = etcd3.client(host=host, port=port)

    def save_user(self, user: User) -> None:
        key = f"users.{user.login}"
        value = str(asdict(user))
        self.etcd.put(key.encode(), value.encode())

    def get_user(self, login: str) -> User | None:
        key = f"users.{login}"
        data, _ = self.etcd.get(key.encode())
        user_result = None
        if data:
            user_result = User(**eval(data.decode()))
        return user_result

    def save_message(self, message: Message) -> None:
        key = f"messages.{message.from_user}.{message.to_user}"
        message.timestamp = str(message.timestamp)
        value = str(asdict(message))
        self.etcd.put(key.encode(), value.encode())

    def get_message(self, from_user: str, to_user: str) -> Message | None:
        key = f"messages.{from_user}.{to_user}"
        data, _ = self.etcd.get(key.encode())
        message_result = None
        if data:
            message_result = Message(**eval(data.decode()))
        return message_result


if __name__ == "__main__":
    user1 = User("user1", "John Wick")
    user2 = User("user2", "Johnny Depp")
    message1 = Message("user1", "user2", "Hey from John Wick", dt.now())
    message2 = Message("user2", "user1", "Hey from Johnny Depp", dt.now())

    storage = EtcdStorage()

    storage.save_user(user1)
    storage.save_user(user2)

    storage.save_message(message1)
    storage.save_message(message2)

    receive_user1 = storage.get_user("user1")
    receive_user2 = storage.get_user("user2")

    receive_message1 = storage.get_message("user1", "user2")
    receive_message2 = storage.get_message("user2", "user1")

    print(receive_user1, receive_user2, sep="\n")
    print(receive_message1, receive_message2, sep="\n")
