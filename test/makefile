
export GCC=gcc
export CFLAGS=-Og -g -fPIC -Wall -Iinclude
#export HIDDEN_STRING=

.PHONY: build
build: bin/test.exe

.PHONY: clean
clean:
	rm -f src/testsuite.2.c
	rm -f src/testsuite.2.o
	rm -f src/external-string.2.c
	rm -f src/external-string.2.o
	rm -f src/external-string2.2.c
	rm -f src/external-string2.2.o
	rm -f src/testsuite-multiple-files.o
	rm -f src/main.o

.PHONY: run
run: build
	gdb bin/test.exe

src/testsuite.2.c: src/testsuite.c
	python $(HIDDEN_STRING) -o src/testsuite.2.c src/testsuite.c

src/testsuite.2.o: src/testsuite.2.c
	$(GCC) $(CFLAGS) -c -o src/testsuite.2.o src/testsuite.2.c

src/external-string.2.c: src/external-string.c
	python $(HIDDEN_STRING) -o src/external-string.2.c src/external-string.c

src/external-string.2.o: src/external-string.2.c
	$(GCC) $(CFLAGS) -c -o src/external-string.2.o src/external-string.2.c

src/external-string2.2.c: src/external-string2.c
	python $(HIDDEN_STRING) -o src/external-string2.2.c src/external-string2.c

src/external-string2.2.o: src/external-string2.2.c
	$(GCC) $(CFLAGS) -c -o src/external-string2.2.o src/external-string2.2.c

src/testsuite-multiple-files.o: src/testsuite-multiple-files.c
	$(GCC) $(CFLAGS) -c -o src/testsuite-multiple-files.o src/testsuite-multiple-files.c

src/main.o: src/main.c
	$(GCC) $(CFLAGS) -c -o src/main.o src/main.c

bin:
	mkdir -p bin

bin/test.exe: src/testsuite.2.o src/external-string.2.o src/external-string2.2.o src/testsuite-multiple-files.o src/main.o | bin
	$(GCC) $(CFLAGS) -o bin/test.exe src/testsuite.2.o src/external-string.2.o src/external-string2.2.o src/testsuite-multiple-files.o src/main.o
