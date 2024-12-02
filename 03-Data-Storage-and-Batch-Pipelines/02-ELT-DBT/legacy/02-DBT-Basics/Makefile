.PHONY: test_hackernews_full test_hackernews_story_comment test

include ../../../make.inc

test_hackernews_full:
	pytest -v --disable-warnings tests/test_hackernews_full.py

test_hackernews_story_comment:
	pytest -v --disable-warnings tests/test_hackernews_story_comment.py

test: pytest-and-write-output
