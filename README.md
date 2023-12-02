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

2. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

# Usage

To run the server, execute the following script. The server will start on port 50052.

```
python server.py
```

To run the client, use the following script. Make sure to replace `<username>` with the desired username:
```
python client.py --user <username>
```

# Configuration

The gRPC server and etcd can be configured through the 'config.py' file, which contains the following constants:

- 'GRPC_CHAT_HOST': The host address for the gRPC server (default: "localhost").
- 'GRPC_CHAT_PORT': The port number for the gRPC server (default: 50052).
- 'ETCD_HOST': The etcd server host (default: "localhost").
- 'ETCD_PORT': The etcd server port (default: 2379).

Adjust these values in the 'config.py' file to customize the server configuration to your specific requirements.

The gRPC client can be configured through command-line options in the client.py script. The available options are:

- '--host': The host address for the gRPC server (default: "localhost").
- '--port': The port number for the gRPC server (default: 50052).
- '--user': The user login for the chat client (required).

Adjust these values as needed to customize the client configuration.

# License
This gRPC Chat application is distributed under the MIT License. See the LICENSE file for more details.
