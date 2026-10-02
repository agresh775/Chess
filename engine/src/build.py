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


run(
    [
        "cmake",
        "-S",
        ".",
        "-B",
        "../../build",
        "-G",
        "Ninja",
        "-DCMAKE_CXX_COMPILER=g++",
        "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
    ],
    "CMake Configure",
)
run(["cmake", "--build", "../../build"], "CMake Build")
run(
    [
        "clang-tidy",
        "-p",
        "../../build/",
        "--config-file=../../config/.clang-tidy",
        "main.cpp",
    ],
    "Clang-Tidy",
)
run(
    [
        "clang-format",
        "--dry-run",
        "--Werror",
        "-style=file:../../config/.clang-format",
        "main.cpp",
    ],
    "Clang-Format Check",
)
