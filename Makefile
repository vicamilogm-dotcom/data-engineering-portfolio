IDU := $(shell id -u)
IDG := $(shell id -g)

######## Initial setup #######

# Create all poetry.lock and install requirements in all challenge at once!
.PHONY: install-poetry
install-poetry:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry install' \;

# direnv allow in all challenge at once!
.PHONY: allow-envrc
allow-envrc:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && direnv allow .' \;

# make you the owner of all challenge folders
.PHONY: own-repo
own-repo:
	@sudo chown $(IDU):$(IDG) -R .

.PHONY: install
install: install-poetry allow-envrc own-repo

######## Ongoing commands #######

# Format all your code everywhere!
.PHONY: format
format:
	find . -name pyproject.toml -exec sh -c 'cd $$(exec dirname {}) && make format' \;

# Run all challenges' tests at once!
.PHONY: test
test:
	find . -name pyproject.toml -exec sh -c 'cd $$(exec dirname {}) && make test' \;

# Update all your virtualenvs at once!
.PHONY: update
update:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry update' \;

	# Refresh all poetry.lock files at once!
.PHONY: refresh-lock
refresh-lock:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && poetry lock --no-update' \;

# Remove all your virtualenvs at once!
.PHONY: remove-venvs
remove-venvs:
	find . -name pyproject.toml -exec sh -c 'echo $$(exec dirname {}) && cd $$(exec dirname {}) && rm -rf .venv' \;

# Delete all your test outputs used by Kitt to track your progress
.PHONY: del-test-output
del-test-output:
	find . -name test_output.txt | xargs rm
