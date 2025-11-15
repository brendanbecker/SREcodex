DOTCODEX_DIR ?= ../dotcodex
INSTALL_CMD := DOTCODEX_DIR=$(DOTCODEX_DIR) bash scripts/install-skills.sh
LIST_CMD    := DOTCODEX_DIR=$(DOTCODEX_DIR) codex-skills list

.PHONY: deploy verify lint clean-runtime reset-runtime

deploy:
	$(INSTALL_CMD)

verify:
	$(LIST_CMD)

lint:
	shellcheck scripts/codex-skills scripts/install-skills.sh

clean-runtime:
	rm -rf $(DOTCODEX_DIR)/skills

reset-runtime: clean-runtime
	rm -f $(DOTCODEX_DIR)/AGENTS.md
