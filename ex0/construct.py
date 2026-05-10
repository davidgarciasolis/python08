import sys
import os
import site

def in_matrix() -> None:
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(site.getsitepackages()[0])



def out_matrix() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("To enter the construct, run: ")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix/Mac")
    print("matrix_env\Scripts\activate # On Windows")
    print()
    print("Then run this program again.")
    

def main() -> None:
    if sys.prefix != sys.base_prefix:
        in_matrix()
    else:
        out_matrix()


if __name__ == "__main__":
    main()