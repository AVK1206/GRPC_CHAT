"""gRPC Chat Service Implementation.

This script defines the implementation of a gRPC Chat Service using
the provided protocol buffer messages and gRPC service definitions.

The server implements three RPC methods:
1. GetUsers: Get a list of users.
2. SendMessage: Send a chat message.
3. Subscribe: Subscribe to a stream of chat messages.

The server uses the ChatServiceServicer class to handle these methods.
Messages are stored in etcd for persistence.

To run the server, execute this script. The server will start
on localhost:50053 by default. A client can customize
the host and port by providing different values to them.
"""

import grpc
import etcd3
from concurrent import futures

from build import chat_pb2, chat_pb2_grpc
from config import GRPC_HOST, GRPC_PORT, ETCD_HOST, ETCD_PORT


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Implementation of the gRPC ChatServiceServicer what provides
    the server-side logic for the gRPC chat service.
    """

    def __init__(self):
        """Initializes the ChatServiceServicer."""
        self.users = [chat_pb2.User(login="user1", full_name="John Wick"),
                      chat_pb2.User(login="user2", full_name="Johnny Depp")]

        self.etcd_client = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)

    def GetUsers(self, request, context):
        """Handles the GetUsers RPC call to the current user
        and returns all users' login and full name.
        """
        return chat_pb2.GetUsersReply(users=self.users)

    def SendMessage(self, request, context):
        """Handles the SendMessage RPC call to the current user
        and stores messages from him in etcd.
        """
        key = f"messages/{request.message.from_user}/{request.message.to_user}"
        value = request.message.body
        self.etcd_client.put(key, value)
        return chat_pb2.SendMessageReply()

    def Subscribe(self, request, context):
        """Handles the Subscribe RPC call to the current user
        and retrieves messages for him from etcd.
        """
        user_login = request.login
        prefix = f"messages/{user_login}/"
        for key, value in self.etcd_client.get_prefix(prefix):
            message = chat_pb2.Message(
                from_user=user_login,
                to_user=key.split("/")[-1],
                body=value
            )
            yield message


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
