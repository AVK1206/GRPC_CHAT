"""gRPC Chat Service Configuration.

This module defines constants for configuring the gRPC Chat Service.
It sets up environment variables to customize the gRPC server
host and port, as well as the etcd host and port for message storage.
If the environment variables are not set, default values are used.

Constants:
    GRPC_HOST (str): The gRPC server host, defaulting to "localhost".
    GRPC_PORT (int): The gRPC server port, defaulting to 50053.
    ETCD_HOST (str): The etcd server host, defaulting to "localhost".
    ETCD_PORT (int): The etcd server port, defaulting to 2379.
"""

import os


GRPC_HOST = os.environ.get("GRPC_CHAT_HOST", "localhost")
GRPC_PORT = int(os.environ.get("GRPC_CHAT_PORT", 50053))

ETCD_HOST = os.environ.get("ETCD_HOST", "localhost")
ETCD_PORT = int(os.environ.get("ETCD_PORT", 2379))
