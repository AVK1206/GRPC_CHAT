"""
Run the gRPC chat client.

This function initializes a gRPC channel and stub, performs various chat-related actions,
such as retrieving the user list, sending messages, and getting chat messages.

The client actions include:
- Retrieving the user list from the gRPC server.
- Sending multiple chat messages from different users.
- Getting a specified number of chat messages from the server.
- Subscribing to a continuous stream of new chat messages.

The function is intended to be called when executing the client script.

Attributes:
    channel: The gRPC channel to communicate with the gRPC server.
    stub: The gRPC stub for making remote procedure calls (RPCs) to the server.

Methods:
    get_user_list: Retrieves the user list from the gRPC server and prints it.
    send_message: Sends a chat message to the gRPC server and prints a success message.
    get_chat_messages: Retrieves a specified number of chat messages from the gRPC server and prints them.
    subscribe_to_messages: Subscribes to a continuous stream of new chat messages and prints them.

"""
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor, as_completed

from build import chat_pb2
from build import chat_pb2_grpc
import itertools
import time
import grpc


def get_user_list(stub):
    """
    Get a list of users from the server.

    Args:
        stub: The gRPC stub.

    Returns:
        None
    """
    user_list_request = chat_pb2.UserListRequest()
    user_list_response = stub.GetUserList(user_list_request)
    print("User List:")
    for user in user_list_response.users:
        print(f"  {user.login}: {user.full_name}")


def send_message(stub, from_user, to_user, body):
    """
    Send a chat message to the server.

    Args:
        stub: The gRPC stub.
        from_user: The sender's username.
        to_user: The recipient's username.
        body: The message body.

    Returns:
        None
    """
    request = chat_pb2.MessageRequest(
        from_user=from_user,
        to_user=to_user,
        timestamp=int(time.time()),
        body=body
    )
    stub.SendMessage(request)
    print("Message sent successfully!")


def get_chat_messages(stub, num_messages=1):
    """
    Get a stream of chat messages from the server.

    Args:
        stub: The gRPC stub.
        num_messages: The number of messages to retrieve.

    Returns:
        A list of GetMessageReply messages.
    """
    request = chat_pb2.GetMessageRequest()
    messages = stub.GetMessages(request)

    received_messages = []
    for message in itertools.islice(messages, num_messages):
        received_messages.append(message)

    print(f"Received first {num_messages} chat messages:")
    for message in received_messages:
        print(f"From: {message.from_user}, To: {message.to_user}, Message: {message.body}")

    return received_messages


# def subscribe_to_messages(stub):
#     """
#     Subscribe to a stream of new chat messages from the server.
#
#     Args:
#         stub: The gRPC stub.
#
#     Returns:
#         None
#     """
#     request = chat_pb2.SubscribeRequest()
#     try:
#         for response in stub.Subscribe(request):
#             for message in response.messages:
#                 print(f"Received message: From {message.from_user}, To {message.to_user}, Message: {message.body}")
#     except grpc._channel._Rendezvous as err:
#         print(f"Error during subscription: {err}")


def run():
    """Main function to run the gRPC chat client."""
    channel = grpc.insecure_channel('localhost:50052')
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    get_user_list(stub)
    send_message(stub, "user1", "user2", "Hello from user1!")
    send_message(stub, "user2", "user3", "Hello from user2!")
    send_message(stub, "user3", "user4", "Hello from user2!")
    send_message(stub, "user4", "user5", "Hello from user2!")
    get_chat_messages(stub, num_messages=3)

    # with futures.ThreadPoolExecutor() as executor:
    #     subscribe_future = executor.submit(subscribe_to_messages, stub)
    #     send_message(stub, "user1", "user2", "Hello from user1!")
    #     for future in as_completed([subscribe_future]):
    #         try:
    #             future.result()
    #         except Exception as e:
    #             print(f"Error in task: {e}")


if __name__ == '__main__':
    run()
