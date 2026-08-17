.PHONY: help install test eval demo verify evidence screenshots

PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
export DEMO_AUTH ?= true
export BIND_HOST ?= 127.0.0.1
export OFFLINE_MODE ?= true
export STORE_RAW_MESSAGES ?= false

help:
	@echo "MindMend Empathy Anchor"
	@echo "  make install      Install Python dependencies"
	@echo "  make test         Run Node and Python tests"
	@echo "  make eval         Run the labeled detector harness"
	@echo "  make demo         Start the local showcase on 127.0.0.1:8000"
	@echo "  make verify       Tests + live /health /ready /scan checks"
	@echo "  make evidence     Regenerate docs/evidence from a live process"

install:
	$(PIP) install -r backend/requirements.txt

test:
	npm test
	DEMO_AUTH=true $(PYTHON) -m pytest backend/tests

eval:
	$(PYTHON) backend/eval/run_eval.py

demo:
	DEMO_AUTH=true BIND_HOST=127.0.0.1 OFFLINE_MODE=true $(PYTHON) backend/app.py

verify:
	chmod +x scripts/verify.sh scripts/capture-evidence.sh docker-entrypoint.sh
	./scripts/verify.sh

evidence:
	chmod +x scripts/verify.sh scripts/capture-evidence.sh docker-entrypoint.sh
	./scripts/capture-evidence.sh

screenshots:
	node scripts/capture-screenshots.mjs
