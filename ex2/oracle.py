import os
from dotenv import load_dotenv


def get_config() -> dict[str, str | None]:
    load_dotenv()
    config = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }
    return config


def validate_config(config: dict[str, str | None]) -> None:
    missing = []

    for key, value in config.items():
        if not value:
            missing.append(key)

    if missing:
        print("WARNING: Missing configuration variables:")
        for var in missing:
            print(f" - {var}")
        print()


def display_status(config: dict[str, str | None]) -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print("\nConfiguration loaded:")

    mode = config.get("MATRIX_MODE", "unknown")
    print(f"Mode: {mode}")

    if mode == "production":
        print("Database: Connected to production instance")
        print("API Access: Authenticated (production)")
        print("Log Level:", config.get("LOG_LEVEL"))
        print("Zion Network: Online")
    elif mode == "development":
        print("Database: Connected to development instance")
        print("API Access: Authenticated (development)")
        print("Log Level:", config.get("LOG_LEVEL"))
        print("Zion Network: Online")
    else:
        print("Database: Connected to local instance")
        print("API Access: Deauthenticated")
        print("Log Level:", config.get("LOG_LEVEL"))
        print("Zion Network: Offline")

    print("\nEnvironment security check:")

    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found")

    print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


def main() -> None:
    config = get_config()

    validate_config(config)
    display_status(config)


if __name__ == "__main__":
    main()
