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
    client.py --user user1 or -u user1

    # Specify custom server host and port
    client.py [--host or -H] localhost [--port or -p] 50053
    [--user or -u] [--action or -a] [--body or -b]

    client.py -H localhost -p 50053 -u user1 -a get_users
    client.py -u user1 -a send_message -t user2 -b "Hey"
    client.py -u user1 -a subscribe.
"""

import grpc
import argparse

from build import chat_pb2, chat_pb2_grpc


class InvalidDataError(Exception):
    """Generic exception class for invalid data in commands."""
    pass


def check_required_arguments(args, required_args):
    """Check if required arguments are present, raise error if not."""
    missing_args = [arg for arg in required_args if not getattr(args, arg)]
    if missing_args:
        raise InvalidDataError(
            f"Error: Missing required argument(s): {', '.join(missing_args)}.")


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
    print(f"Subscribed to messages for {login}.")
    for message in messages:
        print(
            f"Received message: {message.body} (from: {message.from_user},"
            f" to: {message.to_user})")


def build_parser():
    """Build arguments parser for the command-line options."""
    parser = argparse.ArgumentParser(description="gRPC Chat Client")
    parser.add_argument("-H", "--host", type=str,
                        default="localhost",
                        help="Server host (default: localhost)")

    parser.add_argument("-p", "--port", type=int, default=50053,
                        help="Server port (default: 50053)")

    parser.add_argument("-u", "--user", type=str,
                        help="User login for the chat (required)")

    parser.add_argument("-a", "--action", type=str, required=True,
                        choices=["get_users", "send_message", "subscribe"],
                        help="""Action to perform
                        get_users,
                        send_message,
                        subscribe.""")

    parser.add_argument("-t", "--to_user", type=str, default=None,
                        help="Receiving user for sending a message.")

    parser.add_argument("-b", "--body", type=str, default=None,
                        help="Message body for sending a message")

    return parser


def perform_action(stub, args):
    """Perform the action based on the provided
    command-line arguments.

    This function also checks for the required arguments for each
    action and raises custom exceptions if they are missing.
    """
    if args.action == "get_users":
        check_required_arguments(args, ["user"])
        get_users(stub)

    elif args.action == "send_message":
        check_required_arguments(args, ["user", "to_user", "body"])
        send_message(stub, args.user, args.to_user, args.body)

    elif args.action == "subscribe":
        check_required_arguments(args, ["user"])
        subscribe(stub, args.user)


def main():
    """Main function for the gRPC Chat Client."""
    parser = build_parser()
    args = parser.parse_args()

    with grpc.insecure_channel(f"{args.host}:{args.port}") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        perform_action(stub, args)


if __name__ == "__main__":
    main()
