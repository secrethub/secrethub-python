SHELL = bash
SWIG_VERSION = 4.0.2
CGO_FILES = Client.a Client.h
PYTHON_FILES = Client.py SecretHubXGOPINVOKE.py Secret.py SecretVersion.py
SWIG_FILES = secrethub_wrap.c
OUT_FILES = secrethub_wrap.o libSecretHubXGO.so SecretHubXGO.dll
XGO_DIR = ./secrethub-xgo
DEPS = secrethub_wrap.c Client.h
OBJ = secrethub_wrap.o Client.a

lib: client swig compile
	@echo "Library Ready ^-^"

lib-win: client-win swig compile-win
	@echo "Library Ready ^-^"

.PHONY: client-win
client-win: $(XGO_DIR)/secrethub_wrapper.go
	@echo "Making the C library from Go files (Windows)..."
	@cd $(XGO_DIR) && GOOS=windows GOARCH=amd64 CGO_ENABLED=1 go build -o ../Client.a -buildmode=c-archive secrethub_wrapper.go

.PHONY: compile-win
compile-win: $(DEPS)
	@echo "Compiling..."
	#@cl.exe /c /O2 secrethub_wrap.c /I C:\hostedtoolcache\windows\Python\3.8.6\x64\include /Fo secrethub_wrap.obj
	x86_64-w64-mingw32-gcc -c -O2 -fpic -o secrethub_wrap.obj -I C:\hostedtoolcache\windows\Python\3.8.6\x64\include secrethub_wrap.c
	#@cl.exe /LD -fPIC secrethub_wrap.obj Client.a /OUT:_secrethub.dll
	x86_64-w64-mingw32-gcc -shared -fPIC secrethub_wrap.obj Client.a -o _secrethub.dll

.PHONY: client
client: $(XGO_DIR)/secrethub_wrapper.go
	@echo "Making the C library from Go files (Linux)..."
	@cd $(XGO_DIR) && go build -o ../Client.a -buildmode=c-archive secrethub_wrapper.go

.PHONY: compile
compile: $(DEPS)
	@echo "Compiling..."
	@gcc -c -O2 -fpic -o secrethub_wrap.o -I/usr/include/python3.8 secrethub_wrap.c
	@gcc -shared -fPIC $(OBJ) -o _secrethub.so

.PHONY: swig
swig:
	@echo "Generating swig files..."
	@swig -python secrethub.i

.PHONY: clean
clean:
	@rm -f $(CGO_FILES) $(SWIG_FILES) $(OUT_FILES) $(addprefix test/, $(PYTHON_FILES))
	@rm -rf build bin obj test/bin test/obj
