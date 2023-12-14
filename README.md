A simple client-server chat application using gRPC in Python with Etcd3 for message storage. The server supports operations like retrieving a list of users, sending messages, and broadcasting new messages to subscribed clients.

# gRPC Chat Service - Server

This directory contains the server-side implementation of a gRPC Chat Service. The server provides three main functionalities: GetUsers, SendMessage, and Subscribe.

# Prerequisites

- Python 3
- gRPC
- Protocol Buffers
- etcd3

# Installation

1. Clone the repository:

    ```
    git clone https://github.com/AVK1206/GRPC_CHAT.git
    cd server
    ```
    
2. Initialize and update the submodule:

   ```
   git submodule update --init --recursive
   ```
   
3. Create a Virtual Environment:
   
   ```
   python3 -m venv venv
   ```
   
4. Activate the Virtual Environment:
   
   ```
   source venv/bin/activate
   ```

5. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```
   
# Usage

1. Run the server:

   ```
   python3 server.py
   ```

2. Open a new terminal window, activate the virtual environment, and run the client:
   
   ```
   source venv/bin/activate
   cd client
   python3 client.py --user <username> --action <action: 
   Retrieve a list of users,
   Send a message,
   Subscribe to messages.>
   ```
   
3. Retrieve a list of users:
   
   ```
   python3 client.py --user <username> --action get_users or
   python3 client.py --u <username> --a get_users
   ```
   
4. Send a message from one user to another:
   
   ```
   python3 client.py --user <from_user> --action send_message --to_user <to_user> --body "Your message here" or
   python3 client.py -u <from_user> -a send_message -t <to_user> -b "Your message here" 
   ```
   
5. Subscribe to messages for a user:
   
   ```
   python3 client.py --user <username> --action subscribe or 
   python3 client.py -u <username> -a subscribe
   ```
   
# Configuration

The gRPC server can be configured through the 'config.py' file, which contains the following constants:

- 'GRPC_CHAT_HOST': The host address for the gRPC server (default: "localhost").
- 'GRPC_CHAT_PORT': The port number for the gRPC server (default: 50053).

Adjust these values in the 'config.py' file to customize the server configuration to your specific requirements.

The gRPC client can be configured through command-line options in the client.py script. The available options are:

- '--host or -H': The host address for the gRPC server (default: "localhost").
- '--port or -p': The port number for the gRPC server (default: 50053).
- '--user or -u': The user login for the chat client (required).
- '--action or -a': The action to perform, available options are "get_users", "send_message", and "subscribe".
- '--to_user or -t': Who sends the message.
- '--body or -b':The message.


# License
This gRPC Chat application is distributed under the MIT License. See the LICENSE file for more details.
