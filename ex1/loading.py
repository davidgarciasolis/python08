from importlib import import_module
from types import ModuleType
from typing import Optional

PACKAGES = ["numpy", "pandas", "matplotlib"]


def check_packages() -> Optional[dict[str, ModuleType]]:
    modules = {}

    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    for pkg in PACKAGES:
        try:
            module = import_module(pkg)
            modules[pkg] = module
            print(f"[OK] {pkg} ({module.__version__})")
        except ImportError:
            print(f"[MISSING] {pkg}")
            return None

    return modules


def main() -> None:
    modules = check_packages()

    if not modules:
        print("\nInstall with pip:")
        print("pip install -r requirements.txt")
        print("\nInstall with Poetry:")
        print("poetry install")
        return

    np = modules["numpy"]
    pd = modules["pandas"]

    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")

    data = np.random.randint(0, 100, 1000)
    df = pd.DataFrame({"matrix_data": data})

    print(f"Processing {len(df)} data points...")

    plt.hist(df["matrix_data"], bins=20)
    plt.title("Matrix Data Analysis")
    plt.savefig("matrix_analysis.png")
    print("Generating visualization...")
    print()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
