include ../../../make.inc

test: pytest-and-write-output

generate:
	python -m grpc_tools.protoc \
		-Iapi/generated_proto=api/protos \
		--python_out=. \
		--grpc_python_out=. \
		api/protos/api.proto
