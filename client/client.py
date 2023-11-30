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
    """Get a list of users from the chat server to the current user."""
    request = chat_pb2.GetUsersRequest()
    response = stub.GetUsers(request)
    print("List of users:")
    for user in response.users:
        print(f"{user.login}: {user.full_name}")


def send_message(stub, from_user, to_user, body):
    """Send a chat message from the current user to any user."""
    message = chat_pb2.Message(from_user=from_user, to_user=to_user, body=body)
    request = chat_pb2.SendMessageRequest(message=message)
    stub.SendMessage(request)
    print(f"Message sent from {from_user} to {to_user}: {body}")


def subscribe(stub, login):
    """Subscribe to a stream of chat messages and retrieve all
    messages for the current user.
    """
    request = chat_pb2.SubscribeRequest(login=login)
    messages = stub.Subscribe(request)
    print(f"Subscribed to messages for {login}. Waiting for messages...")
    for message in messages:
        print(
            f"Received message: {message.body} (from: {message.from_user},"
            f" to: {message.to_user})")


def build_parser():
    """Build arguments parser for the command-line options."""
    parser = argparse.ArgumentParser(description="gRPC Chat Client")
    parser.add_argument("--host", type=str, default="localhost",
                        help="Server host")
    parser.add_argument("--port", type=int, default=50052, help="Server port")
    parser.add_argument("--user", type=str, required=True, help="User login")
    return parser


def choose_action():
    """Display available actions and prompt the user for input."""
    print("Please choose what you want")
    print("1. Retrieve a list of users")
    print("2. Send a chat message")
    print("3. Subscribe to messages")
    choice = input("Please enter the number of your choice"
                   "or just something else to exit: ")
    return choice


def main():
    """Main function for the gRPC Chat Client."""
    parser = build_parser()
    args = parser.parse_args()

    channel = grpc.insecure_channel(f"{args.host}:{args.port}")
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    while True:
        action_choice = choose_action()

        match action_choice:
            case "1":
                get_users(stub)
            case "2":
                to_user = input("Enter the username to send a message to: ")
                body = input("Enter the message body: ")
                send_message(stub, args.user, to_user, body)
            case "3":
                subscribe(stub, args.user)
            case _:
                print("Exiting...")
                break


if __name__ == "__main__":
    main()
