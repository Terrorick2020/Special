from pathlib import Path

class Settings:
    RESULTS_DIR = Path("C:\\Users\\ta1\\Documents\\projects\\scaner\\app\\results")
    SUBDOMAINS_FILE = Path("C:\\Users\\ta1\\Documents\\projects\\scaner\\app\\subdomains.txt")
    MAX_CONTENT_LINES = 500
    REQUEST_TIMEOUT = 15
    DEEPSEEK_API_KEY = "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"
    DEEPSEEK_MODEL = "deepseek/deepseek-r1"
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0

settings = Settings()