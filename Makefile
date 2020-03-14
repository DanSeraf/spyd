PID :=  $(shell ps aux | grep 'main.py' | awk '{print $2}' | head -n 1)

all:
	PYTHONPATH=src python3 main.py --servdir ./src/spyd/data/
