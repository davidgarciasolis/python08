#!/usr/bin/env python3

import sys
import os
import site


def is_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def main() -> None:
    in_venv = is_virtual_env()

    if in_venv:
        print("MATRIX STATUS: Welcome to the construct")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        site_packages = site.getsitepackages()
        print("\nPackage installation path:")
        print(site_packages[0])

    else:
        print("MATRIX STATUS: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print("\nTo enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate  # On Unix")
        print("matrix_env\\Scripts\\activate  # On Windows")
        print()
        print("Then run this program again.")


if __name__ == "__main__":
    main()
