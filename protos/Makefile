GENERATED_DIR := "../generated"

dep_all:
	mkdir -p $(GENERATED_DIR)
	touch $(GENERATED_DIR)/__init__.py
	python -m grpc_tools.protoc -I.  --python_out=$(GENERATED_DIR) --grpc_python_out=$(GENERATED_DIR) FPSimulation.proto
