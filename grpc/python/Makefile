INSTALL_DIR :="../../generated/python"
PROTO_PATH := ".."
PROTO_INSTALL_PATH := "/usr/share/freecad-daily/Mod/FrontPanelSimulation"
PROTO_FILE := $(PROTO_PATH)/FPSimulation.proto

dep_all:
	mkdir -p "$(INSTALL_DIR)/.."
	mkdir -p "$(INSTALL_DIR)"
	touch $(INSTALL_DIR)/__init__.py
	touch $(INSTALL_DIR)/../__init__.py
	python3 -m grpc_tools.protoc -I$(PROTO_PATH)  --python_out="$(INSTALL_DIR)" --grpc_python_out="$(INSTALL_DIR)" "$(PROTO_FILE)" 

install:
	mkdir -p "$(PROTO_INSTALL_PATH)"
	cp "$(PROTO_FILE)" "$(PROTO_INSTALL_PATH)"
