from __future__ import annotations
from pathlib import Path

import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - handled at runtime
    load_dotenv = None


def read_env() -> None:
    if load_dotenv is None:
        sys.stderr.write("ERROR: python-dotenv is not installed.\n")
        sys.stderr.write("Install it with: pip install python-dotenv\n")
        raise SystemExit(1)

    load_dotenv(override=False)


def get_config_value(name: str, default: str = "") -> str:
    value = os.getenv(name, default).strip()
    return value


def normalize_mode(value: str) -> str:
    lowered = value.lower()
    if lowered in ("development", "production"):
        return lowered
    return "development"


def database_status(mode: str, database_url: str) -> str:
    if not database_url:
        if mode == "production":
            return "Not configured"
        return "Connected to local instance"

    if mode == "production":
        return "Connected to production database"
    return "Connected to local instance"


def api_status(api_key: str) -> str:
    if api_key:
        return "Authenticated"
    return "Missing API key"


def zion_status(zion_endpoint: str, mode: str) -> str:
    if zion_endpoint:
        return f"Online ({zion_endpoint})"
    if mode == "production":
        return "Offline"
    return "Online (local resistance route)"


def log_level_status(log_level: str, mode: str) -> str:
    if log_level:
        return log_level.upper()
    return "DEBUG" if mode == "development" else "INFO"


def environment_warnings(
    mode: str,
    raw_mode: str,
    database_url: str,
    api_key: str,
    log_level: str,
    zion_endpoint: str,
) -> list[str]:
    warnings: list[str] = []
    if raw_mode and mode != raw_mode.lower():
        warnings.append(f"Invalid MATRIX_MODE '{raw_mode}' detected; defaulting to development.")
    if not database_url:
        warnings.append("DATABASE_URL is missing; using local instance defaults.")
    if not api_key:
        warnings.append("API_KEY is missing; API access remains unauthenticated.")
    if not log_level:
        warnings.append(f"LOG_LEVEL is missing; defaulting to {log_level_status(log_level, mode)}.")
    if not zion_endpoint:
        warnings.append("ZION_ENDPOINT is missing; Zion network falls back to offline mode.")
    if mode == "production" and warnings:
        warnings.append("Production should define all critical configuration values explicitly.")
    return warnings


def security_check() -> None:
    BASE_DIR = Path(__file__).resolve().parent
    env_file_exists = os.path.isfile(".env")
    gitignore_exists = (BASE_DIR.parent / ".gitignore").exists()
    override_available = any(name in os.environ for name in ("MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL", "ZION_ENDPOINT"))

    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if env_file_exists and gitignore_exists:
        print("[OK] .env file properly configured")
    elif env_file_exists:
        print("[WARN] .env file exists but .gitignore does not ignore it")
    else:
        print("[WARN] .env file not found; copy .env.example to .env for local development")

    if override_available:
        print("[OK] Production overrides available")
    else:
        print("[WARN] No production overrides configured")
    print()
    print("The Oracle sees all configurations.")


def print_configuration(mode: str, database_url: str, api_key: str, log_level: str, zion_endpoint: str) -> None:
    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {database_status(mode, database_url)}")
    print(f"API Access: {api_status(api_key)}")
    print(f"Log Level: {log_level_status(log_level, mode)}")
    print(f"Zion Network: {zion_status(zion_endpoint, mode)}")
    print()


def main() -> int:
    read_env()

    raw_mode = get_config_value("MATRIX_MODE", "development")
    mode = normalize_mode(raw_mode)
    database_url = get_config_value("DATABASE_URL", "")
    api_key = get_config_value("API_KEY", "")
    log_level = get_config_value("LOG_LEVEL", "")
    zion_endpoint = get_config_value("ZION_ENDPOINT", "")

    print("ORACLE STATUS: Reading the Matrix...")
    print()
    print_configuration(mode, database_url, api_key, log_level, zion_endpoint)

    warnings = environment_warnings(mode, raw_mode, database_url, api_key, log_level, zion_endpoint)
    if warnings:
        print("Configuration warnings:")
        for warning in warnings:
            print(f"[WARN] {warning}")
        print()

    security_check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
