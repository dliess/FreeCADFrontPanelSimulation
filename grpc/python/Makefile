INSTALL_DIR :="../../generated/python"
PROTO_PATH := ".."
PROTO_FILE := $(PROTO_PATH)/FPSimulation.proto

dep_all:
	mkdir -p "$(INSTALL_DIR)/.."
	mkdir -p "$(INSTALL_DIR)"
	touch $(INSTALL_DIR)/__init__.py
	touch $(INSTALL_DIR)/../__init__.py
	python -m grpc_tools.protoc -I$(PROTO_PATH)  --python_out="$(INSTALL_DIR)" --grpc_python_out="$(INSTALL_DIR)" "$(PROTO_FILE)" 
