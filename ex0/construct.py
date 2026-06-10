import os
import sys


def package_path(prefix: str) -> str:
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    if sys.platform.startswith("win"):
        return os.path.join(prefix, "Lib", "site-packages")
    return os.path.join(prefix, "lib", version, "site-packages")


def in_matrix() -> None:
    print("MATRIX STATUS: Welcome to the construct")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print(f"Package installation path: {package_path(sys.prefix)}")
    print(f"Global package path: {package_path(sys.base_prefix)}")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")


def out_matrix() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()

    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print("Then run this program again.")


def main() -> None:
    if sys.prefix != sys.base_prefix:
        in_matrix()
    else:
        out_matrix()


if __name__ == "__main__":
    main()
