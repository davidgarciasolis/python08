from __future__ import annotations

import os
import sys
from importlib import import_module, metadata
from pathlib import Path
from typing import Any


REQUIRED_PACKAGES = ("numpy", "pandas", "matplotlib")
OPTIONAL_PACKAGES = ("requests",)
OUTPUT_FILE = Path("matrix_analysis.png")


def package_version(name: str, module: Any | None) -> str:
    if module is not None:
        version = getattr(module, "__version__", None)
        if version:
            return str(version)

    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "unknown"


def load_dependencies() -> tuple[dict[str, Any], list[str], list[str]]:
    """Revision de paquetes requeridos y opcionales"""
    modules: dict[str, Any] = {}
    missing_required: list[str] = []
    missing_optional: list[str] = []

    for name in REQUIRED_PACKAGES + OPTIONAL_PACKAGES:
        try:
            modules[name] = import_module(name)
        except Exception:
            modules[name] = None
            if name in REQUIRED_PACKAGES:
                missing_required.append(name)
            else:
                missing_optional.append(name)

    return modules, missing_required, missing_optional


def print_dependency_report(modules: dict[str, Any], api_mode: bool) -> None:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    for name in REQUIRED_PACKAGES:
        module = modules.get(name)
        version = package_version(name, module)
        status = "OK" if module is not None else "MISSING"
        message = "ready"
        if name == "numpy":
            message = "Numerical computation ready"
        elif name == "pandas":
            message = "Data manipulation ready"
        elif name == "matplotlib":
            message = "Visualization ready"
        print(f"[{status}] {name} ({version}) - {message}")

    if api_mode:
        module = modules.get("requests")
        version = package_version("requests", module)
        if module is not None:
            status = "OK"
        else:
            status = "MISSING"
        if module is not None:
            message = "Network access ready"
        else:
            message = "Optional API access unavailable"
        print(f"[{status}] requests ({version}) - {message}")


def print_manager_comparison() -> None:
    poetry_active = (bool(os.environ.get("POETRY_ACTIVE"))
                     or "poetry" in sys.executable.lower())
    pip_env = sys.prefix != sys.base_prefix

    print("Package manager comparison:")
    print("- pip: installs directly from requirements.txt "
          "with `pip install -r requirements.txt`.")
    print("- Poetry: reads pyproject.toml, resolves dependencies"
          ", and uses a lockfile with `poetry install`.")
    if poetry_active:
        print("- Current environment: Poetry-managed execution detected.")
    elif pip_env:
        print("- Current environment: virtual environment detected;"
              " this is the usual pip workflow.")
    else:
        print("- Current environment: global interpreter detected;"
              " package installs would affect the system Python.")


def build_matrix_data(np: Any, pd: Any, rows: int = 1000) -> Any:
    rng = np.random.default_rng(42)
    cycle = np.arange(rows)
    drift = np.cumsum(rng.normal(0.02, 0.12, size=rows))
    interference = rng.normal(0.0, 0.8, size=rows)
    signal = drift + interference
    stability = (100 - (np.abs(signal) * 11
                 + np.abs(rng.normal(0.0, 3.0, size=rows))))
    stability = np.clip(stability, 0, 100)

    frame = pd.DataFrame(
        {
            "cycle": cycle,
            "signal": signal,
            "stability": stability,
        }
    )
    frame["rolling_stability"] = (frame["stability"].rolling
                                  (window=40, min_periods=1).mean())
    frame["zone"] = pd.cut(
        frame["stability"],
        bins=[-0.1, 40, 70, 100],
        labels=["critical", "unstable", "stable"],
    )
    return frame


def summarize_matrix_data(frame: Any, api_mode: bool) -> None:
    stats = frame["stability"].describe()
    zone_counts = (frame["zone"].value_counts(dropna=False).reindex
                   (["critical", "unstable", "stable"], fill_value=0))

    print("Analyzing Matrix data...")
    print(f"Processing {len(frame)} data points...")
    print(f"Average stability: {stats['mean']:.2f}")
    print(f"Minimum stability: {stats['min']:.2f}")
    print(f"Maximum stability: {stats['max']:.2f}")
    print("Zone distribution:")
    for zone, count in zone_counts.items():
        print(f"- {zone}: {int(count)}")

    print("Installed versions snapshot:")
    print(f"- numpy: {package_version('numpy', sys.modules.get('numpy'))}")
    print(f"- pandas: {package_version('pandas', sys.modules.get('pandas'))}")
    print(f"- matplotlib: "
          f"{package_version('matplotlib', sys.modules.get('matplotlib'))}")
    if api_mode and sys.modules.get("requests") is not None:
        print(f"- requests: "
              f"{package_version('requests', sys.modules.get('requests'))}")


def create_visualization(frame: Any, plt: Any) -> None:
    print("Generating visualization...")

    fig, (ax1, ax2) = plt.subplots(2, 1,
                                   figsize=(11, 8), constrained_layout=True)
    fig.suptitle("Matrix Stability Analysis", fontsize=16, fontweight="bold")

    ax1.plot(frame["cycle"], frame["stability"],
             color="#2ec4b6", alpha=0.35, linewidth=1, label="stability")
    ax1.plot(frame["cycle"], frame["rolling_stability"],
             color="#e71d36", linewidth=2.2, label="rolling mean")
    ax1.set_xlabel("Cycle")
    ax1.set_ylabel("Stability")
    ax1.set_ylim(0, 105)
    ax1.legend(frameon=False)
    ax1.grid(alpha=0.2)

    zone_counts = (frame["zone"].value_counts().reindex
                   (["critical", "unstable", "stable"], fill_value=0))
    ax2.bar(zone_counts.index.astype(str), zone_counts.values,
            color=["#ff6b6b", "#f4a261", "#2a9d8f"])
    ax2.set_xlabel("Zone")
    ax2.set_ylabel("Count")
    ax2.grid(axis="y", alpha=0.2)

    fig.savefig(OUTPUT_FILE, dpi=160)
    plt.close(fig)


def show_missing_help(missing_required: list[str],
                      missing_optional: list[str], api_mode: bool) -> int:
    print("Dependency check failed.")
    if missing_required:
        print("Missing required packages:")
        for name in missing_required:
            print(f"- {name}")
    if api_mode and missing_optional:
        print("Missing optional packages:")
        for name in missing_optional:
            print(f"- {name}")
    print()
    print("Install with pip:")
    print("  pip install -r requirements.txt")
    print("Install with Poetry:")
    print("  poetry install")
    print("Run with Poetry:")
    print("  poetry run python loading.py")
    return 1


def main() -> int:
    api_mode = "--api" in sys.argv
    modules, missing_required, missing_optional = load_dependencies()

    print_dependency_report(modules, api_mode=api_mode)
    print_manager_comparison()

    if missing_required:
        return show_missing_help(missing_required, missing_optional, api_mode)

    np = modules["numpy"]
    pd = modules["pandas"]
    matplotlib = modules["matplotlib"]
    matplotlib.use("Agg")
    plt = import_module("matplotlib.pyplot")

    frame = build_matrix_data(np, pd)
    summarize_matrix_data(frame, api_mode=api_mode)
    create_visualization(frame, plt)

    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    main()
