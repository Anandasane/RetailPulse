
import logging
import subprocess
import sys
from pathlib import Path


# ============================================
# 1. PROJECT CONFIGURATION
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"


# ============================================
# 2. LOGGING CONFIGURATION
# ============================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)

logger = logging.getLogger("RetailPulse")


# ============================================
# 3. PIPELINE STEP EXECUTION
# ============================================

def run_step(description, command):
    """
    Execute one pipeline stage.

    Capture output, record logs, and stop
    execution if the stage fails.
    """

    logger.info("=" * 60)
    logger.info("STARTING: %s", description)

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False
        )

        # Record standard output.
        if result.stdout:
            for line in result.stdout.splitlines():
                logger.info("[%s] %s", description, line)

        # Record standard error.
        if result.stderr:
            for line in result.stderr.splitlines():
                logger.warning("[%s] %s", description, line)

        # Stop if the command failed.
        if result.returncode != 0:
            raise RuntimeError(
                f"{description} failed "
                f"with exit code {result.returncode}"
            )

        logger.info("COMPLETED: %s", description)

    except Exception:
        logger.exception("FAILED: %s", description)
        raise


# ============================================
# 4. MAIN PIPELINE ORCHESTRATION
# ============================================

def main():

    python = sys.executable

    pipeline_steps = [

        (
            "Data Ingestion",
            [
                python,
                "-m",
                "src.ingestion.ingest_files"
            ]
        ),

        (
            "Data Cleaning",
            [
                python,
                "-m",
                "src.cleaning.clean_data"
            ]
        ),

        (
            "ETL Validation",
            [
                python,
                "-m",
                "src.validation.validate_etl"
            ]
        ),

        (
            "MySQL Database Loading",
            [
                python,
                "-m",
                "src.database.load_data"
            ]
        )
    ]

    logger.info("")
    logger.info("=" * 60)
    logger.info("RETAILPULSE ETL PIPELINE STARTED")
    logger.info("=" * 60)

    try:

        for description, command in pipeline_steps:

            run_step(
                description,
                command
            )

        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("All ETL stages executed successfully.")
        logger.info("Log file: %s", LOG_FILE)
        logger.info("=" * 60)

    except Exception:

        logger.exception("RETAILPULSE PIPELINE FAILED")

        logger.error(
            "Pipeline stopped. Check the log file: %s",
            LOG_FILE
        )

        raise SystemExit(1)


# ============================================
# 5. SCRIPT ENTRY POINT
# ============================================

if __name__ == "__main__":
    main()
