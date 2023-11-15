SRC_DIR := ./protos
BUILD_DIR := ./build

PROTO_FILE := $(SRC_DIR)/chat.proto

all: compile_proto

compile_proto:
	python -m grpc_tools.protoc -I$(SRC_DIR) --python_out=$(BUILD_DIR) --grpc_python_out=$(BUILD_DIR) $(PROTO_FILE)

clean:
	rm -rf $(BUILD_DIR)
