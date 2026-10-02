import subprocess
import sys


def run(cmd, description):
    print(f"\n--- Running: {description} ---\n")
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", check=False
    )
    if result.stdout:
        print("STDOUT:\n", result.stdout, sep="")
    if result.stderr:
        print("STDERR:\n", result.stderr, sep="")
    print("Return code:", result.returncode)
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        sys.exit(result.returncode)


run(["ruff", "check", "."], "Ruff Lint")
run(["ruff", "format", "--check", "."], "Ruff Format Check")
