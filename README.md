# GRPC_CHAT

A simple client-server chat application using gRPC in Python with Etcd3 for message storage.
The server supports operations like retrieving a list of users, sending messages, and broadcasting new messages
to subscribed clients.

Compile the protocol buffers with the provided Makefile using command "make" in terminal.
To clean up compiled files use command "make clean" in terminal.

Ensure you have gRPC tools installed use command "pip install -r requirements.txt".
