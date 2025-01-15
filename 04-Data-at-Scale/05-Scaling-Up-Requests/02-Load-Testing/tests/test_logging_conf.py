from pathlib import Path


class TestLoggingConf:
    def test_logging_conf(self):
        # read configuration file into string
        txt = Path("app/logging.conf").read_text().lower()

        # assess presence of key elements
        assert txt.count("propagate=1") > 2
        assert "args=" in txt
        assert "/app/logs/error.log" in txt
        assert "/app/logs/access.log" in txt
        assert "level=debug" in txt
