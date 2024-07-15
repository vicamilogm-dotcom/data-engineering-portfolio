include ../../../make.inc

.PHONY: test_users test_tweets test_likes test

test_users:
	@PYTHONDONTWRITEBYTECODE=1 pytest tests -v --disable-warnings 2>&1 > test_output.txt || echo "let's look at the output"
	PYTHONDONTWRITEBYTECODE=1 pytest tests -m users -v --disable-warnings --color=yes

test_tweets:
	@PYTHONDONTWRITEBYTECODE=1 pytest tests -v --disable-warnings 2>&1 > test_output.txt || echo "let's look at the output"
	PYTHONDONTWRITEBYTECODE=1 pytest tests -m "users or tweets" -v --disable-warnings --color=yes

test_likes:
	@PYTHONDONTWRITEBYTECODE=1 pytest tests -v --disable-warnings 2>&1 > test_output.txt || echo "let's look at the output"
	PYTHONDONTWRITEBYTECODE=1 pytest tests -m likes -v --disable-warnings --color=yes

test: pytest-and-write-output
