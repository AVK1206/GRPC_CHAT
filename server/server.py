"""
gRPC Chat Service Implementation.

This module defines the implementation of a gRPC Chat Service using the provided
protocol buffer messages and gRPC service definitions.

The ChatServiceServicer class implements the gRPC service methods for user list retrieval,
sending messages, getting messages, and subscribing to new messages.

Attributes:
    message_queue (list): A list to store chat messages.
    message_condition (threading.Condition): A condition variable to synchronize access to the message queue.
    MAX_QUEUE_SIZE (int): The maximum size of the message queue.

Methods:
    GetUserList: Implements the GetUserList gRPC method to provide a list of users.
    SendMessage: Implements the SendMessage gRPC method to add a message to the queue.
    GetMessages: Implements the GetMessages gRPC method to retrieve and clear messages from the queue.
    Subscribe: Implements the Subscribe gRPC method to continuously yield new messages to subscribers.
    serve: Initializes and starts the gRPC server.
"""

from concurrent import futures
from build import chat_pb2
from build import chat_pb2_grpc
from threading import Condition
import grpc
import time

message_queue = []
message_condition = Condition()
MAX_QUEUE_SIZE = 10


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def GetUserList(self, request, context):
        """
        Get a list of users.

        Args:
            request: The request message containing user list retrieval parameters.
            context: The context of the gRPC service call.

        Returns:
            The reply message containing a list of users.

        """
        users = [
            chat_pb2.User(login="user1", full_name="John Wick"),
            chat_pb2.User(login="user2", full_name="Johnny Depp"),
        ]
        user_list = chat_pb2.UserListReply(users=users)
        return user_list

    def SendMessage(self, request, context):
        """
         Send a chat message.

        Args:
            request: The request message containing the chat message details.
            context: The context of the gRPC service call.

        Returns:
            The empty reply message indicating a successful message send.
        """
        with message_condition:
            # Add the message to the queue.
            message_queue.append(request)

            # Ensure the queue size does not exceed the maximum.
            if len(message_queue) > MAX_QUEUE_SIZE:
                message_queue.pop(0)

            message_condition.notify_all()
        return chat_pb2.MessageReply()

    def GetMessages(self, request, context):
        """
        Get a stream of chat messages.

        Args:
            request: The request message containing parameters for message retrieval.
            context: The context of the gRPC service call.

        Returns:
            A stream of reply messages containing chat messages.
        """
        with message_condition:
            # Wait for messages if the queue is empty
            while not message_queue:
                message_condition.wait()

            # Retrieve and clear the messages from the queue
            messages = message_queue[:]
            del message_queue[:]

        reply_messages = []
        for message in messages:
            reply_messages.append(chat_pb2.GetMessageReply(
                from_user=message.from_user,
                to_user=message.to_user,
                timestamp=int(time.time()),
                body=message.body
            ))

        yield reply_messages

    # def Subscribe(self, request, context):
    #     """
    #     Subscribe to a stream of chat messages.
    #
    #     Args:
    #         request: The request message for initiating a subscription.
    #         context: The context of the gRPC service call.
    #
    #     Returns:
    #         A stream of reply messages containing chat messages.
    #     """
    #     try:
    #         while True:
    #             with message_condition:
    #                 # Wait for messages if the queue is empty
    #                 while not message_queue:
    #                     message_condition.wait()
    #
    #                 # Retrieve and clear the messages from the queue
    #                 messages = message_queue[:]
    #                 del message_queue[:]
    #
    #             yield chat_pb2.SubscribeReply(messages=messages)
    #     except grpc.RpcError as error:
    #         print(f"Subscription terminated: {error}")


def serve():
    """Start the gRPC server. Initializes and starts the gRPC server with the ChatServiceServicer."""
    print("Starting server on port 50052...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("localhost:50052")
    server.start()
    print("Server started. Waiting for termination...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
