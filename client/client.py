"""gRPC Chat Client Implementation.

This script provides a simple command-line interface
for interacting with a gRPC-based chat server.

It allows users to perform the following actions:
1. Retrieve a list of users from the chat server.
2. Send chat messages to other users on the server.
3. Subscribe to a stream of incoming chat messages.

Usage:
    client.py [--host HOST] [--port PORT] --user USER

Examples:
    # Run the client with default settings
    client.py --user user1

    # Specify custom server host and port
    client.py --host localhost --port 50051 --user user2
"""

import grpc
import argparse

from build import chat_pb2, chat_pb2_grpc


def get_users(stub):
    """Get a list of users."""
    request = chat_pb2.GetUsersRequest()
    response = stub.GetUsers(request)
    print("List of users:")
    for user in response.users:
        print(f"{user.login}: {user.full_name}")


def send_message(stub, from_user, to_user, body):
    """Send a chat message."""
    message = chat_pb2.Message(from_user=from_user, to_user=to_user, body=body)
    request = chat_pb2.SendMessageRequest(message=message)
    stub.SendMessage(request)
    print(f"Message sent from {from_user} to {to_user}: {body}")


def subscribe(stub, login):
    """Subscribe to a stream of chat messages."""
    request = chat_pb2.SubscribeRequest(login=login)
    messages = stub.Subscribe(request)
    print(f"Subscribed to messages for {login}. Waiting for messages...")
    for message in messages:
        print(
            f"Received message: {message.body} (from: {message.from_user},"
            f" to: {message.to_user})")


def main():
    """Main function for the gRPC Chat Client."""
    parser = argparse.ArgumentParser(description="gRPC Chat Client")
    parser.add_argument("--host", type=str, default="localhost",
                        help="Server host")
    parser.add_argument("--port", type=int, default=50052, help="Server port")
    parser.add_argument("--user", type=str, required=True, help="User login")

    args = parser.parse_args()

    channel = grpc.insecure_channel(f"{args.host}:{args.port}")
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    get_users(stub)

    to_user = input("Enter the username to send a message to: ")
    body = input("Enter the message body: ")
    send_message(stub, args.user, to_user, body)

    subscribe(stub, args.user)

    while True:
        to_user = input(
            "Enter username to send a message to (or press Enter to exit): ")
        if not to_user:
            break

        body = input("Enter the message body: ")
        send_message(stub, args.user, to_user, body)

        for message in stub.Subscribe(
                chat_pb2.SubscribeRequest(login=args.user)):
            print(
                f"Received message: {message.body} (from: {message.from_user},"
                f" to: {message.to_user})")


if __name__ == "__main__":
    main()
