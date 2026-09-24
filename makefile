
.PHONY: sample
sample:
	make -C sample run HIDDEN_STRING=$(CURDIR)/hidden-string.py

.PHONY: clean
clean:
	make -C sample clean
