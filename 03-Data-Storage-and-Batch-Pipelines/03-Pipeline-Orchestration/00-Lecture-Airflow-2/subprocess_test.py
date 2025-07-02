import subprocess


def main() -> None:
    subprocess.run(["ls", "-lha"])


if __name__ == "__main__":
    main()
