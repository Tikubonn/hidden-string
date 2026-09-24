
export GCC=gcc
export CFLAGS=-O3 -fPIC -Wall
#export HIDDEN_STRING=
export PYTHON=py

.PHONY: build
build: bin/sample.exe

.PHONY: clean
clean:
	rm -f src/main.2.c
	rm -f src/main.2.o

.PHONY: run
run: build
	objdump -s -j .rdata src/main.2.o
	bin/sample.exe

src/main.2.c: src/main.c
	$(PYTHON) $(HIDDEN_STRING) -e utf-8 -o src/main.2.c src/main.c

src/main.2.o: src/main.2.c
	$(GCC) $(CFLAGS) -c -o src/main.2.o src/main.2.c

bin:
	mkdir -p bin

bin/sample.exe: src/main.2.o | bin
	$(GCC) $(CFLAGS) -o bin/sample.exe src/main.2.o
