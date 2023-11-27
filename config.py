""" gRPC Chat Service Configuration.

This module sets up the configuration for the gRPC Chat Service.
It defines constants for the gRPC server host and port based on
environment variables. If the environment
variables are not set, default values are used.

Constants:
    GRPC_HOST (str): The gRPC server host, defaulting to "localhost".
    GRPC_PORT (int): The gRPC server port, defaulting to 50052.
"""

import os

GRPC_HOST = os.environ.get("GRPC_CHAT_HOST", "localhost")
GRPC_PORT = int(os.environ.get("GRPC_CHAT_PORT", 50052))

