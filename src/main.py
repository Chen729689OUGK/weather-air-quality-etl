
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / "etl.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

PIPELINE_STAGES = [
    ("EXTRACT", SRC_DIR / "extract.py"),
    ("TRANSFORM", SRC_DIR / "transform.py"),
    ("LOAD", SRC_DIR / "load.py"),
    ("VALIDATE", SRC_DIR / "validate.py"),
]


def run_stage(name, script):
    logging.info("=" * 50)
    logging.info("Starting stage: %s", name)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        logging.info("%s output:\n%s", name, result.stdout.strip())

    if result.stderr.strip():
        if result.returncode == 0:
            logging.warning("%s messages:\n%s", name, result.stderr.strip())
        else:
            logging.error("%s errors:\n%s", name, result.stderr.strip())

    if result.returncode != 0:
        raise RuntimeError(
            f"Stage {name} failed with exit code {result.returncode}"
        )

    logging.info("Stage %s completed successfully", name)


def main():
    start_time = datetime.now()
    logging.info("WEATHER AND AIR QUALITY ETL STARTED")

    try:
        for name, script in PIPELINE_STAGES:
            run_stage(name, script)

        elapsed = (datetime.now() - start_time).total_seconds()
        logging.info(
            "ETL PIPELINE COMPLETED SUCCESSFULLY in %.2f seconds",
            elapsed,
        )

    except Exception:
        logging.exception("ETL PIPELINE FAILED")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
