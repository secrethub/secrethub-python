SHELL = bash
SWIG_VERSION = 4.0.2
CGO_FILES = Client.a Client.h
PYTHON_FILES = Client.py SecretHubXGOPINVOKE.py Secret.py SecretVersion.py
SWIG_FILES = secrethub_wrap.c
OUT_FILES = secrethub_wrap.o libSecretHubXGO.so SecretHubXGO.dll
XGO_DIR = ./secrethub-xgo
DEPS = secrethub_wrap.c Client.h
OBJ = secrethub_wrap.o Client.a
OS_VAR = $(shell uname -s | tr A-Z a-z)

lib: client swig compile
	@echo "Library Ready ^-^"

ifeq ($(OS_VAR), Windows_NT)
.PHONY: client
client: $(XGO_DIR)/secrethub_wrapper.go
	@echo "Making the C library from Go files (Windows)..."
	@cd $(XGO_DIR) && GOOS=windows GOARCH=amd64 CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc go build -o ../Client.a -buildmode=c-archive secrethub_wrapper.go

.PHONY: compile
compile: $(DEPS)
	@echo "Compiling..."
	@x86_64-w64-mingw32-gcc -c -O2 -fpic -o secrethub_wrap.o secrethub_wrap.c
	@x86_64-w64-mingw32-gcc -shared -fPIC $(OBJ) -o _SecretHub.dll
else
.PHONY: client
client: $(XGO_DIR)/secrethub_wrapper.go
	@echo "Making the C library from Go files (Linux)..."
	@cd $(XGO_DIR) && go build -o ../Client.a -buildmode=c-archive secrethub_wrapper.go

.PHONY: compile
compile: $(DEPS)
	@echo "Compiling..."
	@gcc -c -O2 -fpic -o secrethub_wrap.o -I/usr/include/python3.8 secrethub_wrap.c
	@gcc -shared -fPIC $(OBJ) -o _secrethub.so
endif

.PHONY: swig
swig:
	@echo "Generating swig files..."
	@swig -python secrethub.i

.PHONY: clean
clean:
	@rm -f $(CGO_FILES) $(SWIG_FILES) $(OUT_FILES) $(addprefix test/, $(PYTHON_FILES))
	@rm -rf build bin obj test/bin test/obj
