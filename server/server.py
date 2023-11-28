""" gRPC Chat Service Implementation.

This script defines the implementation of a gRPC Chat Service using the provided
protocol buffer messages and gRPC service definitions.

The server implements three RPC methods:
1. GetUsers: Get a list of users.
2. SendMessage: Send a chat message.
3. Subscribe: Subscribe to a stream of chat messages.

The server uses the ChatServiceServicer class to handle these methods.

To run the server, execute this script. The server will start on localhost:50052
by default. A client can customize the host and port by providing different values
to them.
"""

import grpc
from concurrent import futures
from build import chat_pb2, chat_pb2_grpc
from config import GRPC_HOST, GRPC_PORT


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Implementation of the gRPC ChatServiceServicer what provides
    the server-side logic for the gRPC chat service.
    """
    
    def __init__(self):
        """Initializes the ChatServiceServicer."""
        self.users = [chat_pb2.User(login="user1", full_name="John Wick"),
                      chat_pb2.User(login="user2", full_name="Johnny Depp")]

        self.messages = []

    def GetUsers(self, request, context):
        """Handles the GetUsers RPC call."""
        return chat_pb2.GetUsersReply(users=self.users)

    def SendMessage(self, request, context):
        """Handles the SendMessage RPC call."""
        self.messages.append(request.message)
        return chat_pb2.SendMessageReply()

    def Subscribe(self, request, context):
        """Handles the Subscribe RPC call."""
        user_login = request.login
        for message in self.messages:
            if message.to_user == user_login:
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
