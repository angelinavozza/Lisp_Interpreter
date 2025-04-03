.PHONY: all run clean

all: run

run:
	python3 interpreter.py

clean:
	rm -rf __pycache__