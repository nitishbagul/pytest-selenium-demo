"""Central configuration. Reads from environment variables with sensible defaults,
so the same code runs locally and in CI without edits."""
import os


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))

    # Test credentials (saucedemo provides these publicly)
    STANDARD_USER = "standard_user"
    LOCKED_USER = "locked_out_user"
    PASSWORD = "secret_sauce"
