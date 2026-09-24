
.PHONY: sample
sample:
	make -C sample run HIDDEN_STRING=$(CURDIR)/hidden-string.py

.PHONY: clean
clean:
	make -C sample clean
	make -C test clean

.PHONY: test
test:
	make -C test run HIDDEN_STRING=$(CURDIR)/hidden-string.py
