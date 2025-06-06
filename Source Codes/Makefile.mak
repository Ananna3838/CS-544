# Makefile for QUIC Chat Project

PYTHON := python3
SERVER := server.py
CLIENT := client.py
PORT := 8888
IP := 127.0.0.1

run-server:
	@echo "Starting server on port $(PORT)..."
	$(PYTHON) $(SERVER) --port $(PORT)

run-client:
	@echo "Starting client and connecting to $(IP):$(PORT)..."
	$(PYTHON) $(CLIENT) --ip $(IP) --port $(PORT)
