INSTALL_DIR :="../../generated/python"
PROTO_PATH := ".."
PROTO_INSTALL_PATH := "/usr/share/freecad-daily/Mod/FrontPanelSimulation"
PROTO_FILE := $(PROTO_PATH)/FPSimulation.proto

dep_all:
	mkdir -p "$(INSTALL_DIR)/.."
	mkdir -p "$(INSTALL_DIR)"
	python3 -m grpc_tools.protoc -I$(PROTO_PATH)  --python_out="$(INSTALL_DIR)" --grpc_python_out="$(INSTALL_DIR)" "$(PROTO_FILE)"
	sed -i "s/import FPSimulation_pb2 as FPSimulation__pb2/from . import FPSimulation_pb2 as FPSimulation__pb2/" $(INSTALL_DIR)/FPSimulation_pb2_grpc.py

install:
	mkdir -p "$(PROTO_INSTALL_PATH)"
	cp "$(PROTO_FILE)" "$(PROTO_INSTALL_PATH)"
