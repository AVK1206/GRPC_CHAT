# Source directory for protobuf files.
SRC_DIR := ./GRPC-CHAT-PROTOS/protos
# Build directory for generated Python files.
BUILD_DIR := ./build
# Protocol Buffer file to be compiled.
PROTO_FILE := $(SRC_DIR)/chat.proto

# Target to compile all protobuf files.
all: compile_proto

# Target to compile the specified protobuf file.
compile_proto:
	python -m grpc_tools.protoc -I$(SRC_DIR) --python_out=$(BUILD_DIR) --grpc_python_out=$(BUILD_DIR) $(PROTO_FILE)

# Target to clean up the build directory.
clean:
	rm -rf $(BUILD_DIR)
