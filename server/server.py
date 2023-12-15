""" gRPC Chat Service Implementation.

This script defines the implementation of a gRPC Chat Service using
the provided protocol buffer messages and gRPC service definitions.

The server implements three RPC methods:
1. GetUsers: Get a list of users.
2. SendMessage: Send a chat message.
3. Subscribe: Subscribe to a stream of chat messages.

The server uses the ChatServiceServicer class to handle these methods.

To run the server, execute this script. The server will start
on localhost:50053 by default. A client can customize
the host and port by providing different values to them.
"""

from concurrent import futures

import grpc

from build import chat_pb2, chat_pb2_grpc
from config import GRPC_HOST, GRPC_PORT
from storage.etcd_storage import EtcdStorage


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Implementation of the gRPC ChatServiceServicer what provides
    the server-side logic for the gRPC chat service.
    """

    def __init__(self):
        """Initializes the ChatServiceServicer with
        an EtcdStorage instance.
        """
        self.storage = EtcdStorage()

    def GetUsers(self, request, context):
        """Handles the GetUsers RPC call
        retrieving all users from storage.
        """
        users = [user.to_pb() for user in self.storage.get_all_users()]
        return chat_pb2.GetUsersReply(users=users)

    def SendMessage(self, request, context):
        """Handles the SendMessage RPC call
        storing the sent message in etcd.
        """
        self.storage.save_message(request.message)
        return chat_pb2.SendMessageReply()

    def Subscribe(self, request, context):
        """Handles the Subscribe RPC call
        streaming messages to the user.
        """
        user_login = request.login
        storage = EtcdStorage()
        all_messages = storage.get_messages(user_login)
        for message in all_messages:
            yield message.to_pb()

        last_sent_timestamp = all_messages[-1].timestamp if all_messages else 0
        while context.is_active():
            new_messages = storage.get_messages(user_login,
                                                last_sent_timestamp)
            for message in new_messages:
                yield message.to_pb()
                last_sent_timestamp = message.timestamp


def serve(host, port):
    """Starts the gRPC server for the chat service."""
    print(f"Starting server on {host}:{port}...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(),
                                                    server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    try:
        print("Server started. Waiting for termination...")
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped.")


if __name__ == "__main__":
    serve(GRPC_HOST, GRPC_PORT)
