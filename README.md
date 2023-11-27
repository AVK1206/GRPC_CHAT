# gRPC Chat Service - Server

This directory contains the server-side implementation of a gRPC Chat Service. The server provides three main functionalities: GetUsers, SendMessage, and Subscribe.

# Prerequisites

- Python 3
- gRPC
- Protocol Buffers

# Installation

1. Clone the repository:

    ```
    bash
    git clone https://github.com/AVK1206/GRPC_CHAT.git
    cd server
    ```

2. Install the required dependencies:

    ```
    bash
    pip install -r requirements.txt
    ```

# Usage

To run the server, execute the following script. The server will start on port 50052.

```
bash
python server.py
```

# Configuration

The gRPC server can be configured through the 'config.py' file, which contains the following constants:

- 'GRPC_CHAT_HOST': The host address for the gRPC server (default: "localhost").
- 'GRPC_CHAT_PORT': The port number for the gRPC server (default: 50052).

Adjust these values in the 'config.py' file to customize the server configuration to your specific requirements.
